import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="Recommendation System", layout="wide")

#  LOAD DATA

@st.cache_data
def load_data():
    df = pd.read_csv("C:\\Users\\DEEL\\dealio_major_project_final_folder\\smartphone_cleaned_v4.csv")
    df.columns = df.columns.str.strip()

    num_cols = [
        'price','rating','ram_capacity','battery_capacity',
        'internal_memory','screen_size','refresh_rate'
    ]

    # Convert to numeric
    for col in num_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Fill missing values
    df[num_cols] = df[num_cols].fillna(df[num_cols].median())

    # Value score
    df['value_score'] = df['rating'] / df['price']

    return df

df = load_data()

# CONTENT-BASED MODEL

features = [
    'price','ram_capacity','battery_capacity',
    'internal_memory','screen_size','refresh_rate','rating'
]

scaler = StandardScaler()
scaled_data = scaler.fit_transform(df[features])

similarity = cosine_similarity(scaled_data)

# TITLE

st.title(" Smartphone Recommendation System")

st.write("""
Find the best smartphone based on your needs.

✔ Best phones under budget  
✔ Value-for-money phones  
✔ Similar phone recommendations  
""")

st.markdown("---")

#  SIDEBAR

st.sidebar.header(" Filter Options")

budget = st.sidebar.slider("Budget (₹)", 5000, 150000, 20000)
ram = st.sidebar.selectbox("Minimum RAM (GB)", [2,4,6,8,12,16])
battery = st.sidebar.slider("Minimum Battery (mAh)", 2000, 7000, 5000)

recommend_type = st.sidebar.selectbox(
    "Recommendation Type",
    ["Smart (Best Overall)", "Value for Money", "Similar Phones"]
)

# FUNCTIONS


def smart_recommend(df, budget, ram, battery):
    filtered = df[
        (df['price'] <= budget) &
        (df['ram_capacity'] >= ram) &
        (df['battery_capacity'] >= battery)
    ].copy()

    if filtered.empty:
        return pd.DataFrame()

    filtered['value_score'] = filtered['rating'] / filtered['price']

    return filtered.sort_values(by='value_score', ascending=False).head(10)


def recommend_value(df, budget):
    filtered = df[df['price'] <= budget]

    if filtered.empty:
        return pd.DataFrame()

    return filtered.sort_values(by='value_score', ascending=False).head(10)


def recommend_similar(phone_name):
    matches = df[df['model'] == phone_name]

    if matches.empty:
        return pd.DataFrame()

    idx = matches.index[0]

    distances = list(enumerate(similarity[idx]))
    sorted_dist = sorted(distances, key=lambda x: x[1], reverse=True)

    indices = [i[0] for i in sorted_dist[1:6]]

    return df.iloc[indices].reset_index(drop=True)

#  OUTPUT


st.subheader("Results")

if recommend_type == "Smart (Best Overall)":

    result = smart_recommend(df, budget, ram, battery)

    if result.empty:
        st.warning(" No phones found. Try adjusting filters.")
    else:
        st.success("Top Recommended Phones")

        st.dataframe(
            result[['brand_name','model','price','rating','ram_capacity','battery_capacity']],
            use_container_width=True
        )


elif recommend_type == "Value for Money":

    result = recommend_value(df, budget)

    if result.empty:
        st.warning(" No phones found under this budget.")
    else:
        st.success(" Best Value Phones")

        st.dataframe(
            result[['brand_name','model','price','rating','value_score']],
            use_container_width=True
        )


elif recommend_type == "Similar Phones":

    phone_list = df['model'].dropna().drop_duplicates().values

    selected_phone = st.selectbox("Select a Phone", phone_list)

    if st.button("Find Similar Phones"):

        result = recommend_similar(selected_phone)

        if result.empty:
            st.warning(" No similar phones found.")
        else:
            st.success(" Similar Phones")

            st.dataframe(
                result[['brand_name','model','price','rating']],
                use_container_width=True
            )