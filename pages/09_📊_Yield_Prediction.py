import streamlit as st
import pandas as pd
from logic import get_yield_prediction
from utils import apply_custom_style, t

st.set_page_config(page_title="Yield Prediction", page_icon="📊", layout="wide")
apply_custom_style()

st.title(t('yield_title'))
st.markdown(t('yield_desc'))

# Static Lists
states = ["Maharashtra", "Punjab", "Uttar Pradesh", "Gujarat", "Haryana", "Madhya Pradesh", "Karnataka", "West Bengal", "Bihar", "Rajasthan", "Andhra Pradesh", "Telangana", "Tamil Nadu", "Odisha", "Other"]
seasons = ["Kharif", "Rabi", "Zaid", "Whole Year"]

# Sidebar Filters
st.sidebar.header(t('select_param'))

# 1. Location Details
col1, col2, col3 = st.columns(3)
with col1:
    selected_state = st.selectbox(t('location'), states)
with col2:
    city = st.text_input(t('district_city'), placeholder="e.g. Pune")
with col3:
    village = st.text_input(t('village'), placeholder="e.g. Haveli")

# 2. Season & Crop
col_a, col_b = st.columns(2)
with col_a:
    selected_season = st.selectbox(t('select_season'), seasons)
with col_b:
    selected_crop = st.text_input(t('enter_crop'), value="Rice", placeholder=t('crop_ph'))

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
    soil_type = st.selectbox(t('curr_soil'), ["Normal/Loamy", "Sandy (Low Water Retention)", "Clayey (Water Logging Risk)", "Saline/Degraded"])
with col_2:
    weather_outlook = st.selectbox(t('weather_outlook'), ["Normal Rainfall", "Drought/Low Rainfall", "Heavy Rainfall/Flooding", "Heatwave"])

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
        st.error(error)
    else:
        est_prod = result['Predicted_Production']
        est_yield = result['Average_Yield']
        explanation = result['AI_Explanation']
        
        st.divider()
        col1, col2 = st.columns(2)
        
        with col1:
            st.success(f"### 🌾 {t('est_prod')}: **{est_prod:,.2f} Tonnes**")
            st.info(f"{t('est_yield')}: **{est_yield:,.2f} Tonnes/Acre**")
            
        with col2:
            st.markdown(f"**{t('ai_insight')}:**")
            st.markdown(f"*{explanation}*")
