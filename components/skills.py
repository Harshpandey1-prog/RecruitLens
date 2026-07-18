import streamlit as st

def show_skills(repos):

    skills = set()

    for repo in repos:

        language = repo["language"]

        if language == "Python":
            skills.update([
                "🐍 Python",
                "📊 Data Analysis",
                "🤖 Machine Learning"
            ])

        elif language == "Jupyter Notebook":
            skills.update([
                "📒 Jupyter Notebook",
                "📈 Data Science"
            ])

        elif language == "SQL":
            skills.update([
                "💾 SQL",
                "🗄 Database Management"
            ])

        elif language == "Java":
            skills.update([
                "☕ Java",
                "⚙ Object-Oriented Programming"
            ])

        elif language == "JavaScript":
            skills.update([
                "🌐 JavaScript",
                "🎨 Web Development"
            ])

        elif language == "C":
            skills.update([
                "💻 C Programming",
                "⚡ Problem Solving"
            ])

        elif language == "C++":
            skills.update([
                "🚀 C++",
                "🧮 Data Structures & Algorithms"
            ])

    st.subheader("🧠 AI Skill Detection")

    if skills:
        st.success("Detected Skills")

        for skill in sorted(skills):
            st.write("✅", skill)

    else:
        st.warning("No skills detected.")

    return skills