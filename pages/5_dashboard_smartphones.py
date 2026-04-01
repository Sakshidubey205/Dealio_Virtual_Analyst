import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="EDA Dashboard", layout="wide")

#  LOAD DATA
@st.cache_data
def load_data():
    df = pd.read_csv("C:\\Users\\DEEL\\dealio_major_project_final_folder\\smartphone_cleaned_v4.csv")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# TITLE

st.title(" Smartphone Market Analysis Dashboard")

st.write("""
This dashboard provides detailed insights into smartphone market trends,
features, pricing, and user preferences using Exploratory Data Analysis (EDA).
""")

st.markdown("---")

#  SECTION 1: DISTRIBUTION


st.header(" Price & Rating Analysis")

col1, col2 = st.columns(2)

with col1:
    fig = px.histogram(df, x='price', nbins=50, title="Price Distribution")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.histogram(df, x='rating', nbins=50, title="Rating Distribution")
    st.plotly_chart(fig, use_container_width=True)

#SECTION 2: PRICE VS FEATURES


st.header(" Price vs Features")

col1, col2 = st.columns(2)

with col1:
    fig = px.scatter(df, x='price', y='ram_capacity',
                     title="Price vs RAM", color='ram_capacity')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.scatter(df, x='price', y='battery_capacity',
                     title="Price vs Battery", color='battery_capacity')
    st.plotly_chart(fig, use_container_width=True)

# SECTION 3: BRAND ANALYSIS

st.header(" Brand Analysis")

top_brands = df['brand_name'].value_counts().head(10).reset_index()
top_brands.columns = ['brand_name', 'count']

fig = px.bar(top_brands, x='count', y='brand_name',
             orientation='h', title="Top 10 Brands")
st.plotly_chart(fig, use_container_width=True)

# SECTION 4: 5G & FEATURES

st.header(" Feature Adoption")

col1, col2, col3 = st.columns(3)

with col1:
    fig = px.histogram(df, x='has_5g', title="5G Support")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.histogram(df, x='has_nfc', title="NFC Support")
    st.plotly_chart(fig, use_container_width=True)

with col3:
    fig = px.histogram(df, x='has_ir_blaster', title="IR Blaster")
    st.plotly_chart(fig, use_container_width=True)

# SECTION 5: DISPLAY

st.header(" Display Analysis")

col1, col2 = st.columns(2)

with col1:
    fig = px.histogram(df, x='screen_size', title="Screen Size Distribution")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.histogram(df, x='refresh_rate', title="Refresh Rate")
    st.plotly_chart(fig, use_container_width=True)

#  SECTION 6: CAMERA

st.header(" Camera Analysis")

col1, col2 = st.columns(2)

with col1:
    fig = px.scatter(df, x='price', y='primary_camera_rear',
                     title="Price vs Rear Camera",
                     color='primary_camera_rear')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.scatter(df, x='price', y='primary_camera_front',
                     title="Price vs Front Camera",
                     color='primary_camera_front')
    st.plotly_chart(fig, use_container_width=True)

#SECTION 7: PROCESSOR

st.header(" Processor Analysis")

fig = px.histogram(df, y='processor_brand',
                   title="Processor Distribution")
st.plotly_chart(fig, use_container_width=True)

# SECTION 8: STORAGE & RAM

st.header(" Storage & RAM")

col1, col2 = st.columns(2)

with col1:
    fig = px.histogram(df, x='ram_capacity',
                       title="RAM Distribution")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.histogram(df, x='internal_memory',
                       title="Storage Distribution")
    st.plotly_chart(fig, use_container_width=True)

#  SECTION 9: OS

st.header(" OS Distribution")

fig = px.histogram(df, x='os', title="Operating System")
st.plotly_chart(fig, use_container_width=True)

#  SECTION 10: CORRELATION

st.header(" Correlation Heatmap")

numeric_df = df.select_dtypes(include=['int64','float64'])

fig = px.imshow(numeric_df.corr(),
                text_auto=True,
                title="Correlation Matrix",
                aspect="auto",
                color_continuous_scale='RdBu_r')

st.plotly_chart(fig, use_container_width=True)