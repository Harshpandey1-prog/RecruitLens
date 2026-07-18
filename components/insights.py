import streamlit as st

def show_insights(followers, repo_count, languages, total_stars):

    st.subheader("💡 AI Insights")

    insights = []

    if followers >= 100:
        insights.append("✅ Strong GitHub Community Presence")
    else:
        insights.append("⚠️ Increase followers to improve visibility")

    if repo_count >= 10:
        insights.append("✅ Good number of public repositories")
    else:
        insights.append("⚠️ Add more public repositories")

    if languages >= 3:
        insights.append("✅ Uses multiple programming languages")
    else:
        insights.append("⚠️ Learn more programming languages")

    if total_stars >= 100:
        insights.append("✅ Repositories receive good community support")
    else:
        insights.append("⚠️ Work on projects that attract more stars")

    for insight in insights:
        st.write(insight)

    return insights