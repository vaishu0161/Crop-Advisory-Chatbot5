import streamlit as st
from weather import get_weather
from rules2 import get_tomorrow_alert
from ai import ask_ai

# Page configuration
st.set_page_config(
    page_title="Crop Advisory Chatbot",
    page_icon="🌾",
    layout="centered"
)

st.title("🌾 AI Crop Advisory Chatbot")
st.write("📍 Demo Location: Kumbakonam, Tamil Nadu")

# Crop selection
crop = st.selectbox(
    "🌱 Select your crop",
    ["Paddy", "Sugarcane", "Groundnut"]
)

# Fixed location (Kumbakonam)
lat = 10.9601
lon = 79.3788

# Fetch weather only once
if "weather_data" not in st.session_state:
    st.session_state.weather_data = get_weather(lat, lon)

weather_data = st.session_state.weather_data

if weather_data:

    today_weather = weather_data[0]
    tomorrow_weather = weather_data[1]

    # Today's Weather
    st.subheader("🌤 Today's Weather")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Max Temp", f"{today_weather['temp_max']} °C")

    with col2:
        st.metric("Min Temp", f"{today_weather['temp_min']} °C")

    with col3:
        st.metric("Rainfall", f"{today_weather['rainfall_mm']} mm")

    st.divider()

    # Tomorrow Alert
    st.subheader("📢 Tomorrow's Alert")

    alert = get_tomorrow_alert(tomorrow_weather, crop)
    st.warning(alert)

    st.divider()

    # Chatbot
    st.subheader("💬 Ask the AI Crop Advisor")

    question = st.text_input(
        "Ask your farming question",
        placeholder="Example: Should I irrigate today?"
    )

    if st.button("Ask"):

        if question.strip() == "":
            st.warning("Please enter a question.")

        else:
            with st.spinner("Thinking..."):
                answer = ask_ai(question, today_weather, crop)

            with st.chat_message("user"):
                st.write(f"🌱 Crop: {crop}")
                st.write(question)

            with st.chat_message("assistant"):
                st.write(answer)

else:
    st.error("Unable to fetch weather data. Please try again later.")