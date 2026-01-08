import streamlit as st
import os, requests
from dotenv import load_dotenv
from utils import apply_custom_style, t
from logic import get_weather_data
from datetime import datetime

load_dotenv()
st.set_page_config(page_title="Weather Info", page_icon="☁️", layout="wide")
apply_custom_style()

st.title(f"☁️ {t('weather_det')}")

col1, _ = st.columns([1, 2])
with col1:
    default_city = "Nagpur"
    if 'active_user' in st.session_state and st.session_state.active_user:
         default_city = st.session_state.active_user.get('city', "Nagpur")
    city = st.text_input(t('city'), value=default_city)

api_key = os.getenv("WEATHER_API_KEY")

if city:
    data, error = get_weather_data(city, api_key)
    if data:
        # Layout Weather Card
        st.markdown(f"### {city}")
        
        main = data['main']
        weather = data['weather'][0]
        wind = data['wind']
        
        col_w1, col_w2, col_w3 = st.columns(3)
        with col_w1:
            st.metric("Temperature", f"{main['temp']}°C", f"Feels like {main['feels_like']}°C")
        with col_w2:
            st.metric("Humidity", f"{main['humidity']}%")
        with col_w3:
             st.metric("Wind Speed", f"{wind['speed']} m/s")
        
        st.info(f"**Condition:** {weather['description'].title()}")
    else:
        if "API Key not configured" in str(error):
            st.warning("⚠️ Real-time data unavailable. Showing **SIMULATED** data because API Key is missing.")
            st.markdown("To get real data: [Get Free Key](https://openweathermap.org/api) and add to `.env` file as `WEATHER_API_KEY`.")
        else:
             st.error(f"❌ Error fetching data: {error}")
             st.info("Showing simulated data for demonstration:")
             
        # Fallback Simulation
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Temperature (Simulated)", value="28°C", delta="2°C")
        with col2:
            st.metric(label="Humidity (Simulated)", value="65%", delta="-5%")
