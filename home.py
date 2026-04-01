import streamlit as st

st.set_page_config(page_title="Dealio", layout="wide")

st.title("Dealio - Market Intelligence Platform")

st.write("""
Tilio is a smart analytics platform that helps you understand market trends,
analyze products, and make data-driven decisions.

In this project, we analyze the smartphone/Earphones market using machine learning
and recommendation systems.
""")

st.markdown("## Smartphone Analysis")

if st.button("Go to Smartphone Analysis"):
    st.switch_page("pages/1_Smartphone.py")

st.markdown("## Earphones Analysis")

if st.button("Go to Earphones Analysis"):
    st.switch_page("pages/6_Earphones.py")