import streamlit as st
import pickle
import numpy as np

# Load trained model
model = pickle.load(open("house_price_model.pkl", "rb"))

st.set_page_config(page_title="House Price Prediction", layout="centered")

st.markdown("""
<style>
    .title {text-align: center; font-size: 38px; color: #00E3FF; font-weight: bold;}
    .sub {text-align: center; color: #CCCCCC; font-size: 16px;}
    .container {padding: 20px; border-radius: 12px; background-color: #1C1F26;}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>🏡 House Price Prediction</div>", unsafe_allow_html=True)
st.markdown("<div class='sub'>Enter house details to get the estimated price</div>", unsafe_allow_html=True)

with st.container():
    st.write("")

    area = st.text_input("Area (sq ft)")
    bedrooms = st.text_input("Bedrooms")
    bathrooms = st.text_input("Bathrooms")
    stories = st.text_input("Stories")
    parking = st.text_input("Parking")

    mainroad = st.selectbox("Near Main Road?", ["Select", "yes", "no"])
    guestroom = st.selectbox("Guest Room Available?", ["Select", "yes", "no"])
    basement = st.selectbox("Basement Present?", ["Select", "yes", "no"])
    hotwater = st.selectbox("Hot Water Heating?", ["Select", "yes", "no"])
    aircon = st.selectbox("Air Conditioning?", ["Select", "yes", "no"])
    prefarea = st.selectbox("Preferred Area?", ["Select", "yes", "no"])
    furnish = st.selectbox("Furnishing Status", ["Select","furnished", "semi-furnished", "unfurnished"])

def yes_no(val):
    if val == "yes": return 1
    elif val == "no": return 0
    return None

if st.button("Predict Price 💰"):
    # ✅ Validation: User must provide all values
    if (not area or not bedrooms or not bathrooms or not stories or not parking or
        mainroad == "Select" or guestroom == "Select" or basement == "Select" or 
        hotwater == "Select" or aircon == "Select" or prefarea == "Select" or furnish == "Select"):
        st.warning("⚠️ Please fill all fields before predicting.")
    else:
        mainroad = yes_no(mainroad)
        guestroom = yes_no(guestroom)
        basement = yes_no(basement)
        hotwater = yes_no(hotwater)
        aircon = yes_no(aircon)
        prefarea = yes_no(prefarea)

        furnished = 1 if furnish == "furnished" else 0
        semi_furnished = 1 if furnish == "semi-furnished" else 0

        features = np.array([[float(area), float(bedrooms), float(bathrooms), float(stories), float(parking),
                              mainroad, guestroom, basement, hotwater, aircon, prefarea,
                              furnished, semi_furnished]])

        price = model.predict(features)[0]

        st.success(f"💵 Estimated House Price: **₹ {price:,.2f}**")
