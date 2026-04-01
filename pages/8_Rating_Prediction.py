import streamlit as st
import pandas as pd
import pickle


# =========================
# 📦 LOAD MODEL
# =========================
@st.cache_resource
def load_model():
    with open("rating_prediction_model1.pkl", "rb") as f:
        model = pickle.load(f)
    return model

model = load_model()

# =========================
# 🎨 CUSTOM CSS
st.markdown("""
<style>

body {
    background-color: #0e1117;
}

.stApp {
    background: linear-gradient(135deg, #0f172a, #020617);
    color: white;
}

/* Card */
.card {
    background: #111827;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 0px 20px rgba(0,0,0,0.4);
    margin-bottom: 20px;
}

/* Title */
.title {
    font-size: 32px;
    font-weight: bold;
    color: #38bdf8;
}

/* Button */
.stButton>button {
    background: linear-gradient(90deg, #22c55e, #16a34a);
    color: white;
    border-radius: 10px;
    padding: 10px 20px;
    border: none;
    font-weight: bold;
}

.stButton>button:hover {
    background: linear-gradient(90deg, #16a34a, #15803d);
}

/* Inputs */
.stTextInput input, .stNumberInput input {
    border-radius: 10px;
}

/* Slider */
.stSlider {
    padding-top: 10px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# 🎧 HEADER
# =========================
st.markdown('<div class="title">🎧 Earphone Rating Predictor</div>', unsafe_allow_html=True)
st.caption("Smart AI model to predict product ratings")

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

    fast_charging = st.radio("Fast Charging", ["Yes", "No"], horizontal=True)
    ENC = st.radio("ENC", ["Yes", "No"], horizontal=True)
    ANC = st.radio("ANC", ["Yes", "No"], horizontal=True)

with col2:
    feature_count = st.slider("Feature Count", 1, 20, 8)
    feature_score = st.slider("Feature Score", 0.0, 10.0, 7.0)
    value_score = st.slider("Value Score", 0.0, 10.0, 7.0)

    # 🔥 Fast input (typing instead of + -)
    offer_price = st.text_input("Offer Price (₹)", "1499")
    real_price = st.text_input("Real Price (₹)", "2999")

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# 🔮 PREDICTION
# =========================

if st.button("🚀 Predict Rating"):

    # Convert price safely
    try:
        offer_price = float(offer_price)
        real_price = float(real_price)
    except:
        st.error("❌ Please enter valid numeric price")
        st.stop()

    # Auto calculations
    offer = ((real_price - offer_price) / real_price) * 100 if real_price != 0 else 0
    calculated_discount = offer
    amount_saved = real_price - offer_price

    # Convert Yes/No
    fast_charging = 1 if fast_charging == "Yes" else 0
    ENC = 1 if ENC == "Yes" else 0
    ANC = 1 if ANC == "Yes" else 0

    # Create input
    input_data = pd.DataFrame([{
        'company': company,
        'color': color,
        'type': type_,
        'people_review': people_review,
        'offer_price': offer_price,
        'real_price': real_price,
        'offer': offer,
        'battery_hours': battery_hours,
        'fast_charging': fast_charging,
        'ENC': ENC,
        'ANC': ANC,
        'calculated_discount': calculated_discount,
        'amount_saved': amount_saved,
        'value_score': value_score,
        'feature__score': feature_score,
        'feature_count': feature_count
    }])

    try:
        prediction = model.predict(input_data)[0]

        st.markdown(f"""
        <div class="card">
            <h2 style="color:#22c55e;">⭐ Predicted Rating: {round(prediction,2)} / 5</h2>
        </div>
        """, unsafe_allow_html=True)

        st.progress(min(prediction / 5, 1.0))

        # Rating label
        if prediction >= 4:
            st.success("🔥 Excellent Product")
        elif prediction >= 3:
            st.warning("👍 Average Product")
        else:
            st.error("⚠️ Low Rated Product")

    except Exception as e:
        st.error("Prediction failed")
        st.write(e)
