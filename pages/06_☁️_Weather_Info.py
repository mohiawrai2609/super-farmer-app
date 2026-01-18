import streamlit as st
import os, requests
from dotenv import load_dotenv
from utils import apply_custom_style, t, render_bottom_nav, init_session
from logic import get_weather_data

# Init Session
init_session()
from datetime import datetime

load_dotenv()
st.set_page_config(page_title=t('weather_det'), page_icon="☁️", layout="wide")
apply_custom_style()

# --- HEADER (Vision Pro Style) ---
st.markdown(f"""
<div class="header-card" style="padding: 40px; margin-bottom: 30px;">
    <div style="display:flex; justify-content:center; align-items:center; gap:20px;">
        <img src="https://img.icons8.com/3d-fluency/512/partly-cloudy-day.png" width="80">
        <div>
            <h1 style="font-size: 2.5rem; margin:0;">{t('weather_det')}</h1>
            <p style="color: #E0E0E0; font-size: 1.1rem; margin:0;">{t('weather_forecast')}</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- CSS INJECTION FOR WEATHER CARDS ---
st.markdown("""
<style>
/* Main Weather Hero Card */
.weather-hero {
    background: linear-gradient(135deg, #1E88E5, #42A5F5);
    border-radius: 30px;
    padding: 30px;
    color: white;
    box-shadow: 0 15px 35px rgba(33, 150, 243, 0.3);
    text-align: center;
    position: relative;
    overflow: hidden;
}
.hero-temp {
    font-size: 5rem;
    font-weight: 800;
    margin: 10px 0;
    text-shadow: 0 5px 15px rgba(0,0,0,0.2);
}
.hero-city {
    font-size: 1.8rem;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
}
.hero-desc {
    font-size: 1.4rem;
    opacity: 0.9;
    background: rgba(255,255,255,0.2);
    padding: 5px 15px;
    border-radius: 20px;
    display: inline-block;
}

/* Glass Metric Cards */
.metric-glass {
    background: rgba(255, 255, 255, 0.7);
    border-radius: 20px;
    padding: 20px;
    text-align: center;
    border: 1px solid rgba(255, 255, 255, 0.5);
    box-shadow: 0 5px 15px rgba(0,0,0,0.05);
}
.metric-label {
    font-size: 0.9rem;
    color: #555;
    font-weight: 600;
    text-transform: uppercase;
}
.metric-value {
    font-size: 1.8rem;
    font-weight: 700;
    color: #333;
}
</style>
""", unsafe_allow_html=True)

# --- SEARCH BAR ---
col_search, _ = st.columns([1, 2])
with col_search:
    st.markdown(f"### {t('select_loc')}")
    default_city = t('nagpur')
    if 'active_user' in st.session_state and st.session_state.active_user:
         default_city = st.session_state.active_user.get('city', t('nagpur'))
    city = st.text_input(t('city'), value=default_city, label_visibility="collapsed")

api_key = os.getenv("WEATHER_API_KEY")

if city:
    weather_lang = st.session_state.get('language', 'English')
    data, error = get_weather_data(city, api_key, language=weather_lang)
    
    if data:
        main = data['main']
        weather = data['weather'][0]
        wind = data['wind']
        
        # --- HERO SECTION ---
        col_hero, col_metrics = st.columns([1, 1], gap="large")
        
        with col_hero:
            icon_url = f"http://openweathermap.org/img/wn/{weather['icon']}@4x.png"
            # Fallback icon if URL fails or for aesthetic
            # We use a nice CSS gradient card
            st.markdown(f"""
            <div class="weather-hero">
                <div class="hero-city">📍 {city}</div>
                <div class="hero-temp">{main['temp']}°<span style="font-size:2rem;">C</span></div>
                <div class="hero-desc">{weather['description'].title()}</div>
                <div style="margin-top:15px; font-size:1rem; opacity:0.8;">{t('feels_like')} {main['feels_like']}°C</div>
            </div>
            """, unsafe_allow_html=True)

        with col_metrics:
            st.markdown(f"### {t('cond_details')}")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"""
                <div class="metric-glass" style="margin-bottom:20px;">
                    <div class="metric-label">💧 {t('humidity')}</div>
                    <div class="metric-value">{main['humidity']}%</div>
                </div>
                
                <div class="metric-glass">
                    <div class="metric-label">💨 {t('wind_speed')}</div>
                    <div class="metric-value">{wind['speed']} m/s</div>
                </div>
                """, unsafe_allow_html=True)
                
            with c2:
                st.markdown(f"""
                <div class="metric-glass" style="margin-bottom:20px;">
                    <div class="metric-label">🌡️ {t('max_temp')}</div>
                    <div class="metric-value">{main['temp_max']}°C</div>
                </div>
                
                <div class="metric-glass">
                    <div class="metric-label">🧊 {t('min_temp')}</div>
                    <div class="metric-value">{main['temp_min']}°C</div>
                </div>
                """, unsafe_allow_html=True)
        
    else:
        st.error(f"{t('err_weather_fetch')} {city}")
        if data is None and "API Key" in str(error): # Simulate if key missing 
             # Fallback Simulation Interface
             st.warning(t('simulated_data_warn'))
             st.markdown(f"""
            <div class="weather-hero" style="background: linear-gradient(135deg, #78909C, #90A4AE);">
                <div class="hero-city">📍 {city} {t('simulated_text')}</div>
                <div class="hero-temp">28°<span style="font-size:2rem;">C</span></div>
                <div class="hero-desc">{t('partly_cloudy')}</div>
            </div>
            """, unsafe_allow_html=True)

render_bottom_nav(active_tab='Weather')
st.markdown("<br><br><br>", unsafe_allow_html=True)
