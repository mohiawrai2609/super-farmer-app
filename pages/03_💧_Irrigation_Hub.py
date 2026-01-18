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
apply_custom_style()

st.markdown(f"""
<div class="glass-container">
    <div class="header-card" style="background: transparent; box-shadow: none; border: none; padding: 0;">
        <div style="display:flex; justify-content:center; align-items:center; gap:20px;">
            <img src="https://cdn-icons-png.flaticon.com/512/3214/3214746.png" width="80" style="filter: drop-shadow(0 4px 6px rgba(0,0,0,0.1));">
            <div>
                <h1 style="font-size: 2.5rem; margin:0; color: #1B5E20; text-shadow: 0 1px 2px rgba(255,255,255,0.5);">{t('irrigation')}</h1>
                <p style="color: #2E7D32; font-size: 1.1rem; margin:0; font-style: italic; font-weight: 600;">{t('smart_water')}</p>
            </div>
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
