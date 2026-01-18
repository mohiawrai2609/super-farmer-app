import streamlit as st
from logic import calculate_irrigation
from utils import apply_custom_style, t, render_bottom_nav
import base64
import os

# Function to encode image
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

st.set_page_config(page_title=t('irrigation'), page_icon="💧", layout="wide")

# Apply Global Style
apply_custom_style(blur_bg=True) # Keep global blur for consistency

# --- LOAD BACKGROUND IMAGE ---
current_dir = os.path.dirname(os.path.abspath(__file__))
bg_image_path = os.path.join(os.path.dirname(current_dir), "assets", "irrigation_bg_v2.png")

bg_style = ""
if os.path.exists(bg_image_path):
    try:
        img_base64 = get_base64_of_bin_file(bg_image_path)
        # Re-applying to the card as per original "Same" request
        bg_style = f"""
            background: linear-gradient(rgba(255, 255, 255, 0.8), rgba(255, 255, 255, 0.9)), 
                        url("data:image/png;base64,{img_base64}") center center / cover no-repeat !important;
        """
    except:
        bg_style = "background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%) !important;"
else:
    bg_style = "background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%) !important;"

# --- CUSTOM CSS ---
st.markdown(f"""
<style>
    /* 1. Page Background - Keep it light */
    .stApp {{
        background: #F1F8E9 !important;
    }}
    
    /* 2. Inner Card Style - RESTORING ORIGINAL "FARMER" THEME */
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        {bg_style}
        border: 2px solid #66BB6A !important;
        border-radius: 20px !important;
        box-shadow: 0 10px 30px rgba(27, 94, 32, 0.2) !important;
        padding: 30px !important;
    }}
    
    /* 3. Text Styling - Dark Green */
    div[data-testid="stVerticalBlockBorderWrapper"] label,
    div[data-testid="stVerticalBlockBorderWrapper"] h3,
    div[data-testid="stVerticalBlockBorderWrapper"] p {{
        color: #1B5E20 !important;
        font-weight: 700 !important;
    }}
    
    /* Header Card Adjustments */
    .header-card {{
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(5px);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 30px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        text-align: center;
    }}

    /* Inputs */
    .stTextInput input, .stNumberInput input, div[data-baseweb="select"] > div {{
        background-color: #FFFFFF !important;
        color: #1B5E20 !important;
        border: 1px solid #81C784 !important;
    }}
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown(f"""
<div class="header-card">
    <div style="display:flex; justify-content:center; align-items:center; gap:20px;">
        <img src="https://cdn-icons-png.flaticon.com/512/3214/3214746.png" width="80" style="filter: drop-shadow(0 4px 6px rgba(0,0,0,0.1));">
        <div>
            <h1 style="font-size: 2.5rem; margin:0; color: #1B5E20;">{t('irrigation')}</h1>
             <p style="color: #2E7D32; font-size: 1.1rem; margin:0; font-style: italic; font-weight: 600;">{t('smart_water')}</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- MAIN INPUT SECTION ---
with st.container(border=True):
    st.markdown(f"<h3 style='margin-bottom:30px; text-align: center;'>🚜 {t('calc_water')}</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")
    with col1:
        selected_crop = st.text_input(t('enter_crop'), value=t('rice'), placeholder=t('crop_placeholder'), key="irr_crop")
        soil_type = st.selectbox(t('select_soil'), [t('soil_sandy_simple'), t('soil_clayey_simple'), t('soil_loamy_simple')], key="irr_soil")
    with col2:
        area = st.number_input(t('farm_area'), min_value=0.1, value=1.0)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button(t('calc_water'), type="primary", use_container_width=True):
        lang = st.session_state.get('language', 'English')
        water, frequency = calculate_irrigation(selected_crop, soil_type, area, language=lang)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("---")
        res_c1, res_c2 = st.columns([1, 2], gap="large")
        
        with res_c1:
             st.markdown(f"""
            <div style="background: rgba(2, 136, 209, 0.9); border-radius: 20px; padding: 25px; text-align: center; color: white; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                <div style="font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px; opacity: 0.9;">{t('req_water')}</div>
                <div style="font-size: 2.2rem; font-weight: 800; margin-top: 5px;">{water}</div>
            </div>
            """, unsafe_allow_html=True)
            
        with res_c2:
            st.markdown(f"""
            <div style="background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(10px); border-radius: 20px; padding: 25px; height: 100%; display: flex; flex-direction: column; justify-content: center; border: 1px solid rgba(255,255,255,0.5);">
                <div style="font-size: 1rem; color: #0277BD; font-weight: 600;">{t('rec_schedule')}</div>
                <div style="font-size: 1.2rem; font-weight: 500; color: #01579B; margin-top: 5px;">{frequency}</div>
            </div>
            """, unsafe_allow_html=True)

# Render Bottom Navigation
render_bottom_nav(active_tab='Home')
st.markdown("<br><br><br>", unsafe_allow_html=True)
