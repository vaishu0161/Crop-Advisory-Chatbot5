import streamlit as st
from weather import get_weather
from rules2 import get_tomorrow_alert

# -----------------------------
# Rule-Based Chatbot
# -----------------------------
def answer_question(question, crop, weather):
    q = question.lower()

    if "irrigat" in q or "water" in q:
        if weather["rainfall_mm"] > 5:
            return "🌧 Rain is expected. Avoid irrigation today."
        else:
            return "💧 Irrigation is recommended if the soil is dry."

    elif "fertilizer" in q or "fertiliser" in q:
        return f"🌱 Apply fertilizer as per the recommended schedule for {crop}. Avoid applying before heavy rain."

    elif "pest" in q or "insect" in q:
        return "🐛 Regularly inspect your field. If pests are found, use the recommended pesticide for your crop."

    elif "temperature" in q or "temp" in q:
        return f"🌡 Today's maximum temperature is {weather['temp_max']}°C and minimum is {weather['temp_min']}°C."

    elif "rain" in q:
        return f"🌧 Expected rainfall: {weather['rainfall_mm']} mm."

    elif "crop" in q:
        return f"🌾 Selected crop: {crop}."

    else:
        return (
            "I can answer questions about:\n"
            "- Irrigation\n"
            "- Rainfall\n"
            "- Temperature\n"
            "- Fertilizer\n"
            "- Pest control"
        )


# -----------------------------
# Streamlit App
# -----------------------------
st.set_page_config(
    page_title="Crop Advisory System",
    page_icon="🌾",
    layout="centered"
)

st.title("🌾 Crop Advisory System")
st.write("📍 Demo Location: Kumbakonam, Tamil Nadu")

crop = st.selectbox(
    "🌱 Select your Crop",
    ["Paddy", "Sugarcane", "Groundnut"]
)

lat = 10.9601
lon = 79.3788

weather_data = get_weather(lat, lon)

if weather_data and len(weather_data) >= 2:

    today = weather_data[0]
    tomorrow = weather_data[1]

    st.subheader("🌤 Today's Weather")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Max Temp", f"{today['temp_max']} °C")

    with c2:
        st.metric("Min Temp", f"{today['temp_min']} °C")

    with c3:
        st.metric("Rainfall", f"{today['rainfall_mm']} mm")

    st.divider()

    st.subheader("📢 Tomorrow's Advisory")
    st.info(get_tomorrow_alert(tomorrow, crop))

    st.divider()

    # Rule-based chatbot
    st.subheader("💬 Ask a Farming Question")

    question = st.text_input(
        "Type your question",
        placeholder="Example: Should I irrigate today?"
    )

    if st.button("Ask"):
        if question.strip():
            answer = answer_question(question, crop, today)

            with st.chat_message("user"):
                st.write(question)

            with st.chat_message("assistant"):
                st.write(answer)
        else:
            st.warning("Please enter a question.")

else:
    st.error("Unable to fetch weather data.")