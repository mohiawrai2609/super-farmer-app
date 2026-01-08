# Force reload
import streamlit as st
from utils import apply_custom_style, t, save_db, load_db

st.set_page_config(page_title="User Profile", page_icon="👤", layout="wide")
apply_custom_style()

# --- AUTO-LOGIN LOGIC ---
if 'active_user' not in st.session_state or not st.session_state.active_user:
    # Try to recover session from disk
    if 'user_data' not in st.session_state:
        st.session_state.user_data = load_db()
    
    last_phone = st.session_state.user_data.get('meta', {}).get('last_active_phone')
    if last_phone:
        user_obj = st.session_state.user_data.get(str(last_phone))
        if user_obj:
            st.session_state.active_user = user_obj
            # st.success(f"Welcome back, {user_obj['name']}") # Optional toast

if 'active_user' not in st.session_state or not st.session_state.active_user:
    st.error("Please login from the Home page first.")
    if st.button("Go to Home"):
         st.switch_page("app.py")
    st.stop()

user = st.session_state.active_user

# --- HEADER SECTION ---
col_head1, col_head2 = st.columns([1, 4])
with col_head1:
    st.markdown('<img src="https://cdn-icons-png.flaticon.com/512/3022/3022938.png" style="border-radius: 50%; border: 2px solid #4CAF50; width: 80px;">', unsafe_allow_html=True)
with col_head2:
    st.markdown(f"<h2 style='margin:0; color: #2E7D32;'>{user['name']}</h2>", unsafe_allow_html=True)

    st.caption("📍 " + user['city'])

st.markdown("---")

# --- QUERY PARAM HANDLER ---
# Check if a mode is active
params = st.query_params
mode = params.get("mode", None)

if mode == "edit_crop":
    with st.container():
        st.info("🌱 Update Your Main Crop")
        new_crop = st.text_input("New Crop Name", value=user.get('crop', ''))
        if st.button("Save Crop", key="save_crop_btn"):
            st.session_state.active_user['crop'] = new_crop
            save_db(st.session_state.user_data)
            st.success("Updated!")
            st.query_params.clear() # Clear param
            st.rerun()
        if st.button("Cancel", key="cancel_crop"):
             st.query_params.clear()
             st.rerun()

elif mode == "edit_loc":
    with st.container():
        st.info("📍 Update Your Location")
        new_city = st.text_input("New City Name", value=user.get('city', ''))
        if st.button("Save Location", key="save_loc_btn"):
            st.session_state.active_user['city'] = new_city
            save_db(st.session_state.user_data)
            st.success("Updated!")
            st.query_params.clear()
            st.rerun()
        if st.button("Cancel", key="cancel_loc"):
             st.query_params.clear()
             st.rerun()
             
elif mode == "edit_lang":
    with st.container():
        st.info("🌐 Change App Language")
        new_lang = st.selectbox("Select Language", ['English', 'Hindi', 'Marathi'])
        if st.button("Update Language", key="save_lang_btn"):
            st.session_state.language = new_lang
            st.success("Updated!")
            st.query_params.clear()
            st.rerun()
        if st.button("Cancel", key="cancel_lang"):
             st.query_params.clear()
             st.rerun()

# --- MY INFORMATION SECTION ---
st.subheader("📋 My Information")
c1, c2, c3 = st.columns(3)

def green_link(icon_url, label, url):
    # Pure HTML Link wrapper
    code = f"""
    <a href="{url}" target="_self" style="text-decoration: none;">
        <div class="profile-icon-box">
            <img src="{icon_url}" width="40" style="filter: brightness(0) invert(1);">
        </div>
        <div class='profile-label'>{label}</div>
    </a>
    """
    st.markdown(code, unsafe_allow_html=True)

with c1:
    green_link("https://cdn-icons-png.flaticon.com/128/2921/2921822.png", "Select Crop", "?mode=edit_crop")
with c2:
    green_link("https://cdn-icons-png.flaticon.com/128/3898/3898150.png", "Change Lang", "?mode=edit_lang")
with c3:
    green_link("https://cdn-icons-png.flaticon.com/128/2942/2942076.png", "Location", "?mode=edit_loc")

st.markdown(" <br> ", unsafe_allow_html=True)

# --- FEATURES SECTION ---
st.subheader("🌟 Features")
f1, f2, f3 = st.columns(3)

with f1:
    # Crop Care -> Crop Rec Page
    green_link("https://cdn-icons-png.flaticon.com/128/3022/3022938.png", "Crop Care", "Crop_Recommendation")
with f2:
    # Protection -> Pest/Fert Page
    green_link("https://cdn-icons-png.flaticon.com/128/2966/2966486.png", "Protection", "Fertilizer_Advisor")
with f3:
    # Calc -> Fert Page
    green_link("https://cdn-icons-png.flaticon.com/128/2382/2382533.png", "Fertilizer", "Fertilizer_Advisor")

st.markdown("---")

# --- FOOTER BUTTONS ---
col_foot1, col_foot2 = st.columns(2)
with col_foot1:
    if st.button("🚪 Sign Out", use_container_width=True):
        st.session_state.active_user = None
        if 'meta' in st.session_state.user_data:
            st.session_state.user_data['meta']['last_active_phone'] = None
            save_db(st.session_state.user_data)
        st.switch_page("app.py")

with col_foot2:
    # Link to Full Profile Edit Mode? Or just keep duplicate functionality hidden?
    # Keeping the button for full edit
    if st.button("👤 Full Profile", use_container_width=True):
        st.query_params.clear()
        st.query_params["mode"] = "edit_full"
        st.rerun()

if mode == "edit_full":
    with st.container():
        st.markdown("### 📝 Edit Full Details")
        with st.form("full_profile_form"):
            new_name = st.text_input("Full Name", value=user.get('name', ''))
            new_land = st.number_input("Land Size (Acres)", value=float(user.get('land_size', 1.0)))
            new_n = st.number_input("Soil N", value=float(user.get('soil_n', 50)))
            new_p = st.number_input("Soil P", value=float(user.get('soil_p', 50)))
            new_k = st.number_input("Soil K", value=float(user.get('soil_k', 50)))
            if st.form_submit_button("Save All"):
                st.session_state.active_user['name'] = new_name
                st.session_state.active_user['land_size'] = new_land
                st.session_state.active_user['soil_n'] = new_n
                st.session_state.active_user['soil_p'] = new_p
                st.session_state.active_user['soil_k'] = new_k
                save_db(st.session_state.user_data)
                st.success("Saved!")
                st.query_params.clear()
                st.rerun()
            if st.form_submit_button("Cancel"):
                st.query_params.clear()
                st.rerun()

st.markdown(" <br><br> ", unsafe_allow_html=True)
if st.button("🏠 Back to Home", use_container_width=True):
    st.switch_page("app.py")
