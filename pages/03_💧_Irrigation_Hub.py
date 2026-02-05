import streamlit as st
import os
import base64
from utils import t # Safe import for page title if used immediately, but better to hardcode or use later

st.set_page_config(page_title="💧 Irrigation Hub", page_icon="💧", layout="wide")

from logic import calculate_irrigation
from utils import apply_custom_style, render_bottom_nav

# Function to encode image
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Apply Global Style (Sidebar hiding etc.)
apply_custom_style(blur_bg=False)

# --- LOAD BACKGROUND IMAGE ---
current_dir = os.path.dirname(os.path.abspath(__file__))
bg_image_path = os.path.join(os.path.dirname(current_dir), "assets", "irrigation_bg_v2.png")

bg_image_css = ""
if os.path.exists(bg_image_path):
    try:
        img_base64 = get_base64_of_bin_file(bg_image_path)
        # Apply to .stApp for FULL PAGE BACKGROUND as requested
        # Reduced white overlay for better visibility of the "Farmer Scene"
        bg_image_css = f"""
        [data-testid="stAppViewContainer"], .stApp {{
            background: url("data:image/png;base64,{img_base64}") no-repeat center center fixed !important;
            background-size: cover !important;
        }}
        .stApp::before {{
            content: "";
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(255, 255, 255, 0.5); /* Light overlay */
            backdrop-filter: blur(10px) !important;
            -webkit-backdrop-filter: blur(10px) !important;
            z-index: -1;
        }}
        """
    except Exception as e:
        pass

# --- CUSTOM CSS ---
st.markdown(f"""
<style>
/* 1. Page Background */
{bg_image_css}

/* Hide Default Canvas to show our custom background */
#bg-canvas {{
    display: none !important;
}}

/* 2. Header Style */
.header-card {{
    background: rgba(255, 255, 255, 0.3);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 30px;
    border: 1px solid rgba(255, 255, 255, 0.4);
    text-align: center;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}}

/* 3. Card/Container Style - VISION PRO GLASS */
div[data-testid="stVerticalBlockBorderWrapper"] {{
    background: rgba(255, 255, 255, 0.7) !important;
    backdrop-filter: blur(12px) !important;
    border: 2px solid #43A047 !important;
    border-radius: 25px !important;
    box-shadow: 0 15px 35px rgba(27, 94, 32, 0.2) !important;
    padding: 35px !important;
}}

/* 4. Text Styling - Dark Green for high contrast */
h1, h2, h3, h4, label, p {{
    color: #114B15 !important;
    font-weight: 800 !important;
    text-shadow: 0 1px 2px rgba(255,255,255,0.8);
}}

/* 5. Inputs - Crisp White */
.stTextInput input, .stNumberInput input, div[data-baseweb="select"] > div {{
    background-color: #FFFFFF !important;
    color: #114B15 !important;
    border: 1px solid #43A047 !important;
    font-weight: 700 !important;
}}

/* 6. Primary Button */
button[kind="primary"] {{
    background: linear-gradient(135deg, #43A047 0%, #1B5E20 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    font-weight: 900 !important;
    text-transform: uppercase;
    letter-spacing: 1px;
    box-shadow: 0 4px 15px rgba(46, 125, 50, 0.4) !important;
}}

/* 7. Ensure Footer visibility */
.bottom-nav {{
    background: white !important;
    border-top: 2px solid #43A047 !important;
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
             <p style="color: #2E7D32; font-size: 1.1rem; margin:0; font-style: italic; font-weight: 700;">{t('smart_water')}</p>
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
            <div style="background: linear-gradient(135deg, #0288D1, #01579B); border-radius: 20px; padding: 25px; text-align: center; color: white; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
                <div style="font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px; opacity: 0.9; color: white !important;">{t('req_water')}</div>
                <div style="font-size: 2.2rem; font-weight: 800; margin-top: 5px; color: white !important;">{water}</div>
            </div>
            """, unsafe_allow_html=True)
            
        with res_c2:
            st.markdown(f"""
            <div style="background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(10px); border-radius: 20px; padding: 25px; height: 100%; display: flex; flex-direction: column; justify-content: center; border: 1px solid #0288D1;">
                <div style="font-size: 1rem; color: #0277BD; font-weight: 700;">{t('rec_schedule')}</div>
                <div style="font-size: 1.2rem; font-weight: 600; color: #01579B; margin-top: 5px;">{frequency}</div>
            </div>
            """, unsafe_allow_html=True)

# Render Bottom Navigation
render_bottom_nav(active_tab='Home')
st.markdown("<br><br><br><br>", unsafe_allow_html=True) # Extra padding for footer
