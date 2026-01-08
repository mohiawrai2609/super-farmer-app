import streamlit as st
from utils import apply_custom_style, t, save_db
from logic import get_fertilizer_recommendation
from PIL import Image

st.set_page_config(page_title="Fertilizer Advisor", page_icon="🧪", layout="wide")
apply_custom_style()

st.title(f"🧪 {t('fert_advisor')}")
st.write("Get suggestions for the right fertilizers based on your soil profile.")

# --- INPUT METHOD SELECTION ---
input_method = st.radio(t('input_method'), [t('manual'), t('upload')], horizontal=True)

n, p, k = 50, 50, 50
selected_crop = "Rice"
uploaded_image = None
soil_unknown = False

col1, col2 = st.columns(2)

if input_method == t('upload'):
    with col1:
        uploaded_file = st.file_uploader(t('drop_image'), type=["jpg", "png", "jpeg"])
        if uploaded_file:
            uploaded_image = Image.open(uploaded_file)
            st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
    with col2:
        selected_crop = st.text_input(t('enter_crop'), value="Rice", placeholder=t('crop_placeholder'))
        
        # New: Crop Growth Stage
        stage_opts = t('stage_options') if isinstance(t('stage_options'), list) else ['Pre-Sowing', 'Growth', 'Flowering', 'Harvest']
        crop_stage = st.selectbox(t('crop_stage_label'), stage_opts, key="stage_upload")
        
        # New: Optional Pest Observation
        pest_issue = st.text_input(t('pest_obs'), placeholder=t('pest_obs_ph'), key="pest_upload")

else: # Manual
    with col1:
        # Check for saved profile
        user = st.session_state.get('active_user', {})
        def_n = user.get('soil_n', 50)
        def_p = user.get('soil_p', 50)
        def_k = user.get('soil_k', 50)
        
        soil_unknown = st.checkbox(t('no_card'))
        
        if soil_unknown:
            st.info(f"ℹ️ {t('using_avg')}")
            n, p, k = 50, 50, 50
            if st.button(t('find_lab')):
                 st.switch_page("pages/07_📖_Farming_Knowledge.py")
        else:
            n = st.number_input(t('nitrogen'), min_value=0, max_value=200, value=def_n, key="fert_n")
            p = st.number_input(t('phosphorus'), min_value=0, max_value=200, value=def_p, key="fert_p")
            k = st.number_input(t('potassium'), min_value=0, max_value=200, value=def_k, key="fert_k")
            
            # Save Profile Button
            if st.button(t('save_profile')):
                if st.session_state.active_user:
                    phone = st.session_state.active_user['phone']
                    st.session_state.user_data[phone]['soil_n'] = n
                    st.session_state.user_data[phone]['soil_p'] = p
                    st.session_state.user_data[phone]['soil_k'] = k
                    st.session_state.active_user = st.session_state.user_data[phone] # Update session
                    save_db(st.session_state.user_data)
                    st.success(t('profile_saved'))
            
    with col2:
        selected_crop = st.text_input(t('enter_crop'), value="Rice", placeholder=t('crop_placeholder'))
        
        # New: Crop Growth Stage
        stage_opts = t('stage_options') if isinstance(t('stage_options'), list) else ['Pre-Sowing', 'Growth', 'Flowering', 'Harvest']
        crop_stage = st.selectbox(t('crop_stage_label'), stage_opts)
        
        # New: Optional Pest Observation
        pest_issue = st.text_input(t('pest_obs'), placeholder=t('pest_obs_ph'))
    
if st.button(t('get_fert_sugg')):
    with st.spinner("Analyzing..."):
        lang = st.session_state.get('language', 'English')
        if uploaded_image:
             fert, advice, pest_rec, schedule = get_fertilizer_recommendation(0, 0, 0, selected_crop, image_data=uploaded_image, pest_issue=pest_issue, crop_stage=crop_stage, language=lang)
        else:
             fert, advice, pest_rec, schedule = get_fertilizer_recommendation(n, p, k, selected_crop, pest_issue=pest_issue, crop_stage=crop_stage, language=lang)
             
    st.success(f"### {t('sugg_fert')}: **{fert}**")
    st.info(f"### {t('rec_schedule')}: **{schedule}**")
    st.warning(f"### {t('rec_pest')}: **{pest_rec}**")
    st.write(f"**💡 {t('ai_reasoning')}:** {advice}")
