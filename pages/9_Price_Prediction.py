import streamlit as st
import pandas as pd
import numpy as np
import pickle

# =========================
# 📦 LOAD MODEL
# =========================
@st.cache_resource
def load_model():
    with open("earphones_price_prediction_model2.pkl", "rb") as f:
        model = pickle.load(f)
    return model

model = load_model()

# =========================
# 🎨 CSS
# =========================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #020617, #0f172a);
    color: white;
}

.card {
    background: #111827;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 20px;
    box-shadow: 0px 0px 20px rgba(0,0,0,0.4);
}

.title {
    font-size: 32px;
    font-weight: bold;
    color: #38bdf8;
}

.stButton>button {
    background: linear-gradient(90deg, #3b82f6, #2563eb);
    color: white;
    border-radius: 10px;
    padding: 10px 20px;
    border: none;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# =========================
# 🎧 HEADER
# =========================
st.markdown('<div class="title">💰 Earphone Price Predictor</div>', unsafe_allow_html=True)
st.caption("Predict ideal market price based on features")

# =========================
# 🧾 INPUT SECTION
# =========================

st.markdown('<div class="card">', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    company = st.selectbox("Company", ["boAt", "Realme", "Noise", "JBL", "OnePlus"])
    color = st.selectbox("Color", ["Black", "White", "Blue", "Red"])
    type_ = st.selectbox("Type", ["In-Ear", "On-Ear", "Over-Ear"])

    battery_hours = st.slider("Battery Hours", 1, 100, 20)
    people_review = st.number_input("Number of Reviews", min_value=0, value=1000, step=100)

with col2:
    fast_charging = st.radio("Fast Charging", ["Yes", "No"], horizontal=True)
    ENC = st.radio("ENC", ["Yes", "No"], horizontal=True)
    ANC = st.radio("ANC", ["Yes", "No"], horizontal=True)

    feature_count = st.slider("Feature Count", 1, 20, 8)
    feature_score = st.slider("Feature Score", 0.0, 10.0, 7.0)
    value_score = st.slider("Value Score", 0.0, 10.0, 7.0)

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# 🔮 PREDICTION
# =========================

if st.button("🚀 Predict Price"):

    # Convert Yes/No
    fast_charging = 1 if fast_charging == "Yes" else 0
    ENC = 1 if ENC == "Yes" else 0
    ANC = 1 if ANC == "Yes" else 0

    # Input dataframe (IMPORTANT: match training columns)
    input_data = pd.DataFrame([{
        'company': company,
        'color': color,
        'type': type_,
        'people_review': people_review,
        'battery_hours': battery_hours,
        'fast_charging': fast_charging,
        'ENC': ENC,
        'ANC': ANC,
        'value_score': value_score,
        'feature__score': feature_score,
        'feature_count': feature_count
    }])

    try:
        # Predict (log scale → convert back)
        pred_log = model.predict(input_data)[0]
        prediction = np.expm1(pred_log)

        # Safety clamp
        prediction = max(0, prediction)

        st.markdown(f"""
        <div class="card">
            <h2 style="color:#3b82f6;">💰 Predicted Price: ₹ {round(prediction, 2)}</h2>
        </div>
        """, unsafe_allow_html=True)

        # Price category
        if prediction < 1000:
            st.success("🟢 Budget Segment")
        elif prediction < 3000:
            st.info("🔵 Mid-Range Product")
        else:
            st.warning("🟣 Premium Product")

    except Exception as e:
        st.error("Prediction failed")
        st.write(e)