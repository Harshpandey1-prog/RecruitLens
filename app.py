import streamlit as st
import plotly.express as px
import pandas as pd

from github_api.fetch_user import get_user
from github_api.fetch_repos import get_repositories

from github_api.fetch_user import get_user
from github_api.fetch_repos import get_repositories

from components.charts import show_language_charts

from components.skills import show_skills

from components.insights import show_insights
from components.roles import show_roles

from components.score import show_score

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf(
    username,
    score,
    followers,
    repo_count,
    total_stars,
    total_forks,
    roles,
    skills
):

    pdf = SimpleDocTemplate("RecruitLens_Report.pdf")
    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b>RecruitLens AI Report</b>", styles["Title"]))

    story.append(Paragraph(f"Developer : {username}", styles["Normal"]))

    story.append(Paragraph(f"Developer Score : {score}/100", styles["Normal"]))

    story.append(Paragraph(f"Followers : {followers}", styles["Normal"]))

    story.append(Paragraph(f"Repositories : {repo_count}", styles["Normal"]))

    story.append(Paragraph(f"Total Stars : {total_stars}", styles["Normal"]))

    story.append(Paragraph(f"Total Forks : {total_forks}", styles["Normal"]))

    story.append(Paragraph("<br/><b>Detected Skills</b>", styles["Heading2"]))

    for skill in skills:
        story.append(Paragraph(skill, styles["Normal"]))

    story.append(Paragraph("<br/><b>Recommended Roles</b>", styles["Heading2"]))

    for role in roles:
        story.append(Paragraph(role[0], styles["Normal"]))

    pdf.build(story)


# Page Configuration
st.set_page_config(
    page_title="RecruitLens",
    page_icon="🔍",
    layout="wide"
)


# Title
st.title("🔍 RecruitLens")
st.write("GitHub Profile Analyzer for Recruiters")


# Input
username = st.text_input(
    "Enter GitHub Username",
    placeholder="Example: torvalds"
)


# Button
if "analyzed" not in st.session_state:
    st.session_state.analyzed = False

if st.button("Analyze"):
    st.session_state.analyzed = True

