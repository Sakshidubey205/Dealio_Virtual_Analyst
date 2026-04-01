import streamlit as st
import pandas as pd
import joblib


st.set_page_config(page_title="Price Prediction", layout="wide")

# LOAD MODEL

@st.cache_resource
def load_model():
    return joblib.load("price_model_smartphones2.pkl")

model = load_model()

# TITLE


st.title("Smartphone Price Prediction")

st.write("""
Predict the expected price of a smartphone based on its specifications.

This helps in:
- Understanding pricing strategy
- Comparing different configurations
- Identifying value-for-money devices
""")

st.markdown("---")

# INPUT SECTION

st.subheader("Enter Smartphone Details")

col1, col2 = st.columns(2)

with col1:
    ram = st.selectbox("RAM (GB)", [2,4,6,8,12,16])
    battery = st.slider("Battery Capacity (mAh)", 2000, 7000, 5000)
    screen = st.slider("Screen Size (inches)", 5.0, 7.0, 6.5)
    refresh = st.selectbox("Refresh Rate (Hz)", [60,90,120])

with col2:
    rear_cam = st.slider("Rear Camera (MP)", 8, 200, 50)
    front_cam = st.slider("Front Camera (MP)", 5, 50, 16)
    processor = st.selectbox("Processor Brand", ["snapdragon","mediatek","exynos"])
    os = st.selectbox("Operating System", ["android","ios"])

    has_5g = st.selectbox("5G Support", [0,1])
    has_nfc = st.selectbox("NFC", [0,1])
    has_ir = st.selectbox("IR Blaster", [0,1])
    fast_charging = st.selectbox("Fast Charging", [0,1])

#  PREDICTION

if st.button("Predict Price "):

    input_data = pd.DataFrame({
        'has_5g':[has_5g],
        'has_nfc':[has_nfc],
        'has_ir_blaster':[has_ir],
        'processor_brand':[processor],
        'num_cores':[8],
        'processor_speed':[2.5],
        'fast_charging_available':[fast_charging],
        'battery_capacity':[battery],
        'ram_capacity':[ram],
        'internal_memory':[128],
        'screen_size':[screen],
        'refresh_rate':[refresh],
        'num_rear_cameras':[rear_cam],
        'num_front_cameras':[front_cam],
        'os':[os]
    })

    prediction = model.predict(input_data)[0]

    st.success(f" Predicted Price: ₹ {round(prediction, 0)}")

    # Price Category
    if prediction < 15000:
        st.info("Budget Segment")
    elif prediction < 40000:
        st.info("⚖Mid-Range Segment")
    elif prediction < 80000:
        st.info("Premium Segment")
    else:
        st.info("Flagship Segment")