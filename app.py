import streamlit as st
import os
import json
from dotenv import load_dotenv
from utils import apply_custom_style, t, load_db, save_db
from logic import get_weather_data
from datetime import datetime

# Load environment variables
load_dotenv()

# Page Config
st.set_page_config(
    page_title="Farmer Super App",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply Custom "Mobile App" Styles
apply_custom_style()

# --- SESSION STATE INITIALIZATION ---
if 'current_view' not in st.session_state:
    st.session_state.current_view = 'welcome' 
if 'user_data' not in st.session_state:
    # LOAD FROM DISK
    st.session_state.user_data = load_db()
if 'active_user' not in st.session_state:
    st.session_state.active_user = None 
    # Check for auto-login
    # We check if 'last_active_phone' exists in metadata
    last_phone = st.session_state.user_data.get('meta', {}).get('last_active_phone')
    if last_phone and str(last_phone) in st.session_state.user_data:
        # Check if the user object is valid
        user_obj = st.session_state.user_data[str(last_phone)]
        if user_obj:
            st.session_state.active_user = user_obj
            st.session_state.current_view = 'dashboard'

if 'language' not in st.session_state:
    st.session_state.language = 'English' # Default

# --- NAVIGATION FUNCTIONS ---
def navigate_to(view):
    st.session_state.current_view = view
    st.rerun()

def handle_login(phone):
    # Retrieve user from session state DB (loaded from disk)
    user = st.session_state.user_data.get(phone)
    if user:
        st.session_state.active_user = user
        # Update Metadata for Auto-Login
        if 'meta' not in st.session_state.user_data: 
            st.session_state.user_data['meta'] = {}
        st.session_state.user_data['meta']['last_active_phone'] = phone
        save_db(st.session_state.user_data)
        
        st.success(f"{t('namaste')}, {user['name']}!")
        navigate_to('dashboard')
    else:
        st.error(t('user_not_found'))

def handle_registration(name, phone, city):
    if phone in st.session_state.user_data:
        st.error(t('already_reg'))
    else:
        # Create new user profile layout
        new_user = {
            "name": name,
            "phone": phone,
            "city": city,
            "crop": None,
            "land_size": 0.0
        }
        st.session_state.user_data[phone] = new_user
        st.session_state.active_user = new_user
        # Save partially but don't set as active/autologin until fully onboarded? 
        # Actually, let's save now so if they quit they can login.
        save_db(st.session_state.user_data) 
        navigate_to('onboarding')

def save_preferences(confirmed_city, main_crop, land_size):
    if st.session_state.active_user:
        phone = st.session_state.active_user['phone']
        st.session_state.user_data[phone]['city'] = confirmed_city
        st.session_state.user_data[phone]['crop'] = main_crop
        st.session_state.user_data[phone]['land_size'] = land_size
        
        # Save Metadata for Auto-Login
        if 'meta' not in st.session_state.user_data: 
            st.session_state.user_data['meta'] = {}
        st.session_state.user_data['meta']['last_active_phone'] = phone
        
        st.session_state.active_user = st.session_state.user_data[phone] 
        save_db(st.session_state.user_data) # PERSIST TO DISK
        
        navigate_to('dashboard')

# --- VIEW FUNCTIONS ---

def show_welcome_screen():
    # Language Selector (Top Right)
    col_lang, _ = st.columns([1, 4])
    with col_lang:
        st.session_state.language = st.selectbox(
            "🌐 Language / भाषा",
            ['English', 'Hindi', 'Marathi'],
            index=['English', 'Hindi', 'Marathi'].index(st.session_state.language)
        )

    st.markdown(f"""
    <div style='text-align: center; padding: 20px 20px;'>
        <img src="https://cdn-icons-png.flaticon.com/512/3022/3022938.png" width="120">
        <h1 style='color: #2e7d32; font-size: 3rem;'>{t('app_name')}</h1>
        <p style='font-size: 1.5rem; color: #555; font-style: italic;'>{t('tagline')}</p>
    </div>
    """, unsafe_allow_html=True)

    # --- ABOUT SECTION ---
    with st.expander("ℹ️ About the App / ऐप के बारे में"):
        st.markdown("""
        **Farmer Super App** is your all-in-one digital companion for modern farming.
        
        **Features:**
        - 🌱 **Crop Doctor:** AI-based disease diagnosis.
        - 🧪 **Fertilizer Advisor:** Personalized nutrient recommendations.
        - ☁️ **Weather:** Real-time location-based forecasts.
        - 💰 **Mandi Prices:** Live market rates from nearby mandis.
        - 🤖 **AI Agronomist:** 24/7 Chatbot for any farming question.
        
        *Built with ❤️ for Indian Farmers.*
        """)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(t('register'), use_container_width=True):
            navigate_to('register')
        if st.button(t('login'), use_container_width=True):
            navigate_to('login')

def show_register():
    st.markdown(f"## 📝 {t('register')}")
    with st.form("reg_form"):
        name = st.text_input(t('full_name'))
        phone = st.text_input(t('mobile'))
        city = st.text_input(t('city'))
        submitted = st.form_submit_button(t('create_acc'))
        if submitted:
            if name and phone and city:
                handle_registration(name, phone, city)
            else:
                st.error(t('fill_all'))
    if st.button(t('back')):
        navigate_to('welcome')

def show_login():
    st.markdown(f"## 🔑 {t('login')}")
    with st.form("login_form"):
        phone = st.text_input(t('enter_mobile'))
        submitted = st.form_submit_button(t('login_btn'))
        if submitted:
            handle_login(phone)
    if st.button(t('back')):
        navigate_to('welcome')

def show_onboarding():
    st.markdown(f"## {t('setup')}")
    st.success(t('success_create'))
    
    user = st.session_state.active_user
    with st.form("onboarding_form"):
        city = st.text_input(t('confirm_city'), value=user['city'])
        crop = st.text_input(t('select_crop'), value="", placeholder="e.g. Soyabean")
        land = st.number_input(t('land_size'), min_value=0.0, value=1.0, step=0.5)
        
        submitted = st.form_submit_button(t('save'))
        if submitted:
            save_preferences(city, crop, land)

def show_dashboard():
    user = st.session_state.active_user
    if not user:
        navigate_to('welcome')
        return

    # --- CUSTOM HEADER (BigHaat Style) ---
    h_col1, h_col2, h_col3 = st.columns([1, 4, 1])
    
    with h_col1:
        # Profile Icon (Green Turban / Farmer Icon)
        st.markdown('<img src="https://cdn-icons-png.flaticon.com/512/3022/3022938.png" class="icon-image" width="50" style="margin: 0;">', unsafe_allow_html=True)
        if st.button("👤", key="btn_profile_icon"):
            st.switch_page("pages/10_👤_User_Profile.py")

    with h_col2:
        st.markdown(f"<h2 style='margin: 0; padding-top: 10px; color: #2E7D32;'>{t('app_name')}</h2>", unsafe_allow_html=True)

    with h_col3:
        if st.button("🚪", key="btn_logout_icon", help=t('logout')):
            st.session_state.active_user = None
            if 'meta' in st.session_state.user_data:
                st.session_state.user_data['meta']['last_active_phone'] = None
                save_db(st.session_state.user_data)
            st.session_state.current_view = 'welcome'
            st.rerun()

    # --- SEARCH BAR ---
    # --- SEARCH BAR ---
    search_query = st.text_input("Search", placeholder="Search for products, crops, or advice...  ", label_visibility="collapsed")
    
    if search_query:
        q = search_query.lower()
        if any(x in q for x in ['crop', 'disease', 'sick', 'plant']):
            st.switch_page("pages/01_🌱_Crop_Recommendation.py")
        elif any(x in q for x in ['yield', 'profit', 'production', 'estimate']):
            st.switch_page("pages/09_📊_Yield_Prediction.py")
        elif any(x in q for x in ['price', 'mandi', 'market', 'rate']):
            st.switch_page("pages/05_💰_Market_Prices.py")
        elif any(x in q for x in ['rain', 'weather', 'forecast']):
            st.switch_page("pages/06_☁️_Weather_Info.py")
        elif any(x in q for x in ['fertilizer', 'soil', 'npk', 'nutrient']):
             st.switch_page("pages/02_🧪_Fertilizer_Advisor.py")
        elif any(x in q for x in ['insurance', 'premium', 'claim']):
             st.switch_page("pages/04_🛡️_Insurance_Calculator.py")
        else:
            # Default to AI Chat
            st.session_state.ai_query = search_query
            st.switch_page("pages/08_🤖_AI_Agronomist.py")
    
    # Weather Widget (Dynamic City from User Profile)
    # st.markdown(f"### {t('location')}: {user['city']}") # Removed redundant header
    
    # Allow checking another city (Hidden or moved to separate section if needed, keeping simple for now)
    # search_city = st.text_input("Check another city", ...) 
    target_city = user['city'] # Default to user city for cleaner look
    
    api_key = os.getenv("WEATHER_API_KEY")
    
    api_key = os.getenv("WEATHER_API_KEY")
    weather_data, error = get_weather_data(target_city, api_key)
    
    if weather_data:
        temp = round(weather_data['main']['temp'])
        desc = weather_data['weather'][0]['description']
        icon = weather_data['weather'][0]['icon']
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #0288d1, #26c6da); color: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); margin-bottom: 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h2 style="margin: 0; color: white !important;">{temp}°C</h2>
                    <p style="margin: 0; font-size: 1.2rem;">{desc.title()}</p>
                    <p style="margin: 0; opacity: 0.8;">📍 {user['city']}</p>
                </div>
                <img src="http://openweathermap.org/img/wn/{icon}@2x.png" width="80">
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning(f"{t('weather_err')}: {error}")

    # --- BRAND PARTNERS SECTION ---
    st.markdown(f"### 🏭 Trusted Brands")
    b1, b2, b3, b4 = st.columns(4)
    with b1:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Syngenta_logo.svg/320px-Syngenta_logo.svg.png", width=80)
    with b2:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/f/f7/Logo_Bayer.svg/320px-Logo_Bayer.svg.png", width=80)
    with b3:
        st.image("https://upload.wikimedia.org/wikipedia/en/thumb/b/b9/UPL_official_logo.svg/320px-UPL_official_logo.svg.png", width=80)
    with b4:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Tata_logo.svg/320px-Tata_logo.svg.png", width=70)

    # Feature Grid - Section 1: Farm Management (Kheti Badi)
    st.markdown(f"### 🚜 {t('quick_actions')}")
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.markdown(f'<a href="Crop_Recommendation" target="_self"><img src="https://cdn-icons-png.flaticon.com/128/3022/3022938.png" class="icon-image" width="70"></a>', unsafe_allow_html=True)
        st.markdown(f'<p class="nav-label">{t("crop_doc")}</p>', unsafe_allow_html=True)
        
    with c2:
        st.markdown(f'<a href="Fertilizer_Advisor" target="_self"><img src="https://cdn-icons-png.flaticon.com/128/9672/9672439.png" class="icon-image" width="70"></a>', unsafe_allow_html=True)
        st.markdown(f'<p class="nav-label">{t("fert_advisor")}</p>', unsafe_allow_html=True)
        
    with c3:
        st.markdown(f'<a href="Irrigation_Hub" target="_self"><img src="https://cdn-icons-png.flaticon.com/128/3203/3203067.png" class="icon-image" width="70"></a>', unsafe_allow_html=True)
        st.markdown(f'<p class="nav-label">{t("irrigation")}</p>', unsafe_allow_html=True)
        
    with c4:
        st.markdown(f'<a href="Yield_Prediction" target="_self"><img src="https://cdn-icons-png.flaticon.com/128/3094/3094851.png" class="icon-image" width="70"></a>', unsafe_allow_html=True)
        st.markdown(f'<p class="nav-label">{t("yield_pred")}</p>', unsafe_allow_html=True)

    # Feature Grid - Section 2: Services & Info (Suvidha)
    st.markdown("### 🌍 Services")
    c5, c6, c7, c8 = st.columns(4)
    
    with c5:
        st.markdown(f'<a href="Weather_Info" target="_self"><img src="https://cdn-icons-png.flaticon.com/128/1163/1163661.png" class="icon-image" width="70"></a>', unsafe_allow_html=True)
        st.markdown(f'<p class="nav-label">{t("weather_det")}</p>', unsafe_allow_html=True)
        
    with c6:
        st.markdown(f'<a href="Market_Prices" target="_self"><img src="https://cdn-icons-png.flaticon.com/128/2230/2230606.png" class="icon-image" width="70"></a>', unsafe_allow_html=True)
        st.markdown(f'<p class="nav-label">{t("mandi")}</p>', unsafe_allow_html=True)
        
    with c7:
        st.markdown(f'<a href="Insurance_Calculator" target="_self"><img src="https://cdn-icons-png.flaticon.com/128/2966/2966486.png" class="icon-image" width="70"></a>', unsafe_allow_html=True)
        st.markdown(f'<p class="nav-label">{t("insurance")}</p>', unsafe_allow_html=True)
        
    with c8:
        st.markdown(f'<a href="Farming_Knowledge" target="_self"><img src="https://cdn-icons-png.flaticon.com/128/2436/2436636.png" class="icon-image" width="70"></a>', unsafe_allow_html=True)
        st.markdown(f'<p class="nav-label">{t("knowledge")}</p>', unsafe_allow_html=True)

    # AI Section (Full Width)
    st.markdown("### 🤖 Expert Help")
    if st.button(f"{t('ask_ai')} (Chat Now)", use_container_width=True):
        st.switch_page("pages/08_🤖_AI_Agronomist.py")


# --- MAIN ROUTER ---
if st.session_state.current_view == 'welcome':
    show_welcome_screen()
elif st.session_state.current_view == 'register':
    show_register()
elif st.session_state.current_view == 'login':
    show_login()
elif st.session_state.current_view == 'onboarding':
    show_onboarding()
elif st.session_state.current_view == 'dashboard':
    show_dashboard()
