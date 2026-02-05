# Force reload
import streamlit as st

st.set_page_config(page_title="👤 User Profile", page_icon="👤", layout="wide")

from utils import apply_custom_style, t, save_db, load_db, render_bottom_nav

apply_custom_style()

if 'active_user' not in st.session_state or not st.session_state.active_user:
    st.markdown(f"<p style='color: #F44336; font-weight: 800; font-size: 1.2rem; text-align: center; margin-top: 50px;'>{t('login_first')}</p>", unsafe_allow_html=True)
    if st.button(t('go_home'), use_container_width=True, type="primary"):
         st.switch_page("app.py")
    st.stop()

user = st.session_state.active_user

# --- VISUAL STYLING INJECTION ---
st.markdown("""
<style>
/* 1. Global White Background */
.stApp {
    background: #ffffff !important;
}

/* 2. Profile Header - Solid & Premium */
.profile-header {
    background: linear-gradient(135deg, #FF9800 0%, #EF6C00 100%);
    border-radius: 30px;
    padding: 35px;
    border: 1px solid rgba(255,255,255,0.2);
    box-shadow: 0 15px 35px rgba(0,0,0,0.2);
    display: flex;
    align-items: center;
    gap: 25px;
    margin-bottom: 35px;
}

/* 3. Profile Photo Styling */
.profile-img-container {
    padding: 5px;
    background: #ffffff;
    border-radius: 50%;
    box-shadow: 0 8px 15px rgba(0,0,0,0.1);
}
.profile-img {
    width: 110px;
    height: 110px;
    border-radius: 50%;
    border: 4px solid #ffffff;
    object-fit: cover;
    display: block;
}

/* 4. Font Styling - WHITE for Colored Background */
.profile-name {
    color: #ffffff !important;
    font-size: 2.2rem;
    font-weight: 900;
    margin: 0;
    text-shadow: 0 2px 4px rgba(0,0,0,0.3) !important;
}
.profile-loc {
    color: rgba(255,255,255,0.9) !important;
    font-size: 1.1rem;
    font-weight: 600;
    margin-top: 5px;
}
.section-title {
    color: #E65100 !important;
    font-size: 1.6rem;
    font-weight: 800 !important;
    margin: 35px 0 20px 0;
    border-bottom: 3px solid #FF9800;
    padding-bottom: 8px;
    display: inline-block;
}

/* 5. Glass Action Cards - Darker Labels */
.glass-action-card {
    background: #ffffff !important;
    border-radius: 20px;
    padding: 25px;
    text-align: center;
    border: 1px solid #e0e0e0 !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    transition: all 0.3s ease;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-decoration: none !important;
}
.glass-action-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    border-color: #FF9800 !important;
}
.action-label {
    color: #333 !important;
    font-size: 1rem;
    font-weight: 700 !important;
    margin-top: 10px;
}
.action-icon {
    width: 65px;
    height: 65px;
}

/* 6. Button Styling - Proper Colors */
div.stButton > button {
    border-radius: 12px !important;
    font-weight: 700 !important;
    padding: 0.6rem 1rem !important;
    transition: all 0.2s ease !important;
}

/* Sign Out Button - Red */
[data-testid="stBaseButton-secondary"] {
    background: #FFEBEE !important;
    color: #D32F2F !important;
    border: 1px solid #FFCDD2 !important;
}
[data-testid="stBaseButton-secondary"]:hover {
    background: #D32F2F !important;
    color: white !important;
}

/* Home & Profile Buttons - Orange */
[data-testid="stBaseButton-primary"] {
    background: linear-gradient(135deg, #FF9800, #EF6C00) !important;
    color: white !important;
    border: none !important;
}
</style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
st.markdown(f"""
<div class="profile-header">
    <div class="profile-img-container">
        <img src="https://cdn-icons-png.flaticon.com/512/149/149071.png" class="profile-img">
    </div>
    <div>
        <div class="profile-name">{user['name']}</div>
        <div class="profile-loc">📍 {user['city']}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- QUERY PARAM HANDLER ---
params = st.query_params
mode = params.get("mode", None)

if mode:
    # Use a glass container for forms
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    
    if mode == "edit_crop":
        st.markdown(f"### 🌱 {t('prof_select_crop')}")
        new_crop = st.text_input(t('select_crop'), value=user.get('crop', ''))
        col_act1, col_act2 = st.columns(2)
        with col_act1:
            if st.button(t('save'), key="save_crop_btn", type="primary"):
                st.session_state.active_user['crop'] = new_crop
                save_db(st.session_state.user_data)
                st.markdown(f"<p style='color: #4CAF50; font-weight: 800;'>✅ {t('auth_success')}</p>", unsafe_allow_html=True)
                st.query_params.clear()
                st.rerun()
        with col_act2:
            if st.button(t('back'), key="cancel_crop"):
                st.query_params.clear()
                st.rerun()

    elif mode == "edit_loc":
        st.markdown(f"### 📍 {t('prof_location')}")
        new_city = st.text_input(t('city'), value=user.get('city', ''))
        col_act1, col_act2 = st.columns(2)
        with col_act1:
            if st.button(t('save'), key="save_loc_btn", type="primary"):
                st.session_state.active_user['city'] = new_city
                save_db(st.session_state.user_data)
                st.markdown(f"<p style='color: #4CAF50; font-weight: 800;'>✅ {t('auth_success')}</p>", unsafe_allow_html=True)
                st.query_params.clear()
                st.rerun()
        with col_act2:
            if st.button(t('back'), key="cancel_loc"):
                st.query_params.clear()
                st.rerun()
                
    elif mode == "edit_lang":
        st.markdown(f"### 🌐 {t('prof_change_lang')}")
        current_lang = st.session_state.get('language', 'English')
        options = ['English', 'Hindi', 'Marathi']
        new_lang = st.selectbox(t('prof_change_lang'), options, index=options.index(current_lang) if current_lang in options else 0)
        col_act1, col_act2 = st.columns(2)
        with col_act1:
            if st.button(t('save'), key="save_lang_btn", type="primary"):
                st.session_state.language = new_lang
                st.session_state.active_user['language'] = new_lang
                save_db(st.session_state.user_data)
                st.markdown(f"<p style='color: #4CAF50; font-weight: 800;'>✅ {t('auth_success')}</p>", unsafe_allow_html=True)
                st.query_params.clear()
                st.rerun()
        with col_act2:
            if st.button(t('back'), key="cancel_lang"):
                st.query_params.clear()
                st.rerun()

    elif mode == "edit_full":
        st.markdown(f"### 📋 {t('prof_full_profile')}")
        with st.form("full_profile_form"):
            new_name = st.text_input(t('full_name'), value=user.get('name', ''))
            new_land = st.number_input(t('land_size'), value=float(user.get('land_size', 1.0)))
            new_n = st.number_input(t('nitrogen'), value=float(user.get('soil_n', 50)))
            new_p = st.number_input(t('phosphorus'), value=float(user.get('soil_p', 50)))
            new_k = st.number_input(t('potassium'), value=float(user.get('soil_k', 50)))
            if st.form_submit_button(t('save')):
                st.session_state.active_user['name'] = new_name
                st.session_state.active_user['land_size'] = new_land
                st.session_state.active_user['soil_n'] = new_n
                st.session_state.active_user['soil_p'] = new_p
                st.session_state.active_user['soil_k'] = new_k
                save_db(st.session_state.user_data)
                st.markdown(f"<p style='color: #4CAF50; font-weight: 800;'>✅ {t('auth_success')}</p>", unsafe_allow_html=True)
                st.query_params.clear()
                st.rerun()
            if st.form_submit_button(t('back')):
                st.query_params.clear()
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

#Helper to render glass action link
def glass_link(icon_url, label, url):
    code = f"""
    <a href="{url}" target="_self" class="glass-action-card">
        <img src="{icon_url}" class="action-icon">
        <div class='action-label'>{label}</div>
    </a>
    """
    st.markdown(code, unsafe_allow_html=True)

# --- MY INFORMATION SECTION ---
st.markdown(f'<div class="section-title">{t("prof_my_info")}</div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3, gap="medium")

with c1:
    glass_link("https://img.icons8.com/3d-fluency/512/wheat.png", t("prof_select_crop"), "?mode=edit_crop")
with c2:
    glass_link("https://img.icons8.com/3d-fluency/512/language.png", t("prof_change_lang"), "?mode=edit_lang")
with c3:
    glass_link("https://img.icons8.com/3d-fluency/512/map-pin.png", t("prof_location"), "?mode=edit_loc")

st.markdown(" <br> ", unsafe_allow_html=True)

# --- FEATURES SECTION ---
st.markdown(f'<div class="section-title">{t("prof_features")}</div>', unsafe_allow_html=True)
f1, f2, f3 = st.columns(3, gap="medium")

with f1:
    glass_link("https://img.icons8.com/3d-fluency/512/sprout.png", t("prof_crop_care"), "Crop_Recommendation")
with f2:
    glass_link("https://img.icons8.com/3d-fluency/512/shield.png", t("prof_protection"), "Fertilizer_Advisor")
with f3:
    glass_link("https://img.icons8.com/3d-fluency/512/test-tube.png", t("prof_fertilizer"), "Fertilizer_Advisor")

st.markdown("---")

# --- FOOTER BUTTONS ---
col_foot1, col_foot2 = st.columns(2)
with col_foot1:
    if st.button(t("prof_sign_out"), use_container_width=True):
        st.session_state.active_user = None
        if 'meta' in st.session_state.user_data:
            st.session_state.user_data['meta']['last_active_phone'] = None
            save_db(st.session_state.user_data)
        st.switch_page("app.py")

with col_foot2:
    if st.button(t("prof_full_profile"), use_container_width=True, type="primary"):
        st.query_params.clear()
        st.query_params["mode"] = "edit_full"
        st.rerun()

st.markdown(" <br><br> ", unsafe_allow_html=True)
if st.button(t("prof_back_home"), use_container_width=True, type="primary"):
    st.session_state.current_view = 'dashboard'
    st.switch_page("app.py")

# Render Bottom Navigation
render_bottom_nav(active_tab='Home')
