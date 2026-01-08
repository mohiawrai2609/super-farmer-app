import streamlit as st
import os
import requests
from dotenv import load_dotenv
from logic import get_crop_recommendation, get_ai_explanation, get_weather_data
from utils import apply_custom_style, t 

load_dotenv()

st.set_page_config(page_title="Crop Recommendation", page_icon="🌱", layout="wide")
apply_custom_style()

# --- UI LAYOUT ---
st.markdown(f"## {t('crop_title')}")
st.write(f"ℹ️ *{t('tagline')}*")

# Two Columns: Inputs & Results
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown(f"### {t('soil_health')}")
    n = st.number_input(t('nitrogen'), 0, 200, 90)
    p = st.number_input(t('phosphorus'), 0, 200, 42)
    k = st.number_input(t('potassium'), 0, 200, 43)
    ph = st.number_input(t('ph_level'), 0.0, 14.0, 6.5, step=0.1)

    st.markdown(f"### {t('fet_weather')}")
    # City input
    default_city = "Nagpur"
    if 'active_user' in st.session_state and st.session_state.active_user:
        default_city = st.session_state.active_user.get('city', "Nagpur")
        
    city = st.text_input(t('city'), value=default_city)

    if st.button(t('fetch_weather')):
        api_key = os.getenv("WEATHER_API_KEY")
        weather_data, error = get_weather_data(city, api_key)
        if weather_data:
            st.session_state['weather_data'] = weather_data
            st.session_state['weather_fetched'] = True
            st.success(f"✅ {city}: {weather_data['main']['temp']}°C, {weather_data['weather'][0]['description']}")
            # Show simulated warning if applicable
            if weather_data.get("mock"):
                st.warning(t('simulated_warn'))
        else:
            st.error(f"{t('weather_err')}: {error}")

with col2:
    st.markdown(f"### {t('results')}")
    
    if st.button(t('predict_btn'), type="primary"):
        # Check if we have weather data
        weather = st.session_state.get('weather_data')
        if not weather:
            st.warning(t('weather_err'))
        else:
            temp = weather['main']['temp']
            humidity = weather['main']['humidity']
            # Simple rainfall assumption
            rainfall = 200 if "rain" in weather.get("weather", [{}])[0].get("description", "").lower() else 100 
            
            crop, reason = get_crop_recommendation(n, p, k, temp, humidity, ph, rainfall)
            
            # Smart AI Explanation
            ai_explanation = get_ai_explanation(crop, n, p, k, temp, humidity, ph, rainfall)

            st.success(f"## {t('best_crop')} {crop}")
            st.info(f"💡 {reason}")
            
            st.markdown(f"### {t('ai_reasoning')}")
            st.write(ai_explanation)

    # VIEW RAW API RESPONSE
    if st.session_state.get('weather_data'):
        with st.expander(t('view_raw')):
            st.json(st.session_state['weather_data'])