if st.session_state.analyzed and username:
    


    if username:

        # Fetch User Data
        user = get_user(username)

        if user:

            st.success("Profile Found ✅")

            # Profile Section
            col1, col2 = st.columns(2)

            with col1:
                st.image(
                    user["avatar_url"],
                    width=150
                )

            with col2:
                st.subheader(user.get("name") or user["login"])
                st.write(user.get("bio") or "No bio available.")
                st.write("🔗", user["html_url"])


            st.divider()


            # Metrics
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Followers",
                    user["followers"]
                )

            with col2:
                st.metric(
                    "Following",
                    user["following"]
                )

            with col3:
                st.metric(
                    "Repositories",
                    user["public_repos"]
                )


            st.divider()


            # Repository Section
            st.subheader("📂 Repositories")
            # 🔍 Search Repository
            search_repo = st.text_input( 
            "🔍 Search Repository",
            placeholder="Type repository name..."

        )


            repos = get_repositories(username)
            language_count = {}

            for repo in repos:

                language = repo["language"]

                if language:

                  if language in language_count:
                     language_count[language] += 1
                  else:
                     language_count[language] = 1

                  
                  
            language_df = pd.DataFrame({
                "Language": language_count.keys(),
                "Repositories": language_count.values()
                    
            })
            # -----------------------------
            # Developer Score
            # -----------------------------

            total_stars = sum(repo["stargazers_count"] for repo in repos)
            total_forks = sum(repo["forks_count"] for repo in repos)

            languages = len(set(
                repo["language"]
                for repo in repos
                if repo["language"]
            ))

            followers = user["followers"]
            repo_count = user["public_repos"] 

            score = 0


            score += min(followers // 100, 20)
            score += min(repo_count, 20)
            score += min(total_stars // 100, 20)
            score += min(languages * 4, 20)
            score += min(total_forks // 20, 20)

            st.divider()
            show_score(
                 score,
                 followers,
                 repo_count,
                 languages,
                total_stars
            )

           

            st.divider()

            show_insights(
                 followers,
                 repo_count,
                 languages,
                total_stars
            )





    
         
        st.divider()

        st.subheader("🏆 Top Repository")  

        top_repo = max(
            repos,
            key=lambda repo: repo["stargazers_count"]
        ) 

        col1, col2 = st.columns([1, 2])

        with col1:
            st.metric("⭐ Stars", top_repo["stargazers_count"])
            st.metric("🍴 Forks", top_repo["forks_count"])

        with col2:
            st.subheader(top_repo["name"])
            st.write(f"💻 Language: {top_repo['language']}")
            st.write(top_repo["description"] or "No description available.")
            st.link_button("🔗 Open Repository", top_repo["html_url"])  

        

        st.divider()
        skills = show_skills(repos)

        st.divider()
        
        roles = []

        if "🐍 Python" in skills:
             roles.append(("🥇 Data Scientist", 95))
             roles.append(("🥈 Machine Learning Engineer", 90))

        if "📊 Data Analysis" in skills:
             roles.append(("📈 Data Analyst", 88))

        if "💾 SQL" in skills:
             roles.append(("🗄 Database Developer", 82))

        if "☕ Java" in skills:
             roles.append(("☕ Java Developer", 85))

        if "🌐 JavaScript" in skills:
            roles.append(("🌐 Full Stack Developer", 84))

        if "💻 C Programming" in skills:
            roles.append(("⚙ Backend Developer", 75))

        if "🧮 Data Structures & Algorithms" in skills:
            roles.append(("💻 Software Engineer", 80))

        roles = sorted(roles, key=lambda x: x[1], reverse=True)

        show_roles(roles)

        st.divider()

        st.subheader("📄 Recruiter Report")

        if st.button("📥 Generate PDF Report"):

           generate_pdf(
           username=username,
           score=score,
           followers=followers,
           repo_count=repo_count,
           total_stars=total_stars,
           total_forks=total_forks,
           roles=roles,
           skills=sorted(skills)
        )

        st.success("✅ PDF Report Generated Successfully!")  

        if st.button("⬇ Download PDF"):

           with open("RecruitLens_Report.pdf", "rb") as pdf_file:

                st.download_button(
                   label="📥 Click Here to Download",
                   data=pdf_file,
                   file_name="RecruitLens_Report.pdf",
                   mime="application/pdf"
                )





   
        show_language_charts(language_df)

      
        total_stars = 0
        total_forks = 0
        languages = []

        latest_update = ""

        repo_with_max_stars = ""
        max_stars = 0

        for repo in repos:
                total_stars += repo["stargazers_count"]
                total_forks += repo["forks_count"]

                if repo["language"]:
                   languages.append(repo["language"])

                if repo["updated_at"] > latest_update:
                   latest_update = repo["updated_at"]

                if repo["stargazers_count"] > max_stars:
                   max_stars = repo["stargazers_count"]
                   repo_with_max_stars = repo["name"]

        col1, col2, col3 = st.columns(3)

        with col1:
                st.metric("⭐ Total Stars", total_stars)

        with col2:
                st.metric("🍴 Total Forks", total_forks)

        with col3:
                st.metric("💻 Languages", len(set(languages)))
        st.divider()

        st.subheader("📊 GitHub Activity Dashboard")

        col1, col2 = st.columns(2)

        with col1:
             st.metric("📅 Latest Activity", latest_update[:10])

        with col2:
             st.metric("🏆 Most Popular Repo", repo_with_max_stars) 

        if latest_update[:4] == "2026":
            st.success("🔥 Very Active Developer")
        else:
            st.warning("⚠️ Profile seems less active")    

        for repo in repos:
               
               # Search Filter
               if search_repo:
                  if search_repo.lower() not in repo["name"].lower():
                     continue
                  
               with st.container():

                    st.markdown(f"### 📂 {repo['name']}")
                    quality_score = 0
                    # Description
                    if repo["description"]:
                       quality_score += 20

                    # Stars
                    if repo["stargazers_count"] >= 100:
                        quality_score += 30
                    elif repo["stargazers_count"] >= 10:
                         quality_score += 20
                    else:
                        quality_score += 10

                    # Forks
                    if repo["forks_count"] >= 50:
                       quality_score += 20
                    elif repo["forks_count"] >= 10:
                        quality_score += 10

                    # Language
                    if repo["language"]:
                       quality_score += 15

                    # Recently Updated
                    quality_score += 15


                    col1, col2, col3 = st.columns(3)

               with col1:
                    st.metric("⭐ Stars", repo["stargazers_count"])

               with col2:
                    st.metric("🍴 Forks", repo["forks_count"])

               with col3:
                   st.metric("💻 Language", repo["language"] if repo["language"] else "N/A"
                             
                )

               date = repo["updated_at"][:10]
               st.write(f"📅 Last Updated: {date}")

               st.metric("⭐ Quality Score", f"{quality_score}/100")

               if quality_score >= 85:
                  st.success("🏆 Excellent Repository")

               elif quality_score >= 70:
                    st.info("🚀 Good Repository")

               elif quality_score >= 50:
                    st.warning("👍 Average Repository")

               else:
                   st.error("⚠ Needs Improvement")

               st.subheader("🤖 AI Repository Summary")
               summary = ""

               if repo["language"] == "Python":
                  summary = (
                     "This repository is built using Python. "
                     "It may demonstrate programming, automation, "
                     "data science or machine learning skills."
                )

               elif repo["language"] == "C":
                   summary = (
                     "This repository is built using C. "
                     "It demonstrates strong programming fundamentals, "
                     "system-level development and problem-solving skills."
                )

               elif repo["language"] == "C++":
                    summary = (
                      "This repository is built using C++. "
                      "It highlights object-oriented programming and "
                      "data structures & algorithms expertise."
                )

               elif repo["language"] == "Java":
                    summary = (
                       "This repository is built using Java. "
                       "It reflects object-oriented programming "
                       "and backend development knowledge."
                )

               elif repo["language"] == "JavaScript":
                    summary = (
                       "This repository is built using JavaScript. "
                       "It showcases frontend or full-stack "
                       "web development skills."
                )

               else:
                  summary = (
                    "This repository demonstrates software development "
                    "skills using modern programming technologies."
                ) 

               summary += (
                   f"\n\n⭐ {repo['stargazers_count']} Stars"
                   f"\n🍴 {repo['forks_count']} Forks"
                   f"\n📅 Last Updated: {repo['updated_at'][:10]}"
                )

               st.info(summary)


               st.link_button("🔗 Open Repository", repo["html_url"])

               st.divider()  

   
      