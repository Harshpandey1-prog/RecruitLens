import streamlit as st

def show_roles(roles):

    st.subheader("🎯 Best Suitable Roles")

    if len(roles) == 0:
        st.warning("No suitable roles detected.")
        return

    for role in roles:
        st.write(f"✅ {role[0]} ({role[1]}%)")