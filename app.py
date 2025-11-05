import streamlit as st
import pickle
import numpy as np

# Load model
model = pickle.load(open("house_price_model.pkl", "rb"))

# Page Config
st.set_page_config(page_title="House Price Prediction", layout="wide")

# Glassmorphism Background CSS
st.markdown("""
<style>
body {
  background: linear-gradient(135deg, #1D2B64, #F8CDDA);
  font-family: 'Poppins', sans-serif;
}
.card {
  background: rgba(255, 255, 255, 0.12);
  border-radius: 18px;
  padding: 30px;
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.25);
  margin-top: 30px;
}
.title {
  text-align:center;
  font-size:42px;
  font-weight:700;
  color:white;
}
.sub {
  text-align:center;
  font-size:18px;
  color:#EEEEEE;
  margin-bottom:25px;
}
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("<div class='title'>🏡 House Price Prediction</div>", unsafe_allow_html=True)
st.markdown("<div class='sub'>Enter the property details below</div>", unsafe_allow_html=True)

# Card Container
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        area = st.text_input("Area (sq ft)")
        bedrooms = st.text_input("Bedrooms")
        bathrooms = st.text_input("Bathrooms")
        stories = st.text_input("Stories")

    with col2:
        parking = st.text_input("Parking")
        mainroad = st.selectbox("Near Main Road?", ["Select","yes","no"])
        guestroom = st.selectbox("Guest Room?", ["Select","yes","no"])
        basement = st.selectbox("Basement Present?", ["Select","yes","no"])
        hotwater = st.selectbox("Hot Water Heating?", ["Select","yes","no"])
        aircon = st.selectbox("Air Conditioning?", ["Select","yes","no"])
        furnish = st.selectbox("Furnishing", ["Select","furnished","semi-furnished","unfurnished"])

    st.markdown("</div>", unsafe_allow_html=True)

def yn_to_num(val):
    return 1 if val=="yes" else (0 if val=="no" else None)

if st.button("🔍 Predict Price", use_container_width=True):
    if (not area or not bedrooms or not bathrooms or not stories or not parking or
        mainroad=="Select" or guestroom=="Select" or basement=="Select" or
        hotwater=="Select" or aircon=="Select" or furnish=="Select"):

        st.warning("⚠️ Please provide all inputs before predicting.")
    else:
        mainroad = yn_to_num(mainroad)
        guestroom = yn_to_num(guestroom)
        basement = yn_to_num(basement)
        hotwater = yn_to_num(hotwater)
        aircon = yn_to_num(aircon)

        furnished = 1 if furnish == "furnished" else 0
        semi_furnished = 1 if furnish == "semi-furnished" else 0

        features = np.array([[float(area), float(bedrooms), float(bathrooms), float(stories), float(parking),
                              mainroad, guestroom, basement, hotwater, aircon, 0, furnished, semi_furnished]])

        price = model.predict(features)[0]

        st.success(f"💰 Estimated House Price: **₹ {price:,.2f}**")
