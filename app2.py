import streamlit as st
from weather import get_weather
from rules2 import get_tomorrow_alert

# Page configuration
st.set_page_config(
    page_title="Crop Advisory",
    page_icon="🌾",
    layout="centered"
)

st.title("🌾 Crop Advisory System")
st.write("📍 Demo Location: Kumbakonam, Tamil Nadu")

# Crop Selection
crop = st.selectbox(
    "🌱 Select your Crop",
    ["Paddy", "Sugarcane", "Groundnut"]
)

# Fixed Location
lat = 10.9601
lon = 79.3788

# Fetch Weather
try:
    weather_data = get_weather(lat, lon)

    if weather_data and len(weather_data) >= 2:

        today_weather = weather_data[0]
        tomorrow_weather = weather_data[1]

        st.subheader("🌤 Today's Weather")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("🌡 Max Temperature", f"{today_weather['temp_max']} °C")

        with col2:
            st.metric("🌡 Min Temperature", f"{today_weather['temp_min']} °C")

        with col3:
            st.metric("🌧 Rainfall", f"{today_weather['rainfall_mm']} mm")

        st.divider()

        st.subheader("📢 Tomorrow's Crop Advisory")

        alert = get_tomorrow_alert(tomorrow_weather, crop)

        if "warning" in alert.lower():
            st.warning(alert)
        else:
            st.success(alert)

    else:
        st.error("Weather data not available.")

except Exception as e:
    st.error(f"Error: {e}")