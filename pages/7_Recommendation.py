import streamlit as st
import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics.pairwise import cosine_similarity

# =========================
# 📦 LOAD DATA
# =========================
@st.cache_data
def load_data():
    df3 = pd.read_csv("C:\\Users\\DEEL\\dealio_major_project_final_folder\\updated_earphones_dataset.csv")
    df3.columns = df3.columns.str.strip()

    # 🔥 Fix duplicate names
    df3 = df3.drop_duplicates(subset='name')

    # Reset index
    df3 = df3.reset_index(drop=True)

    return df3

df3 = load_data()
df = df3   # ✅ Fix

# =========================
# 🧹 HANDLE MISSING VALUES (FIX FOR ERROR)
# =========================
numeric_cols = ['battery_hours', 'people_review', 'feature_count', 'ratings']
df[numeric_cols] = df[numeric_cols].fillna(0)

df['company'] = df['company'].fillna('Unknown')

# =========================
# 🧠 FEATURE SELECTION
# =========================
features = [
    'company',
    'battery_hours',
    'people_review',
    'feature_count',
    'ratings',
    'ANC',
    'ENC',
    'fast_charging'
]

X = df[features]

# =========================
# 🔄 PREPROCESSING
# =========================
numeric_features = ['battery_hours', 'people_review', 'feature_count', 'ratings']
categorical_features = ['company']

preprocessor = ColumnTransformer([
    ('num', StandardScaler(), numeric_features),
    ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
])

X_processed = preprocessor.fit_transform(X)

# =========================
# 🔗 SIMILARITY MATRIX
# =========================
similarity_matrix = cosine_similarity(X_processed)

# =========================
# 🔍 RECOMMEND FUNCTION
# =========================
def recommend_similar(phone_name, top_n=5):

    df_clean = df.copy()
    df_clean = df_clean.drop_duplicates(subset='name')
    df_clean = df_clean.reset_index(drop=True)

    if phone_name not in df_clean['name'].values:
        return pd.DataFrame()

    idx = df_clean[df_clean['name'] == phone_name].index[0]

    similarity_scores = list(enumerate(similarity_matrix[idx]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    top_indices = [i[0] for i in similarity_scores[1:top_n+1]]

    rec = df_clean.iloc[top_indices].copy()
    rec = rec.reset_index(drop=True)

    return rec

# =========================
# 🎨 UI
# =========================
st.title("📱 Similar Phone Recommendation System")

selected_phone = st.selectbox(
    "Select a Phone",
    df['name'].sort_values().unique()
)

top_n = st.slider("Number of Recommendations", 1, 10, 5)

# =========================
# 🚀 BUTTON
# =========================
if st.button("🔍 Find Similar Phones"):

    results = recommend_similar(selected_phone, top_n)

    if results.empty:
        st.error("No recommendations found")
    else:
        st.subheader("📊 Similar Phones")

        for _, row in results.iterrows():
            st.markdown(f"""
            <div style="
                background:#111827;
                padding:15px;
                border-radius:10px;
                margin-bottom:10px;
            ">
                <h4>{row['company']} - {row['name']}</h4>
                <p>💰 ₹ {row['offer_price']} | ⭐ {row['ratings']}</p>
                <p>🔋 Battery: {row['battery_hours']} hrs</p>
            </div>
            """, unsafe_allow_html=True)