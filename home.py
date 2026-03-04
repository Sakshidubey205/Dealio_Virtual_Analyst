import streamlit as st

# --- Page Configuration ---
st.set_page_config(
    page_title="Dealio - Virtual Analyst",
    page_icon="📊",
    layout="wide"
)

# --- Title ---
st.markdown("""
<h1 style='text-align:center; color:#1f3b4d; font-size:48px;'>
🚀 Dealio – The Virtual Product Intelligence Analyst
</h1>
""", unsafe_allow_html=True)

st.markdown("---")

# --- Intro Section ---
st.markdown("""
### 🔍 Transform Product Data into Smart Decisions

**Dealio** is an AI-powered **Virtual Product Intelligence Analyst** that helps businesses, analysts, and customers make **data-driven product decisions**.

Using **Machine Learning models**, Dealio can:

- Predict product **ratings**
- Estimate optimal **pricing**
- Discover **feature impact**
- Provide **business insights**

Turn **raw product data into actionable intelligence.**
""")

st.markdown("---")

# --- Why Dealio Section ---
st.markdown("## 🎯 Why Dealio?")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.info("🛍 Customers want **better value**")

with col2:
    st.info("🏢 Businesses want **better pricing strategy**")

with col3:
    st.info("🏷 Brands want **stronger positioning**")

with col4:
    st.info("📊 Analysts want **faster insights**")

st.markdown("---")

# --- Core Features Section ---
st.markdown("## 🚀 Core Features")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### ⭐ Rating Prediction Model")

    st.write("""
Predict product ratings based on:

- Technical features  
- Brand  
- Battery performance  
- Customer engagement  
- Product specifications  

This helps understand **what drives customer satisfaction.**
""")

with col2:
    st.markdown("### 💰 Price Prediction Model")

    st.write("""
Estimate optimal product pricing using:

- Brand positioning  
- Feature set  
- Specifications  
- Market patterns  

This helps businesses **identify the right price strategy.**
""")

st.markdown("---")

# --- Advanced Features ---
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🤖 Comparative Model Analysis")

    st.write("""
Dealio automatically:

- Tests multiple ML models  
- Uses cross-validation  
- Selects the best-performing model  
- Ensures statistical reliability
""")

with col2:
    st.markdown("### ⚙ Automated Data Pipeline")

    st.write("""
The system includes:

- Missing value handling  
- Feature encoding  
- Data scaling  
- Model training  
- Model comparison  
- Deployment-ready models
""")

st.markdown("---")

# --- Who Can Use Dealio ---
st.markdown("## 👥 Who Can Use Dealio?")

col1, col2, col3 = st.columns(3)

with col1:
    st.success("""
### 🛍 Customers

- Compare products intelligently  
- Understand rating drivers  
- Make smarter purchases
""")

with col2:
    st.success("""
### 🏢 Businesses

- Optimize pricing strategies  
- Improve product design  
- Analyze customer satisfaction
""")

with col3:
    st.success("""
### 📊 Analysts

- Test ML models quickly  
- Compare performance  
- Deploy models easily
""")

st.markdown("---")

# --- Navigation Section ---
st.markdown("""
## 🚀 Navigation Guide

Use the **sidebar menu** to explore:

🏠 **Home** – Overview of Dealio  
💰 **Price Predictor** – Predict product pricing  
📈 **Analysis App** – Explore insights & analytics
""")

st.markdown("---")

# --- Footer ---
st.markdown("""
<div style='text-align:center; color:gray;'>
Made with ❤️ using Streamlit
</div>
""", unsafe_allow_html=True)

# --- Developer Badge ---
st.markdown("""
<div style='position: fixed; bottom: 20px; right: 20px;
background-color:#1f3b4d; padding:10px 18px;
border-radius:10px; color:white; font-size:14px;'>
Developed by Sakshi
</div>
""", unsafe_allow_html=True)