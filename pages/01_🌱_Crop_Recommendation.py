import streamlit as st
import os
from dotenv import load_dotenv
from logic import get_crop_recommendation, get_ai_explanation, get_weather_data
from utils import apply_custom_style, t 

load_dotenv()

st.set_page_config(page_title=t('crop_doc'), page_icon="🌱", layout="wide")
# --- LOAD BACKGROUND IMAGE ---
import os
import base64

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

bg_img_path = os.path.join("assets", "bg_crop_rec.png")
if os.path.exists(bg_img_path):
    bin_str = get_base64_of_bin_file(bg_img_path)
    bg_image_css = f"""
    [data-testid="stAppViewContainer"], .stApp {{
        background: linear-gradient(rgba(0, 0, 0, 0.2), rgba(0, 0, 0, 0.4)), url("data:image/png;base64,{bin_str}") no-repeat center center fixed !important;
        background-size: cover !important;
        background-attachment: fixed !important;
    }}
    """
else:
    bg_image_css = ""

apply_custom_style()

# --- CSS INJECTION FOR VISIBILITY ---
st.markdown(f"""
<style>
/* 1. Background Injection */
{bg_image_css}

/* Hide Default Canvas */
#bg-canvas {{
    display: none !important;
}}

/* 2. Text Visibility - FORCE WHITE with STRONG SHADOW and BOLD */
h1, h2, h3, h4, p, span, label, div, .stMarkdown, .stText {{
    color: #ffffff !important;
    text-shadow: 0 2px 4px #000000 !important; /* Strong dark shadow */
    font-weight: 800 !important; /* Bold */
}}

/* 3. Input Fields - BLACK TEXT for Readability */
.stTextInput input, .stNumberInput input {{
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    font-weight: 700 !important;
    background-color: rgba(255, 255, 255, 0.8) !important;
}}

/* 4. Glass Containers */
.glass-container {{
    background: rgba(255, 255, 255, 0.1) !important;
    backdrop-filter: blur(12px) !important;
    border-radius: 20px;
    padding: 25px;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3) !important;
    margin-bottom: 20px;
}}

/* 5. Result Cards - Styling */
.result-card {{
    background: white !important;
    border-radius: 12px !important;
    padding: 20px !important;
    margin-bottom: 15px !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
}}
.result-card-white {{
    background: linear-gradient(135deg, #43A047, #66BB6A) !important;
    color: #ffffff !important;
    text-shadow: 0 2px 4px rgba(0,0,0,0.3) !important;
}}
.result-card-white * {{
    color: #ffffff !important;
}}
.result-text-black {{
    color: #000000 !important;
    text-shadow: none !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    line-height: 1.5;
}}
.result-label {{
    color: #333 !important;
    font-weight: 800 !important;
    font-size: 1.1rem !important;
    margin-bottom: 5px;
}}

/* 6. Success/Weather Status - Bigger Font & White */
.stAlert, .stAlert p, [data-testid="stNotificationContent"] {{
    font-size: 1.5rem !important;
    font-weight: 800 !important;
    color: #ffffff !important; 
    text-shadow: 0 1px 2px rgba(0,0,0,0.5) !important;
}}
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown(f"""
<div class="header-card" style="padding: 30px 20px; margin-bottom: 30px; text-align: center;">
    <div style="display: inline-block; background: rgba(255, 255, 255, 0.15); border-radius: 50%; padding: 20px; backdrop-filter: blur(5px); border: 1px solid rgba(255,255,255,0.3); box-shadow: 0 0 25px rgba(74, 175, 80, 0.4); margin-bottom: 15px;">
        <img src="https://cdn-icons-png.flaticon.com/512/6065/6065094.png" width="90" style="filter: drop-shadow(0 4px 6px rgba(0,0,0,0.3)); display: block;">
    </div>
    <h1 style="font-size: 3rem; margin:0; color: #ffffff; text-shadow: 0 3px 6px #000000; font-weight: 900;">{t('crop_title').replace('🌱', '').strip()}</h1>
    <p style="color: #f0f0f0; font-size: 1.2rem; margin-top:10px; font-weight: 600; text-shadow: 0 2px 4px #000;">{t('tagline')}</p>
</div>
""", unsafe_allow_html=True)

# Two Columns: Inputs & Results
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown(f'<div class="glass-container"><h3 style="color:white; margin-bottom: 15px;">🧪 {t("soil_health")}</h3>', unsafe_allow_html=True)
    
    c_n, c_p = st.columns(2)
    with c_n: n = st.number_input(t('nitrogen'), 0, 200, 90)
    with c_p: p = st.number_input(t('phosphorus'), 0, 200, 42)
    
    c_k, c_ph = st.columns(2)
    with c_k: k = st.number_input(t('potassium'), 0, 200, 43)
    with c_ph: ph = st.number_input(t('ph_level'), 0.0, 14.0, 6.5, step=0.1)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(f'<div class="glass-container"><h3 style="color:white; margin-bottom: 15px;">☁️ {t("fet_weather")}</h3>', unsafe_allow_html=True)
    
    # City input logic
    default_city = t('nagpur')
    if 'active_user' in st.session_state and st.session_state.active_user:
        default_city = st.session_state.active_user.get('city', t('nagpur'))
        
    city = st.text_input(t('city'), value=default_city)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button(t('fetch_weather'), use_container_width=True):
        api_key = os.getenv("WEATHER_API_KEY")
        weather_lang = st.session_state.get('language', 'English')
        weather_data, error = get_weather_data(city, api_key, language=weather_lang)
        if weather_data:
            st.session_state['weather_data'] = weather_data
            st.session_state['weather_fetched'] = True
            st.markdown(f"<p style='color: #4CAF50; font-weight: 800; font-size: 1.2rem; text-shadow: 0 2px 4px rgba(0,0,0,0.5);'>✅ {city}: {weather_data['main']['temp']}°C, {weather_data['weather'][0]['description']}</p>", unsafe_allow_html=True)
            if weather_data.get("mock"):
                st.markdown(f"<p style='color: #FF9800; font-weight: 800; font-size: 1.1rem; text-shadow: 0 2px 4px rgba(0,0,0,0.5);'>{t('simulated_warn')}</p>", unsafe_allow_html=True)
        else:
            st.markdown(f"<p style='color: #F44336; font-weight: 800; font-size: 1.2rem; text-shadow: 0 2px 4px rgba(0,0,0,0.5);'>{t('weather_err')}: {error}</p>", unsafe_allow_html=True)
            
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown(f'<div class="glass-container"><h3 style="color:white; margin-bottom: 15px;">🔮 {t("results")}</h3>', unsafe_allow_html=True)
    
    if st.button(t('predict_btn'), type="primary", use_container_width=True):
        # Check if we have weather data
        weather = st.session_state.get('weather_data')
        if not weather:
            st.markdown(f"<p style='color: #FF9800; font-weight: 800; font-size: 1.1rem; text-shadow: 0 2px 4px rgba(0,0,0,0.5);'>{t('weather_err')}</p>", unsafe_allow_html=True)
        else:
            temp = weather['main']['temp']
            humidity = weather['main']['humidity']
            rainfall = 200 if "rain" in weather.get("weather", [{}])[0].get("description", "").lower() else 100 
            
            lang = st.session_state.get('language', 'English')
            crop, reason = get_crop_recommendation(n, p, k, temp, humidity, ph, rainfall, language=lang)
            ai_explanation = get_ai_explanation(crop, n, p, k, temp, humidity, ph, rainfall, language=lang)

            # Premium Result Display using utils.py classes
            st.markdown(f"""
            <div class="result-card result-card-white">
                <div style="font-size: 1.1rem; opacity: 0.9;">{t('best_crop')}</div>
                <div style="font-size: 2.5rem; font-weight: 800;">{crop}</div>
                <div style="font-size: 0.9rem; margin-top: 5px;">{t('highly_suitable')}</div>
            </div>
            
            <div class="result-card" style="border-left: 6px solid #FFC107;">
                <div class="result-label">💡 {t('logic_title')}</div>
                <div class="result-text-black">{reason}</div>
            </div>
            
            <div class="result-card" style="border-left: 6px solid #2196F3;">
                <div class="result-label">🧠 {t('ai_reasoning')}</div>
                <div class="result-text-black">{ai_explanation}</div>
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown("</div>", unsafe_allow_html=True)

    # VIEW RAW API RESPONSE
    if st.session_state.get('weather_data'):
        with st.expander(t('view_raw')):
            st.json(st.session_state['weather_data'])
