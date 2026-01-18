import streamlit as st
from utils import apply_custom_style, t, render_bottom_nav

st.set_page_config(page_title=t('insurance'), page_icon="🛡️", layout="wide")
apply_custom_style()

# --- HEADER (Vision Pro Style) ---
# --- LOAD BACKGROUND IMAGE ---
import os
import base64

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

bg_img_path = os.path.join("assets", "bg_insurance.png")
if os.path.exists(bg_img_path):
    bin_str = get_base64_of_bin_file(bg_img_path)
    bg_image_css = f"""
    [data-testid="stAppViewContainer"], .stApp {{
        background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.7)), url("data:image/png;base64,{bin_str}") no-repeat center center fixed !important;
        background-size: cover !important;
        background-attachment: fixed !important;
    }}
    """
else:
    # Fallback if file missing
    bg_image_css = """
    [data-testid="stAppViewContainer"], .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.7)), url("https://images.unsplash.com/photo-1625246333195-58f214f063ce?q=80&w=2600") no-repeat center center fixed !important;
        background-size: cover !important;
    }
    """

st.markdown(f"""
<div class="header-card" style="padding: 40px; margin-bottom: 20px;">
    <h1 style="font-size: 2.5rem; color: #FFFFFF;">{t('ins_title')}</h1>
    <p style="color: #E0E0E0; font-size: 1.1rem; margin-top: 10px;">{t('ins_sub')}</p>
</div>
""", unsafe_allow_html=True)

# --- CSS INJECTION FOR TABS & RESULTS ---
st.markdown("""
<style>
/* 1. Background Injection */
""" + bg_image_css + """

/* Hide Default Canvas */
#bg-canvas {
    display: none !important;
}

/* Tabs Styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
    background-color: transparent;
}
.stTabs [data-baseweb="tab"] {
    background-color: rgba(255, 255, 255, 0.1);
    border-radius: 15px;
    color: white;
    padding: 10px 25px;
    border: 1px solid rgba(255, 255, 255, 0.2);
}
.stTabs [aria-selected="true"] {
    background-color: rgba(76, 175, 80, 0.3) !important;
    border-color: #4CAF50 !important;
    color: #FFF8E1 !important;
    font-weight: bold;
}

/* Text Visibility Override */
h1, h2, h3, h4, p, span, label, li, strong {
    color: #ffffff !important;
    text-shadow: 0 1px 2px rgba(0,0,0,0.5);
    font-weight: 500;
}
.streamlit-expanderContent p, .streamlit-expanderContent li {
    font-size: 1.05rem !important;
}

/* Result Cards */
.result-card {
    background: rgba(255, 255, 255, 0.9);
    border-radius: 20px;
    padding: 25px;
    margin-top: 20px;
    border-left: 8px solid #4CAF50;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}
/* Ensure result card text is dark for readability on white card */
.result-card .result-label {
    font-size: 0.9rem;
    color: #555 !important;
    font-weight: 600;
    text-shadow: none !important;
}
.result-card .result-value {
    font-size: 2.2rem;
    color: #2E7D32 !important;
    font-weight: 800;
    text-shadow: none !important;
}
.result-card .result-sub {
    font-size: 1.1rem;
    color: #333 !important;
    margin-top: 10px;
    font-weight: 500;
    text-shadow: none !important;
}
</style>
""", unsafe_allow_html=True)

# Wrapper for structure
st.markdown('<div class="glass-container">', unsafe_allow_html=True)

# Scheme Selection using Tabs
tab1, tab2 = st.tabs([f"🌾 {t('pmfby')}", f"🌦️ {t('wbcis')}"])

