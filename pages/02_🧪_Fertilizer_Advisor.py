import streamlit as st
import os
import base64
from utils import apply_custom_style, t, save_db
from logic import get_fertilizer_recommendation
from PIL import Image

st.set_page_config(page_title=t('fert_advisor'), page_icon="🧪", layout="wide")
apply_custom_style()

# Function to encode image
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# --- LOAD BACKGROUND IMAGE ---
bg_image_path = os.path.join("assets", "bg_fertilizer_lab.png")
if os.path.exists(bg_image_path):
    bin_str = get_base64_of_bin_file(bg_image_path)
    bg_image_css = f"""
    [data-testid="stAppViewContainer"], .stApp {{
        background: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.6)), url("data:image/png;base64,{bin_str}") no-repeat center center fixed !important;
        background-size: cover !important;
        background-attachment: fixed !important;
    }}
    """
else:
    bg_image_css = ""

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
.stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div {{
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
.result-val {{
    color: #1B5E20 !important;
    font-weight: 800 !important;
    font-size: 1.3rem !important;
}}
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown(f"""
<div class="header-card" style="padding: 20px; margin-bottom: 30px; text-align: center;">
    <img src="https://img.icons8.com/3d-fluency/512/test-tube.png" width="90" style="filter: drop-shadow(0 4px 8px rgba(0,0,0,0.3)); margin-bottom: 15px;">
    <h1 style="font-size: 3rem; margin:0; color: #ffffff; text-shadow: 0 3px 6px #000000; font-weight: 900;">{t('fert_advisor')}</h1>
    <p style="color: #f0f0f0; font-size: 1.2rem; margin-top:10px; font-weight: 600; text-shadow: 0 2px 4px #000;">{t('fert_subtitle')}</p>
</div>
""", unsafe_allow_html=True)

# Wrappper
st.markdown('<div class="glass-container">', unsafe_allow_html=True)

# --- INPUT METHOD SELECTION ---
col_method, _ = st.columns([2, 1])
with col_method:
    input_method = st.radio(f"{t('input_method')}:", [t('manual'), t('upload')], horizontal=True)

n, p, k = 50, 50, 50
selected_crop = t('rice')
uploaded_image = None
soil_unknown = False
pest_issue = ""

col1, col2 = st.columns(2, gap="large")

if input_method == t('upload'):
    with col1:
        st.markdown(f'<h3 style="color:white;">{t("upload_soil")}</h3>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(t('drop_image'), type=["jpg", "png", "jpeg"])
        if uploaded_file:
            uploaded_image = Image.open(uploaded_file)
            st.image(uploaded_image, caption=t('caption_uploaded'), use_column_width=True, style="border-radius: 15px;")
    with col2:
        st.markdown(f'<h3 style="color:white;">{t("crop_details")}</h3>', unsafe_allow_html=True)
        selected_crop = st.text_input(t('enter_crop'), value=t('rice'), placeholder=t('crop_placeholder'))
        
        stage_opts = [t('stage_pre_sowing'), t('stage_veg'), t('stage_flowering'), t('stage_post_harvest')]
        crop_stage = st.selectbox(t('crop_stage_label'), stage_opts, key="stage_upload")
        
        pest_issue = st.text_input(t('pest_obs'), placeholder=t('pest_obs_ph'), key="pest_upload")

else: # Manual
    with col1:
        st.markdown(f'<h3 style="color:white;">🧪 {t("soil_health")}</h3>', unsafe_allow_html=True)
        # Check for saved profile
        user = st.session_state.get('active_user', {})
        def_n = user.get('soil_n', 50)
        def_p = user.get('soil_p', 50)
        def_k = user.get('soil_k', 50)
        
        soil_unknown = st.checkbox(t('no_card'))
        
        if soil_unknown:
            st.markdown(f"<p style='color: #2196F3; font-weight: 800; font-size: 1.1rem; text-shadow: 0 2px 4px rgba(0,0,0,0.5);'>ℹ️ {t('using_avg')}</p>", unsafe_allow_html=True)
            n, p, k = 50, 50, 50
            if st.button(t('find_lab')):
                 st.switch_page("pages/07_📖_Farming_Knowledge.py")
        else:
            c_n, c_p, c_k = st.columns(3)
            with c_n: n = st.number_input(t('nitrogen'), 0, 200, def_n, key="fert_n")
            with c_p: p = st.number_input(t('phosphorus'), 0, 200, def_p, key="fert_p")
            with c_k: k = st.number_input(t('potassium'), 0, 200, def_k, key="fert_k")
            
            if st.button(t('save_profile')):
                if st.session_state.active_user:
                    phone = st.session_state.active_user['phone']
                    st.session_state.user_data[phone]['soil_n'] = n
                    st.session_state.user_data[phone]['soil_p'] = p
                    st.session_state.user_data[phone]['soil_k'] = k
                    st.session_state.active_user = st.session_state.user_data[phone]
                    save_db(st.session_state.user_data)
                    st.markdown(f"<p style='color: #4CAF50; font-weight: 800; font-size: 1.1rem; text-shadow: 0 2px 4px rgba(0,0,0,0.5);'>✅ {t('profile_saved')}</p>", unsafe_allow_html=True)
            
    with col2:
        st.markdown(f'<h3 style="color:white;">{t("crop_details")}</h3>', unsafe_allow_html=True)
        selected_crop = st.text_input(t('enter_crop'), value=t('rice'), placeholder=t('crop_placeholder'))
        
        stage_opts = [t('stage_pre_sowing'), t('stage_veg'), t('stage_flowering'), t('stage_post_harvest')]
        crop_stage = st.selectbox(t('crop_stage_label'), stage_opts)
        
        pest_issue = st.text_input(t('pest_obs'), placeholder=t('pest_obs_ph'))

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# --- ACTION BUTTON ---
col_center = st.columns([1, 2, 1])
with col_center[1]:
    analyze_btn = st.button(t('get_fert_sugg'), type="primary", use_container_width=True)

if analyze_btn:
    with st.spinner(t('ai_analyzing')):
        lang = st.session_state.get('language', 'English')
        if uploaded_image:
             fert, advice, pest_rec, schedule = get_fertilizer_recommendation(0, 0, 0, selected_crop, image_data=uploaded_image, pest_issue=pest_issue, crop_stage=crop_stage, language=lang)
        else:
             fert, advice, pest_rec, schedule = get_fertilizer_recommendation(n, p, k, selected_crop, pest_issue=pest_issue, crop_stage=crop_stage, language=lang)
             
    # --- RESULT DASHBOARD ---
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown(f"### 💡 {t('ai_insight')}")
    
    r1, r2 = st.columns(2)
    with r1:
        st.markdown(f"""
        <div class="result-card">
            <div class="result-label">🧪 {t('sugg_fert')}</div>
            <div class="result-val">{fert}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="result-card">
            <div class="result-label">📅 {t('rec_schedule')} - {crop_stage}</div>
            <div class="result-text-black">{schedule}</div>
        </div>
        """, unsafe_allow_html=True)
 
    with r2:
        st.markdown(f"""
        <div class="result-card">
            <div class="result-label">🧠 {t('ai_reasoning')}</div>
            <div class="result-text-black">{advice}</div>
        </div>
        """, unsafe_allow_html=True)
        
        if pest_issue:
            st.markdown(f"""
            <div class="result-card">
                <div class="result-label">🦠 {t('rec_pest')}</div>
                <div class="result-text-black">{pest_rec}</div>
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown("</div>", unsafe_allow_html=True)
