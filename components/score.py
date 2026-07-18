import streamlit as st


def show_score(
    score,
    followers,
    repo_count,
    languages,
    total_stars
):

    st.subheader("🤖 Developer Score")
    st.metric("Overall Score", f"{score}/100")

    if score >= 90:
        st.success("🌟 Excellent Developer")
    elif score >= 75:
        st.info("🚀 Strong Developer")
    elif score >= 60:
        st.warning("👍 Good Developer")
    else:
        st.error("📘 Beginner Developer")

    st.divider()

    st.subheader("💪 GitHub Profile Strength")

    st.progress(score / 100)
    st.write(f"Profile Strength: {score}%")

    if score >= 90:
        st.success("🌟 Excellent Profile")
    elif score >= 75:
        st.info("🚀 Strong Profile")
    elif score >= 60:
        st.warning("👍 Good Profile")
    else:
        st.error("📘 Needs Improvement")

    st.divider()

    st.subheader("🤖 Recruiter Recommendation")

    recommendation = []

    if score >= 85:
        hiring = "🟢 Highly Recommended"
    elif score >= 70:
        hiring = "🟡 Recommended"
    else:
        hiring = "🔴 Needs Improvement"

    st.metric("Hiring Score", f"{score}/100")
    st.success(hiring)

    if followers >= 100:
        recommendation.append("✔ Strong GitHub Profile")

    if languages >= 3:
        recommendation.append("✔ Multiple Programming Languages")

    if total_stars >= 100:
        recommendation.append("✔ High Community Engagement")

    if repo_count >= 10:
        recommendation.append("✔ Good Repository Collection")

    for item in recommendation:
        st.write(item)