with tab1:
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown(f"### 📋 {t('pmfby')}")
        crop_type = st.selectbox(t('crop_type'), [t('kharif_opt'), t('rabi_opt'), t('commercial')], key="pmfby_crop")
        sum_insured = st.number_input(t('sum_insured'), min_value=10000, value=50000, key="pmfby_sum")
        area = st.number_input(t('area'), min_value=0.1, value=1.0, key="pmfby_area")

        # Calculate Premium
        # Rates: Kharif=2%, Rabi=1.5%, Commercial=5%
        rate = 0.02
        if crop_type == t('rabi_opt'):
            rate = 0.015
        elif crop_type == t('commercial'):
            rate = 0.05
        
        farmer_share = sum_insured * area * rate
        govt_share = sum_insured * area * (0.12 - rate) # Hypothetical total premium 12%
        if govt_share < 0: govt_share = 0

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button(t('calc_premium'), key="btn_pmfby", type="primary"):
            st.session_state['premium_pmfby'] = {
                "farmer": farmer_share,
                "govt": govt_share,
                "total": farmer_share + govt_share
            }

    with col2:
        if 'premium_pmfby' in st.session_state:
            res = st.session_state['premium_pmfby']
            
            # Custom HTML Result Card
            st.markdown(f"""
            <div class="result-card">
                <div class="result-label">{t('farmer_share')}</div>
                <div class="result-value">₹{res['farmer']:,.2f}</div>
                <div style="margin: 15px 0; border-top: 1px dashed #ccc;"></div>
                <div style="display:flex; justify-content:space-between;">
                    <div>
                        <div class="result-label" style="font-size:0.75rem;">{t('govt_share')}</div>
                        <div class="result-sub">₹{res['govt']:,.2f}</div>
                    </div>
                    <div style="text-align:right;">
                        <div class="result-label" style="font-size:0.75rem;">{t('total_premium')}</div>
                        <div class="result-sub" style="color:#1565C0;">₹{res['total']:,.2f}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"<p style='color: #2196F3; font-weight: 600;'>👈 {t('calc_premium')}</p>", unsafe_allow_html=True)

with tab2:
    col1, col2 = st.columns([1, 1], gap="large")
    with col1:
        st.markdown(f"### 🌦️ {t('wbcis')}")
        st.caption(t('wbcis_desc'))
        
        risk_type = st.selectbox(t('weather_risk'), [t('risk_drought'), t('risk_excess'), t('risk_unseasonal')])
        w_sum_insured = st.number_input(t('sum_insured'), min_value=15000, value=60000, key="wbcis_sum")
        w_area = st.number_input(t('area'), min_value=0.1, value=1.0, key="wbcis_area")
        
        # WBCIS Rates are significantly higher (approx 8-10%)
        w_rate = 0.08
        if risk_type == t('risk_unseasonal'):
            w_rate = 0.10
        elif risk_type == t('risk_excess'):
            w_rate = 0.09
            
        w_farmer_share = w_sum_insured * w_area * w_rate
        w_govt_share = w_sum_insured * w_area * 0.05 # Fixed subsidy
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button(t('calc_premium'), key="btn_wbcis", type="primary"):
            st.session_state['premium_wbcis'] = {
                "farmer": w_farmer_share,
                "govt": w_govt_share,
                "total": w_farmer_share + w_govt_share
            }
            
    with col2:
         if 'premium_wbcis' in st.session_state:
            res = st.session_state['premium_wbcis']
            # Custom HTML Result Card (Red/Orange theme for Risk)
            st.markdown(f"""
            <div class="result-card" style="border-left-color: #FF5722;">
                <div class="result-label">{t('farmer_share')} {t('high_risk')}</div>
                <div class="result-value" style="color: #BF360C;">₹{res['farmer']:,.2f}</div>
                <div style="margin: 15px 0; border-top: 1px dashed #ccc;"></div>
                <div style="display:flex; justify-content:space-between;">
                    <div>
                        <div class="result-label" style="font-size:0.75rem;">{t('govt_share')}</div>
                        <div class="result-sub">₹{res['govt']:,.2f}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
         else:
            st.markdown(f"<p style='color: #2196F3; font-weight: 600;'>👈 {t('calc_premium')}</p>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
render_bottom_nav(active_tab='Home')
st.markdown("<br><br><br>", unsafe_allow_html=True)

# Schemes Info Section
st.markdown("---")
with st.expander(t('ins_info_title')):
    st.markdown(t('ins_info_content'))
