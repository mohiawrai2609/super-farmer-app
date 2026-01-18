import streamlit as st
import pandas as pd
from logic import get_yield_prediction
from utils import apply_custom_style, t, render_bottom_nav

st.set_page_config(page_title=t('yield_pred'), page_icon="📊", layout="wide")

# --- LOAD BACKGROUND IMAGE ---
import os
import base64

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

bg_img_path = os.path.join("assets", "bg_yield_green.png")
if os.path.exists(bg_img_path):
    bin_str = get_base64_of_bin_file(bg_img_path)
    bg_image_css = f"""
    [data-testid="stAppViewContainer"], .stApp {{
        background: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.6)), url("data:image/png;base64,{bin_str}") no-repeat center center fixed !important;
        background-size: cover !important;
        background-attachment: fixed !important;
    }}
    """
else:
    bg_image_css = ""

apply_custom_style()

# --- CSS INJECTION FOR VISIBILITY ---
st.markdown("""
<style>
/* 1. Background Injection */
""" + bg_image_css + """

/* Hide Default Canvas */
#bg-canvas {
    display: none !important;
}

/* 2. Text Visibility - FORCE WHITE with STRONG SHADOW and BOLD */
h1, h2, h3, h4, p, span, label, div, .stMarkdown, .stText {
    color: #ffffff !important;
    text-shadow: 0 2px 4px #000000 !important; /* Strong dark shadow */
    font-weight: 800 !important; /* Bold */
}

/* 3. Input Fields & Containers */
/* Make input labels easier to read */
.stTextInput label, .stNumberInput label, .stSelectbox label, .stDateInput label, .stFileUploader label {
    font-size: 1rem !important;
    font-weight: 600 !important;
    /* Background removed as requested */
}

/* Force Input Text inside the boxes to be BLACK */
.stTextInput input, .stNumberInput input, .stDateInput input {
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    caret-color: #000000 !important;
    text-shadow: none !important;
    font-weight: 600 !important;
    background-color: rgba(255, 255, 255, 0.8) !important; /* Ensure background is light */
}

/* Selectbox Selected Value & Arrow */
div[data-baseweb="select"] div {
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    text-shadow: none !important;
}
div[data-baseweb="select"] svg {
    fill: #000000 !important;
    color: #000000 !important;
}

/* 4. Result/Success Messages */
/* Ensure Success/Error/Info boxes are readable (they rely on alerting colors, so we might need to be careful) */
.stAlert {
    background-color: rgba(255, 255, 255, 0.95) !important;
    color: #333 !important; /* Force black text inside alerts for readability */
}
.stAlert p, .stAlert h3, .stAlert div, .stAlert strong {
    color: #333 !important; /* Override the global white force for alerts */
    text-shadow: none !important;
}

/* 5. Expander Header Styling - SUPER FORCE HUGE */
[data-testid="stExpander"] summary p, 
[data-testid="stExpander"] summary span, 
[data-testid="stExpander"] summary {
    font-size: 2.2rem !important; /* Extremely Large */
    font-weight: 900 !important;
    color: #ffffff !important;
    text-shadow: 0 4px 8px #000000 !important;
}
[data-testid="stExpander"] svg {
    width: 2.5rem !important;
    height: 2.5rem !important;
    stroke-width: 3px !important;
}

</style>
""", unsafe_allow_html=True)

# Centered Header with New Logo
st.markdown(f"""
<div style="text-align: center; margin-bottom: 20px; padding: 20px;">
    <img src="https://cdn-icons-png.flaticon.com/512/3058/3058995.png" width="90" style="filter: drop-shadow(0 4px 6px rgba(0,0,0,0.5)); margin-bottom: 15px;">
    <h1 style="color: #ffffff; text-shadow: 0 3px 6px #000000; font-weight: 900; margin: 0; font-size: 3rem;">{t('yield_title').replace('📊', '').strip()}</h1>
    <p style="color: #ffffff; text-shadow: 0 2px 4px #000000; font-size: 1.3rem; font-weight: 700; margin-top: 10px;">{t('yield_desc')}</p>
</div>
""", unsafe_allow_html=True)

# Static Lists
states = [t('st_mh'), t('st_pb'), t('st_up'), t('st_gj'), t('st_hr'), t('st_mp'), t('st_ka'), t('st_wb'), t('st_br'), t('st_rj'), t('st_ap'), t('st_tg'), t('st_tn'), t('st_od'), t('st_ot')]
seasons = [t('season_kharif'), t('season_rabi'), t('season_zaid'), t('season_year')]

# Sidebar Filters Removed - Moved to main page
st.markdown(f"### ⚙️ {t('select_param')}")

# 1. Location Details
col1, col2, col3 = st.columns(3)
with col1:
    selected_state = st.selectbox(t('location'), states)
