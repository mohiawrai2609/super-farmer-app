import streamlit as st
import pandas as pd
import os
import base64

st.set_page_config(page_title="Farming Knowledge", page_icon="📖", layout="wide")

from logic import KNOWLEDGE_BASE
from utils import apply_custom_style, t, render_bottom_nav
# --- LOAD BACKGROUND IMAGE ---
import os
import base64

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

bg_img_path = os.path.join("assets", "bg_knowledge_clear.png")
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
{bg_image_css}

/* Hide Default Canvas */
#bg-canvas {{
    display: none !important;
}}

/* 2. Text Visibility - FORCE WHITE with STRONG SHADOW and BOLD */
h1, h2, h3, h4, h5, p, span, label, div, .stMarkdown, .stText, li, strong {{
    color: #ffffff !important;
    text-shadow: 0 2px 4px #000000 !important; /* Strong dark shadow */
    font-weight: 800 !important; /* Bold */
}}

/* Tabs Styling */
.stTabs [data-baseweb="tab-list"] {{
    gap: 15px;
    background-color: transparent;
    padding: 10px 0;
}}
.stTabs [data-baseweb="tab"] {{
    background-color: rgba(255, 255, 255, 0.1) !important;
    backdrop-filter: blur(10px);
    border-radius: 15px;
    color: white !important;
    padding: 12px 25px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    font-weight: 700 !important;
}}
.stTabs [aria-selected="true"] {{
    background: linear-gradient(135deg, #4CAF50, #2E7D32) !important;
    border-color: #ffffff !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}}

/* Expander Styling */
div[data-testid="stExpander"] {{
    background-color: rgba(255, 255, 255, 0.1) !important;
    backdrop-filter: blur(10px);
    border-radius: 12px !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    margin-bottom: 10px;
}}
div[data-testid="stExpander"] summary span {{
    font-size: 1.2rem !important;
    color: #ffffff !important;
}}
div[data-testid="stExpander"] [data-testid="stExpanderDetails"] {{
    background-color: rgba(0, 0, 0, 0.3) !important;
    padding: 20px;
    border-radius: 0 0 12px 12px;
}}
</style>
""", unsafe_allow_html=True)

# Get current language from session state
current_lang = st.session_state.get('language', 'English')
kb_data = KNOWLEDGE_BASE.get(current_lang, KNOWLEDGE_BASE['English'])

st.markdown(f"""
<div style="text-align: center; margin-bottom: 30px; padding: 20px;">
    <h1 style="font-size: 3.5rem; margin:0; color: #ffffff; text-shadow: 0 3px 6px #000000; font-weight: 900;">📖 {t('kb_title')}</h1>
    <p style="color: #f0f0f0; font-size: 1.3rem; margin-top:10px; font-weight: 600; text-shadow: 0 2px 4px #000;">{t('kb_subtitle')}</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs([t('tab_seasons'), t('tab_pests'), t('tab_schemes'), t('tab_labs'), t('tab_health')])

with tab1:
    st.subheader(t('sub_seasons'))
    for item in kb_data.get("Seasons", []):
        with st.expander(item["Season"]):
            st.write(f"**{t('kb_crops')}:** {item['Crops']}")
            st.write(f"**{t('kb_care')}:** {item['Care']}")
            
with tab2:
    st.subheader(t('sub_pests'))
    for item in kb_data.get("Pests", []):
        with st.expander(item["Pest"]):
            st.write(f"**{t('kb_symptoms')}:** {item['Symptoms']}")
            st.write(f"**{t('kb_treatment')}:** {item['Cure']}")

with tab3:
    st.subheader(t('sub_schemes'))
    for item in kb_data.get("Schemes", []):
        with st.expander(item["Name"]):
            st.write(f"**{t('kb_benefit')}:** {item['Benefit']}")
            st.write(f"**{t('kb_eligibility')}:** {item['Eligibility']}")

with tab4:
    st.subheader(t('sub_labs'))
    for item in kb_data.get("SoilLabs", []):
        with st.expander(item["Center"]):
            st.write(f"**{t('kb_address')}:** {item['Address']}")
            st.write(f"**{t('kb_contact')}:** {item['Contact']}")
            
with tab5:
    st.subheader(t('sub_health'))
    for item in kb_data.get("SoilHealth", []):
         with st.expander(item["Title"]):
             st.write(item["Tip"])

# Render Bottom Navigation
render_bottom_nav(active_tab='About')
