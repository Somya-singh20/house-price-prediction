import streamlit as st
import pickle
import numpy as np

# Load model
model = pickle.load(open("house_price_model.pkl", "rb"))

# Page config
st.set_page_config(page_title="House Price Prediction", layout="centered")

# Header
st.markdown("<h1 style='text-align: center; font-weight: 600;'>🏡 House Price Prediction</h1>", unsafe_allow_html=True)
st.write("<p style='text-align:center; color:gray;'>Enter the details below to estimate the price</p>", unsafe_allow_html=True)
st.write("---")

# Two-column layout for compact inputs
col1, col2 = st.columns(2)

with col1:
    area = st.number_input("Area (sq ft)", min_value=0, step=1)
    bedrooms = st.number_input("Bedrooms", min_value=0, step=1)
    bathrooms = st.number_input("Bathrooms", min_value=0, step=1)
    stories = st.number_input("Stories", min_value=0, step=1)

with col2:
    parking = st.number_input("Parking", min_value=0, step=1)
    mainroad = st.selectbox("Near Main Road?", ["Select", "yes", "no"])
    guestroom = st.selectbox("Guest Room?", ["Select", "yes", "no"])
    basement = st.selectbox("Basement Present?", ["Select", "yes", "no"])
    hotwater = st.selectbox("Hot Water Heating?", ["Select", "yes", "no"])
    aircon = st.selectbox("Air Conditioning?", ["Select", "yes", "no"])
    furnish = st.selectbox("Furnishing", ["Select", "furnished", "semi-furnished", "unfurnished"])

st.write("---")

def yn_to_num(v):
    return 1 if v == "yes" else (0 if v == "no" else None)

if st.button("Predict Price 💰"):
    if (mainroad=="Select" or guestroom=="Select" or basement=="Select" or 
        hotwater=="Select" or aircon=="Select" or furnish=="Select"):
        st.warning("⚠️ Please fill all fields before predicting.")
    else:
        mainroad = yn_to_num(mainroad)
        guestroom = yn_to_num(guestroom)
        basement = yn_to_num(basement)
        hotwater = yn_to_num(hotwater)
        aircon = yn_to_num(aircon)

        furnished = 1 if furnish=="furnished" else 0
        semi_furnished = 1 if furnish=="semi-furnished" else 0

        features = np.array([[float(area), float(bedrooms), float(bathrooms), float(stories), float(parking),
                              mainroad, guestroom, basement, hotwater, aircon, 0, furnished, semi_furnished]])

        price = model.predict(features)[0]
        st.success(f"✅ Estimated Price: **₹ {price:,.2f}**")
