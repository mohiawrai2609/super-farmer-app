import streamlit as st
from logic import calculate_irrigation
from utils import apply_custom_style, t

st.set_page_config(page_title="Irrigation Hub", page_icon="💧", layout="wide")
apply_custom_style()

st.title(f"💧 {t('irrigation')}")
st.write("Calculate the water needs and frequency for your farm.")

col1, col2 = st.columns(2)
with col1:
    selected_crop = st.text_input(t('enter_crop'), value="Rice", placeholder=t('crop_placeholder'), key="irr_crop")
    soil_type = st.selectbox(t('select_soil'), ["Sandy", "Clayey", "Loamy"], key="irr_soil")
with col2:
    area = st.number_input(t('farm_area'), min_value=0.1, value=1.0)
    
if st.button(t('calc_water')):
    water, frequency = calculate_irrigation(selected_crop, soil_type, area)
    st.success(f"#### {t('req_water')}: **{water}**")
    st.info(frequency)
