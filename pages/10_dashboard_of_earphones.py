import streamlit as st
import pandas as pd
import plotly.express as px


# =========================
# 🚀 PAGE CONFIG
# =========================
st.set_page_config(page_title="Smartphone Dashboard", layout="wide")

# =========================
# 📊 LOAD DATA
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv("C:\\Users\\DEEL\\dealio_major_project_final_folder\\flipkart.csv")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# =========================
# 🧹 DATA CLEANING
# =========================

def clean_price(col):
    return (
        col.astype(str)
        .str.replace('₹', '', regex=False)
        .str.replace(',', '', regex=False)
        .str.strip()
    )

# Check required columns
required_cols = ['offer_price', 'real_price', 'ratings']
for col in required_cols:
    if col not in df.columns:
        st.error(f"❌ Missing column: {col}")
        st.stop()

# Clean price columns
df['offer_price'] = clean_price(df['offer_price'])
df['real_price'] = clean_price(df['real_price'])

df['offer_price'] = pd.to_numeric(df['offer_price'], errors='coerce')
df['real_price'] = pd.to_numeric(df['real_price'], errors='coerce')

# Clean ratings
df['ratings'] = pd.to_numeric(df['ratings'], errors='coerce')

# =========================
# 💸 CREATE DISCOUNT COLUMN (SAFE)
# =========================
if 'calculated_discount' not in df.columns:
    df['calculated_discount'] = (
        (df['real_price'] - df['offer_price']) / df['real_price']
    ) * 100

df['calculated_discount'] = df['calculated_discount'].round(2)
df['calculated_discount'] = df['calculated_discount'].replace([float('inf'), -float('inf')], 0)
df['calculated_discount'] = df['calculated_discount'].fillna(0)

# Drop invalid rows
df = df.dropna(subset=['offer_price', 'real_price', 'ratings'])

# =========================
# 🎯 TITLE
# =========================
st.title("📱 Smartphone Market Analysis Dashboard")
st.markdown("Explore trends, pricing, brands, and customer behavior interactively.")

# =========================
# 🎛 SIDEBAR FILTERS
# =========================
st.sidebar.header("🔍 Filters")

selected_company = st.sidebar.multiselect(
    "Select Company",
    options=df['company'].dropna().unique(),
    default=df['company'].dropna().unique()[:5] if 'company' in df.columns else []
)

price_range = st.sidebar.slider(
    "Select Price Range",
    int(df['offer_price'].min()),
    int(df['offer_price'].max()),
    (int(df['offer_price'].min()), int(df['offer_price'].max()))
)

# Apply filters
filtered_df = df[
    (df['offer_price'] >= price_range[0]) &
    (df['offer_price'] <= price_range[1])
]

if 'company' in df.columns and selected_company:
    filtered_df = filtered_df[filtered_df['company'].isin(selected_company)]

# =========================
# 📊 KPI METRICS
# =========================
col1, col2, col3 = st.columns(3)

col1.metric("📦 Total Products", len(filtered_df))
col2.metric("⭐ Avg Rating", round(filtered_df['ratings'].mean(), 2))
col3.metric("💸 Avg Discount (%)", round(filtered_df['calculated_discount'].mean(), 2))

st.markdown("---")

# =========================
# 📑 TABS
# =========================
tab1, tab2, tab3 = st.tabs(["📊 Overview", "💰 Pricing", "⭐ Ratings & Features"])

# =========================
# 📊 TAB 1: OVERVIEW
# =========================
with tab1:

    if 'color' in df.columns:
        st.subheader("🎨 Top Colors")
        top_colors = filtered_df['color'].value_counts().head(10)

        fig_colors = px.bar(
            x=top_colors.index,
            y=top_colors.values,
            color=top_colors.values,
            title="Top Colors"
        )
        st.plotly_chart(fig_colors, use_container_width=True)

    if 'type' in df.columns:
        st.subheader("🎧 Earphone Types")
        type_counts = filtered_df['type'].value_counts().reset_index()
        type_counts.columns = ['type', 'count']

        fig_type = px.bar(type_counts, x='type', y='count', color='count')
        st.plotly_chart(fig_type, use_container_width=True)

    if 'company' in df.columns:
        st.subheader("🏷 Top Brands")
        top_brands = filtered_df['company'].value_counts().head(10)

        fig_brand = px.bar(
            x=top_brands.index,
            y=top_brands.values,
            color=top_brands.values,
            title="Top Brands"
        )
        st.plotly_chart(fig_brand, use_container_width=True)

# =========================
# 💰 TAB 2: PRICING
# =========================
with tab2:

    st.subheader("💰 Real Price vs Offer Price")

    fig_price = px.scatter(
        filtered_df,
        x='real_price',
        y='offer_price',
        color='calculated_discount',
        hover_data=['company'] if 'company' in df.columns else None
    )
    st.plotly_chart(fig_price, use_container_width=True)

    st.subheader("📉 Price Correlation")

    corr_price = filtered_df[['real_price', 'offer_price', 'calculated_discount']].corr()

    fig_corr = px.imshow(corr_price, text_auto=True)
    st.plotly_chart(fig_corr, use_container_width=True)

# =========================
# ⭐ TAB 3: RATINGS
# =========================
with tab3:

    st.subheader("⭐ Ratings vs Discount")

    corr_rating = filtered_df[['ratings', 'calculated_discount']].corr()

    fig_rating = px.imshow(corr_rating, text_auto=True)
    st.plotly_chart(fig_rating, use_container_width=True)

    if 'feature_count' in df.columns:
        st.subheader("📊 Feature vs Ratings")

        feature_rating = filtered_df.groupby('feature_count')['ratings'].mean().reset_index()

        fig_feature = px.bar(
            feature_rating,
            x='feature_count',
            y='ratings',
            color='ratings'
        )
        st.plotly_chart(fig_feature, use_container_width=True)

    st.subheader("📊 Overall Correlation")

    corr_all = filtered_df.corr(numeric_only=True)

    fig_all = px.imshow(corr_all)
    st.plotly_chart(fig_all, use_container_width=True)

# =========================
# 📥 DOWNLOAD
# =========================
st.markdown("---")

st.download_button(
    label="📥 Download Filtered Data",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_data.csv",
    mime="text/csv"
)