with col2:
    city = st.text_input(t('district_city'), placeholder=t('ph_city_ex'))
with col3:
    village = st.text_input(t('village'), placeholder=t('ph_village_ex'))

# 2. Season & Crop
col_a, col_b = st.columns(2)
with col_a:
    selected_season = st.selectbox(t('select_season'), seasons)
with col_b:
    selected_crop = st.text_input(t('enter_crop'), value=t('rice'), placeholder=t('crop_ph'))

# 3. Area & Image
col_x, col_y = st.columns(2)
with col_x:
    area = st.number_input(t('cult_area'), min_value=0.1, value=5.0, step=0.5)
with col_y:
    uploaded_file = st.file_uploader(t('upload_crop'), type=["jpg", "png", "jpeg"])
    image_data = None
    if uploaded_file:
         from PIL import Image
         image_data = Image.open(uploaded_file)
         st.caption(t('image_loaded'))

# 4. Advanced Scientific Inputs
st.markdown("---")
with st.expander(t('scientific_calc'), expanded=True):
    st.markdown(f"**{t('adv_inputs')}**")
    c1, c2 = st.columns(2)
    with c1:
        sowing_date = st.date_input(t('sowing_date'))
        variety = st.text_input(t('seed_variety'), placeholder=t('seed_ph'))
    with c2:
        irrigation = st.selectbox(t('irrigation'), [t('irri_rainfed'), t('irri_drip'), t('irri_flood'), t('irri_sprinkler')])
        fertilizer = st.text_input(t('fertilizer'), placeholder=t('fert_ph'))
    
    st.markdown("")
    cp1, cp2 = st.columns(2)
    with cp1:
        pest_control_name = st.text_input(t('pest_c_name'), placeholder=t('pest_name_ph'))
    with cp2:
        pest_control = st.text_input(t('pest_ctrl'), placeholder=t('pest_ph'))

# 5. Real-Time Factors
st.markdown("---")
st.subheader(t('real_time_cond'))
col_1, col_2 = st.columns(2)
with col_1:
    soil_type = st.selectbox(t('curr_soil'), [t('soil_loamy'), t('soil_sandy'), t('soil_clayey'), t('soil_saline')])
with col_2:
    weather_outlook = st.selectbox(t('weather_outlook'), [t('weather_normal'), t('weather_drought'), t('weather_heavy_rain'), t('weather_heatwave')])

if st.button(t('predict_yield')):
    with st.spinner(t('analyzing_yield')):
        # Get Current Language
        current_lang = st.session_state.get('language', 'English')
        
        result, error = get_yield_prediction(
            state=selected_state, 
            crop=selected_crop, 
            season=selected_season, 
            area=area, 
            soil=soil_type, 
            weather=weather_outlook, 
            city=city, 
            village=village, 
            image_data=image_data, 
            language=current_lang,
            sowing_date=str(sowing_date),
            variety=variety,
            irrigation=irrigation,
            fertilizer=fertilizer,
            pest_control=pest_control,
            pest_name=pest_control_name
        )
        
    if error:
        st.markdown(f"<p style='color: #F44336; font-weight: 800; font-size: 1.2rem; text-shadow: 0 2px 4px rgba(0,0,0,0.5);'>{error}</p>", unsafe_allow_html=True)
    else:
        est_prod = result['Predicted_Production']
        est_yield = result['Average_Yield']
        explanation = result['AI_Explanation']
        
        st.divider()
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"<p style='color: #4CAF50; font-weight: 800; font-size: 1.4rem; text-shadow: 0 2px 4px rgba(0,0,0,0.5);'>### 🌾 {t('est_prod')}: **{est_prod:,.2f} {t('tonnes')}**</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #2196F3; font-weight: 800; font-size: 1.1rem; text-shadow: 0 2px 4px rgba(0,0,0,0.5);'>{t('est_yield')}: **{est_yield:,.2f} {t('tonnes_acre')}**</p>", unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""
            <style>
                .ai-insight-text, .ai-insight-text * {{
                    color: #000000 !important;
                    text-shadow: none !important;
                    font-weight: 700 !important;
                }}
            </style>
            <div class="ai-insight-text" style="background-color: rgba(255, 255, 255, 0.95); padding: 25px; border-radius: 15px; border-left: 6px solid #FFC107; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
                <h4 style="margin-top: 0; font-size: 1.3rem; color: #000 !important; text-shadow: none !important;">💡 {t('ai_insight')}</h4>
                <p style="font-size: 1.1rem; line-height: 1.6; color: #000 !important; text-shadow: none !important;">
                    {explanation}
                </p>
            </div>
            """, unsafe_allow_html=True)

# Render Bottom Navigation
render_bottom_nav(active_tab='Home')
