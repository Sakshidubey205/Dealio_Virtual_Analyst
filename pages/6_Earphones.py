import streamlit as st
import webbrowser
import os
from streamlit.components.v1 import html


st.set_page_config(page_title="Earphones Analysis", layout="wide")

# =========================
# TITLE
# =========================
st.title(" Earphones Market Analysis")

# =========================
# INTRODUCTION
# =========================
st.write("""
This page helps you understand the Earphones market using data analysis
and machine learning models.

You can:
-  Explore market trends
-  Predict ratings and prices
-  Get smart recommendations

Use the options below to explore different functionalities.
""")

st.markdown("---")

#  BUTTONS

col1, col2, col3 , col4  = st.columns(4)

with col1:
    if st.button(" Recommendation System "):
        st.switch_page("pages/7_Recommendation.py")

with col2:
    if st.button(" Rating Prediction "):
        st.switch_page("pages/8_Rating_Prediction.py")

with col3:
    if st.button("Price Prediction"):
        st.switch_page("pages/9_Price_Prediction.py")

with col4:
    if st.button("Dashboard of the Smartphone Market"):
        st.switch_page("pages/10_dashboard_of_earphones.py")

st.markdown("---")
st.subheader("📊 Auto EDA Report")

if st.button("Generate Full EDA Report"):

    file_path = "eda_report.html"

    if os.path.exists(file_path):
        webbrowser.open_new_tab(file_path)
    else:
        st.error("EDA report not found. Please generate it first.")