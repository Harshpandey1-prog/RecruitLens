import streamlit as st
import plotly.express as px


def show_language_charts(language_df):

    st.subheader("📊 Language Distribution")

    fig = px.pie(
        language_df,
        names="Language",
        values="Repositories",
        hole=0.45,
        title="Most Used Languages"
    )

    fig.update_traces(
        textposition="inside",
        textinfo="label+percent"
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="language_distribution_chart"
    )

    st.subheader("📊 Top Languages")

    bar_fig = px.bar(
        language_df,
        x="Language",
        y="Repositories",
        text="Repositories",
        title="Repositories by Language"
    )

    bar_fig.update_traces(textposition="outside")

    st.plotly_chart(
        bar_fig,
        use_container_width=True,
        key="top_languages_chart"
    )