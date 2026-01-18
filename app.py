import streamlit as st
import os
import json
import textwrap
import base64
from dotenv import load_dotenv
from utils import apply_custom_style, t, load_db, save_db, render_bottom_nav
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

# --- INLINE CSS OVERRIDE (Forced Orange Theme) ---
# --- APPLY CUSTOM STYLES ---
apply_custom_style(blur_bg=True)

# --- SESSION STATE INITIALIZATION ---
if 'user_data' not in st.session_state:
    st.session_state.user_data = load_db()
if 'current_view' not in st.session_state:
    st.session_state.current_view = 'welcome' 
if 'active_user' not in st.session_state:
    st.session_state.active_user = None 
    # Check for auto-login
    last_phone = st.session_state.user_data.get('meta', {}).get('last_active_phone')
    if last_phone and str(last_phone) in st.session_state.user_data:
        user_obj = st.session_state.user_data[str(last_phone)]
        if user_obj:
            st.session_state.active_user = user_obj
            st.session_state.current_view = 'dashboard'

if 'language' not in st.session_state:
    st.session_state.language = 'English' # Primary Default

# Sync language with active user if logged in
if st.session_state.active_user and 'language' in st.session_state.active_user:
    st.session_state.language = st.session_state.active_user['language']

# --- HELPER FUNCTIONS ---
def get_secret(key):
    try:
        if key in st.secrets:
            return st.secrets[key]
    except:
        pass
    return os.getenv(key)

# --- NAVIGATION FUNCTIONS ---
def navigate_to(view):
    st.session_state.current_view = view
    st.rerun()

def handle_login(phone, password):
    phone = phone.strip()
    password = password.strip()
    user = st.session_state.user_data.get(phone)
    if user:
        if user.get('password') == password: # Basic verification for prototype
            # Sync language choice to user profile
            user['language'] = st.session_state.get('language', 'English')
            st.session_state.active_user = user
            if 'meta' not in st.session_state.user_data: 
                st.session_state.user_data['meta'] = {}
            st.session_state.user_data['meta']['last_active_phone'] = phone
            save_db(st.session_state.user_data)
            navigate_to('dashboard')
        else:
            st.markdown(f"<p style='color: #d32f2f; font-weight: 600; text-align: center; margin-top: 10px;'>{t('wrong_password')}</p>", unsafe_allow_html=True)
    else:
        st.markdown(f"<p style='color: #d32f2f; font-weight: 600; text-align: center; margin-top: 10px;'>{t('user_not_found')}</p>", unsafe_allow_html=True)

def handle_registration(name, phone, city, password):
    phone = phone.strip()
    password = password.strip()
    if phone in st.session_state.user_data:
        st.markdown(f"<p style='color: #e65100; font-weight: 600; text-align: center; margin-top: 10px;'>{t('already_reg')}</p>", unsafe_allow_html=True)
    else:
        new_user = {
            "name": name,
            "phone": phone,
            "city": city,
            "password": password,
            "language": st.session_state.get('language', 'English'),
            "crop": None,
            "land_size": 0.0
        }
        st.session_state.user_data[phone] = new_user
        st.session_state.active_user = new_user
        save_db(st.session_state.user_data) 
        navigate_to('onboarding')

def save_preferences(confirmed_city, main_crop, land_size):
    if st.session_state.active_user:
        phone = st.session_state.active_user['phone']
        st.session_state.user_data[phone]['city'] = confirmed_city
        st.session_state.user_data[phone]['crop'] = main_crop
        st.session_state.user_data[phone]['land_size'] = land_size
        
        # Ensure metadata is updated
        if 'meta' not in st.session_state.user_data: 
            st.session_state.user_data['meta'] = {}
        st.session_state.user_data['meta']['last_active_phone'] = phone
        
        # Update active user object
        st.session_state.active_user = st.session_state.user_data[phone] 
        save_db(st.session_state.user_data) 
        
        navigate_to('dashboard')

# --- VIEW FUNCTIONS ---

def show_welcome_screen():
    # Force Pure White Background and hide canvas
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;700;900&display=swap');
    #bg-canvas { display: none !important; }
    .stApp { background: white !important; font-family: 'Outfit', sans-serif !important; }
    </style>
    """, unsafe_allow_html=True)

    # Load New Premium Logo
    logo_path = os.path.join("assets", "logo_premium_v2.png")
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            logo_encoded = base64.b64encode(f.read()).decode()
        logo_src = f"data:image/png;base64,{logo_encoded}"
    else:
        # Unique 3D Premium Golden Wheat Logo
        logo_src = "https://img.icons8.com/3d-fluency/512/wheat.png"

    # Language Selector (Top Right)
    col_lang, _ = st.columns([1, 4])
    with col_lang:
        st.session_state.language = st.selectbox(
            t('lang_label'),
            ['English', 'Hindi', 'Marathi'],
            index=['English', 'Hindi', 'Marathi'].index(st.session_state.language)
        )
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Welcome Branding (Clean White)
    st.markdown(f"""
    <div style='text-align: center; padding: 60px 20px;'>
        <img src="{logo_src}" width="180" style="filter: drop-shadow(0 15px 30px rgba(0,0,0,0.12));">
        <h1 style='color: #000000; font-family: "Outfit", sans-serif; font-size: 3.8rem; font-weight: 900; margin-top: 30px; letter-spacing: -1.5px; line-height: 1.1;'>{t('app_name')}</h1>
        <p style='font-size: 1.5rem; color: #2C3E50; font-family: "Outfit", sans-serif; font-weight: 600; margin-top: 15px; margin-bottom: 50px; opacity: 0.8;'>{t('tagline')}</p>
    </div>
    """, unsafe_allow_html=True)
        
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        if st.button(t('register'), use_container_width=True, type="primary"):
            navigate_to('register')
        st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)
        if st.button(t('login'), use_container_width=True):
            navigate_to('login')

def show_register():
    # Force Pure White Background and hide canvas
    st.markdown("""
    <style>
    #bg-canvas { display: none !important; }
    .stApp { background: white !important; }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style='text-align: center; padding: 20px 0;'>
        <h2 style='color: #1B2631; font-weight: 900; font-size: 2.2rem;'>{t('register')}</h2>
        <p style='color: #5D6D7E; font-weight: 600;'>{t('reg_sub')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="registration-card" style="background: #ffffff; padding: 40px; border-radius: 20px; border: 1px solid #eee; box-shadow: 0 10px 30px rgba(0,0,0,0.03);">', unsafe_allow_html=True)
        with st.form("reg_form", clear_on_submit=False):
            name = st.text_input(t('full_name'), placeholder=t('ph_name'))
            phone = st.text_input(t('mobile'), placeholder=t('ph_mobile'))
            city = st.text_input(t('city'), placeholder=t('ph_city'))
            st.markdown("---")
            pw1 = st.text_input(t('password'), type="password", placeholder=t('ph_pin'))
            pw2 = st.text_input(t('confirm_password'), type="password")
            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button(t('create_acc'), use_container_width=True)
            if submitted:
                if name and phone and city and pw1 and pw2:
                    if len(pw1) < 4:
                        st.error(t('pass_too_short'))
                    elif pw1 != pw2:
                        st.error(t('pass_mismatch'))
                    else:
                        handle_registration(name, phone, city, pw1)
                else:
                    st.markdown(f"<p style='color: #e65100; font-weight: 600; text-align: center; margin-top: 10px;'>{t('fill_all')}</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button(t('back'), use_container_width=True):
        navigate_to('welcome')

def show_login():
    # Force Pure White Background and hide canvas
    st.markdown("""
    <style>
    #bg-canvas { display: none !important; }
    .stApp { background: white !important; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style='text-align: center; padding: 20px 0;'>
        <h2 style='color: #1B2631; font-weight: 900; font-size: 2.2rem;'>{t('login')}</h2>
        <p style='color: #5D6D7E; font-weight: 600;'>{t('login_sub')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="registration-card" style="background: #ffffff; padding: 40px; border-radius: 20px; border: 1px solid #eee; box-shadow: 0 10px 30px rgba(0,0,0,0.03);">', unsafe_allow_html=True)
        with st.form("login_form"):
            phone = st.text_input(t('enter_mobile'), placeholder=t('ph_login_phone'))
            password = st.text_input(t('enter_password'), type="password")
            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button(t('login_btn'), use_container_width=True)
            if submitted:
                if phone and password:
                    handle_login(phone, password)
                else:
                    st.markdown(f"<p style='color: #e65100; font-weight: 600; text-align: center; margin-top: 10px;'>{t('fill_all')}</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button(t('back'), use_container_width=True):
        navigate_to('welcome')

def show_onboarding():
    # Force Pure White Background and hide canvas
    st.markdown("""
    <style>
    #bg-canvas { display: none !important; }
    .stApp { background: white !important; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style='text-align: center; padding: 20px 0;'>
        <img src="https://cdn-icons-png.flaticon.com/512/3064/3064197.png" width="80" style="margin-bottom: 10px;">
        <h2 style='color: #1B2631; font-weight: 800; margin: 0;'>{t('setup')}</h2>
        <p style='color: #2E7D32; font-weight: 700;'>✅ {t('success_create')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    user = st.session_state.active_user
    with st.container():
        st.markdown('<div class="registration-card" style="background: #ffffff; padding: 40px; border-radius: 20px; border: 1px solid #eee; box-shadow: 0 10px 30px rgba(0,0,0,0.03);">', unsafe_allow_html=True)
        with st.form("onboarding_form"):
            city = st.text_input(t('confirm_city'), value=user['city'])
            crop = st.text_input(t('select_crop'), value="", placeholder=t('crop_placeholder'))
            land = st.number_input(t('land_size'), min_value=0.0, value=1.0, step=0.5)
            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button(t('save'), use_container_width=True)
            if submitted:
                save_preferences(city, crop, land)
        st.markdown('</div>', unsafe_allow_html=True)

def show_dashboard():
    user = st.session_state.active_user
    if not user:
        navigate_to('welcome')
        return

    # --- HEADER SECTION ---
    user_name = user.get('name', 'Farmer').split()[0]
    
    # Greeting logic
    greeting_text = "Hi" if st.session_state.get('language') == 'English' else t('namaste')
    
    # CSS for Typewriter Effect and Font
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;700;800&display=swap');
    
    .typewriter-text {
        overflow: hidden;
        border-right: 3px solid #1B2631;
        white-space: nowrap;
        margin: 0;
        animation: typing 2.5s steps(30, end), blink-caret 0.75s step-end infinite;
        display: inline-block;
        vertical-align: bottom;
        max-width: fit-content;
    }
    @keyframes typing { from { width: 0 } to { width: 100% } }
    @keyframes blink-caret { from, to { border-color: transparent } 50% { border-color: #1B2631; } }
    </style>
    """, unsafe_allow_html=True)

    top_header_html = f"""
    <div style="padding: 10px 5px 0px 5px;">
    <!-- Top Row: Location & Profile -->
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
    <!-- Left Side: Welcome & Location -->
    <div style="display: flex; flex-direction: column; gap: 2px;">
        <div style="font-size: 1.5rem; font-weight: 800; color: #1B2631; font-family: 'Outfit', sans-serif; display:flex; align-items:center; gap:5px;">
            {greeting_text}, <span class="typewriter-text">{user_name}</span> 👋🏽
        </div>
        <div style="display: flex; align-items: center; gap: 6px; opacity: 0.8;">
            <img src="https://img.icons8.com/ios-filled/50/2C3E50/marker.png" width="14">
            <span style="font-size: 0.85rem; font-weight: 600; color: #5D6D7E; font-family: 'Outfit', sans-serif;">{user.get('city', t('india'))}</span>
        </div>
    </div>
    <!-- Actions -->
    <div style="display: flex; align-items: center; gap: 15px;">
    <div style="position: relative; background: white; padding: 8px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
    <img src="https://img.icons8.com/ios-filled/50/2C3E50/bell.png" width="22">
    <div style="position: absolute; top: -2px; right: -2px; width: 10px; height: 10px; background: #FF5252; border-radius: 50%; border: 2px solid white;"></div>
    </div>
    <a href="User_Profile" target="_self" style="text-decoration: none; position: relative; z-index: 1000; cursor: pointer;">
    <img src="https://img.icons8.com/fluency/96/user-male-circle.png" width="45" style="border-radius: 50%; border: 2px solid white; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
    </a>
    </div>
    </div>
    </div>
    """
    st.markdown(top_header_html, unsafe_allow_html=True)

    # Search Bar
    search_query = st.text_input(t('search'), placeholder=t('search_placeholder'), label_visibility="collapsed")
    st.markdown("""
    <style>
    div[data-testid="stTextInput"] > div > div > input {
        background-color: white !important;
        color: #2D3436 !important;
        border: 1px solid rgba(0, 0, 0, 0.05) !important;
        border-radius: 20px !important;
        padding: 12px 25px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.04) !important;
        font-size: 1rem !important;
    }
    div[data-testid="stTextInput"] { margin-bottom: 25px !important; }
    </style>
    """, unsafe_allow_html=True)


    # --- WEATHER BANNER ---
    weather_city = user.get('city', t('delhi'))
    weather_lang = st.session_state.get('language', 'English')
    weather_data, weather_msg = get_weather_data(weather_city, get_secret("WEATHER_API_KEY"), language=weather_lang)

    if weather_data:
        w_temp = int(weather_data['main']['temp'])
        w_desc = weather_data['weather'][0]['description'].title()
        w_hum = weather_data['main']['humidity']
        w_wind = weather_data['wind']['speed']
        w_icon = weather_data['weather'][0]['icon']
        
        # Map OWM icons to High-Quality 3D Icons
        icon_map = {
            "01d": "https://img.icons8.com/fluency/96/sun.png", # Clear Day
            "01n": "https://img.icons8.com/fluency/96/moon-symbol.png", # Clear Night
            "02d": "https://img.icons8.com/fluency/96/partly-cloudy-day.png", # Few Clouds
            "02n": "https://img.icons8.com/fluency/96/partly-cloudy-night.png",
            "03d": "https://img.icons8.com/fluency/96/clouds.png", # Scattered
            "03n": "https://img.icons8.com/fluency/96/clouds.png",
            "04d": "https://img.icons8.com/fluency/96/broken-clouds.png", # Broken
            "04n": "https://img.icons8.com/fluency/96/broken-clouds.png",
            "09d": "https://img.icons8.com/fluency/96/rain.png", # Shower Rain
            "09n": "https://img.icons8.com/fluency/96/rain.png",
            "10d": "https://img.icons8.com/fluency/96/partly-cloudy-rain.png", # Rain
            "10n": "https://img.icons8.com/fluency/96/rainy-night.png",
            "11d": "https://img.icons8.com/fluency/96/storm.png", # Thunderstorm
            "11n": "https://img.icons8.com/fluency/96/storm.png",
            "13d": "https://img.icons8.com/fluency/96/snow.png", # Snow
            "13n": "https://img.icons8.com/fluency/96/snow.png",
            "50d": "https://img.icons8.com/fluency/96/fog-day.png", # Mist
            "50n": "https://img.icons8.com/fluency/96/fog-night.png"
        }
        
        # Default to cloud if not found, or use OWM as absolute fallback
        hq_icon = icon_map.get(w_icon, f"https://openweathermap.org/img/wn/{w_icon}@2x.png")
        
        # Styled Container
        st.markdown(f"""
        <div class="glass-panel weather-banner" style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px; border-radius: 24px; padding: 20px;">
            <div style="display: flex; align-items: center; gap: 20px;">
                <img src="{hq_icon}" width="65" style="filter: drop-shadow(0 4px 6px rgba(0,0,0,0.2));">
                <div>
                    <div style="font-size: 1.6rem; font-weight: 800; color: white; letter-spacing: 0.5px; text-shadow: 0 2px 4px rgba(0,0,0,0.2); font-family: 'Poppins', sans-serif;">
                        {w_temp}°C | {w_desc}
                    </div>
                    <div style="font-size: 0.9rem; font-weight: 500; color: rgba(255,255,255,0.95); margin-top: 4px;">
                        {t('humidity')}: <b>{w_hum}%</b> &nbsp;•&nbsp; {t('wind')}: <b>{w_wind} m/s</b>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if weather_msg and 'mock' not in weather_data:
             st.warning(weather_msg)
    else:
        # Fallback if API fails completely
        st.markdown(f"""
        <div class="glass-panel weather-banner" style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 15px;">
            <div style="display: flex; align-items: center; gap: 15px;">
                <img src="https://img.icons8.com/fluency/96/cloud.png" width="45">
                <div>
                    <div style="font-size: 1.2rem; font-weight: 700; color: white;">{t('weather_err')}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # --- TRUSTED PARTNERS (Infinite Marquee) ---
    st.markdown(f'<div class="section-headline">{t("trusted_partners")}</div>', unsafe_allow_html=True)
    
    # Marquee CSS
    st.markdown("""
    <style>
    .marquee-container {
        width: 100%;
        overflow: hidden;
        white-space: nowrap;
        position: relative;
        padding: 40px 0;
        background: rgba(255,255,255,0.05); /* Lighter glass */
        border-radius: 12px;
        margin-bottom: 25px;
    }
    .marquee-track {
        display: inline-flex;
        animation: scroll 30s linear infinite;
        width: max-content;
    }
    @keyframes scroll {
        0% { transform: translateX(0); }
        100% { transform: translateX(-50%); }
    }
    .brand-item {
        margin: 0 40px;
        display: inline-flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    .brand-item:hover {
        transform: scale(1.1);
    }
    .brand-logo { 
        height: 70px; 
        width: 70px;
        object-fit: contain; 
        margin-bottom: 10px;
        background: white;
        border-radius: 50%;
        padding: 10px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    .brand-name { font-size: 0.8rem; font-weight: 600; color: #1B2631; margin-top: 5px; }
    </style>
    """, unsafe_allow_html=True)

    # List of brands and their verified direct URLs and Websites
    brand_assets = [
        {"name": "Govt of India", "url": "https://cdn-icons-png.flaticon.com/512/924/924915.png", "website": "https://www.india.gov.in/"},
        {"name": "IFFCO", "url": "https://upload.wikimedia.org/wikipedia/en/thumb/0/05/Indian_Farmers_Fertiliser_Cooperative_Logo.svg/250px-Indian_Farmers_Fertiliser_Cooperative_Logo.svg.png", "website": "https://www.iffco.in/"}, 
        {"name": "Mahindra", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Mahindra_logo.svg/1280px-Mahindra_logo.svg.png", "website": "https://www.mahindra.com/"},
        {"name": "Bayer", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f7/Logo_Bayer.svg/1024px-Logo_Bayer.svg.png", "website": "https://www.bayer.com/"},
        {"name": "John Deere", "url": "https://logos-world.net/wp-content/uploads/2020/09/John-Deere-Logo.png", "website": "https://www.deere.co.in/"},
        {"name": "Syngenta", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Syngenta_Logo.svg/250px-Syngenta_Logo.svg.png", "website": "https://www.syngenta.co.in/"},
        {"name": "UPL", "url": "https://upload.wikimedia.org/wikipedia/en/thumb/b/b9/UPL_official_logo.svg/250px-UPL_official_logo.svg.png", "website": "https://www.upl-ltd.com/"},
        {"name": "Nuziveedu", "url": "https://pnghdpro.com/wp-content/themes/pnghdpro/download/social-media-and-brands/nuziveedu-seeds-logo.png", "website": "https://www.nuziveeduseeds.com/"},
        {"name": "Jain Irrigation", "url": "https://companieslogo.com/img/orig/JISLDVREQS.NS_BIG-724215c3.png", "website": "https://www.jains.com/"}
    ]
    
    marquee_html = """<div class="marquee-container"><div class="marquee-track">"""
    
    # Duplicate list for smooth infinite scroll
    for _ in range(2):
        for brand in brand_assets:
            marquee_html += f"""
            <a href="{brand['website']}" target="_blank" style="text-decoration: none;">
                <div class="brand-item">
                    <img src="{brand['url']}" class="brand-logo" alt="{brand['name']}">
                    <div class="brand-name">{brand['name']}</div>
                </div>
            </a>"""
    marquee_html += """</div></div>"""
    
    st.markdown(marquee_html, unsafe_allow_html=True)

    # --- DASHBOARD TOOLS GRID ---
    st.markdown(f'<div class="section-headline">{t("quick_actions")}</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <a href="Crop_Recommendation" target="_self" style="text-decoration: none;">
            <div class="tool-card" style="display: flex; align-items: center; gap: 12px; height: 60px;">
                <img src="https://img.icons8.com/fluency/96/sprout.png" width="28">
                <div style="font-size: 0.9rem; font-weight: 600;">{t('crop_doc')}</div>
            </div>
        </a>
        """, unsafe_allow_html=True)
        st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)
        st.markdown(f"""
        <a href="Market_Prices" target="_self" style="text-decoration: none;">
            <div class="tool-card" style="display: flex; align-items: center; gap: 12px; height: 60px;">
                <img src="https://img.icons8.com/fluency/96/money.png" width="28">
                <div style="font-size: 0.9rem; font-weight: 600;">{t('mandi')}</div>
            </div>
        </a>
        """, unsafe_allow_html=True)

    # Load Irrigation Icon
    irrigation_icon_path = os.path.join("assets", "irrigation_hub_clean.png")
    if os.path.exists(irrigation_icon_path):
        with open(irrigation_icon_path, "rb") as f:
            irr_data = f.read()
            irr_encoded = base64.b64encode(irr_data).decode()
        irrigation_icon_src = f"data:image/png;base64,{irr_encoded}"
    else:
        irrigation_icon_src = "https://img.icons8.com/fluency/96/water-drop.png"

    with c2:
        st.markdown(f"""
        <a href="Fertilizer_Advisor" target="_self" style="text-decoration: none;">
            <div class="tool-card" style="display: flex; align-items: center; gap: 12px; height: 60px;">
                <img src="https://img.icons8.com/fluency/96/test-tube.png" width="28">
                <div style="font-size: 0.9rem; font-weight: 600;">{t('fert_advisor')}</div>
            </div>
        </a>
        """, unsafe_allow_html=True)
        st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)
        st.markdown(f"""
        <a href="Irrigation_Hub" target="_self" style="text-decoration: none;">
            <div class="tool-card" style="display: flex; align-items: center; gap: 12px; height: 60px;">
                <img src="{irrigation_icon_src}" width="28">
                <div style="font-size: 0.9rem; font-weight: 600;">{t('irrigation')}</div>
            </div>
        </a>
        """, unsafe_allow_html=True)

    # --- SERVICES & TOOLS ---
    st.markdown(f'<div class="section-headline">{t("services_tools")}</div>', unsafe_allow_html=True)
    sc1, sc2, sc3, sc4 = st.columns(4)
    
    with sc1:
        st.markdown(f"""
        <a href="Insurance_Calculator" target="_self" style="text-decoration: none;">
            <div class="glass-card" style="text-align: center; padding: 15px 15px !important; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100px;">
                <img src="https://img.icons8.com/fluency/96/shield.png" width="35" style="margin-bottom: 8px;">
                <div style="font-size: 0.75rem; font-weight: 600; line-height: 1.1;">{t('insurance')}</div>
            </div>
        </a>
        """, unsafe_allow_html=True)

    with sc2:
        st.markdown(f"""
        <a href="Farming_Knowledge" target="_self" style="text-decoration: none;">
            <div class="glass-card" style="text-align: center; padding: 15px 15px !important; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100px;">
                <img src="https://img.icons8.com/fluency/96/book.png" width="35" style="margin-bottom: 8px;">
                <div style="font-size: 0.75rem; font-weight: 600; line-height: 1.1;">{t('knowledge')}</div>
            </div>
        </a>
        """, unsafe_allow_html=True)

    with sc3:
        st.markdown(f"""
        <a href="Yield_Prediction" target="_self" style="text-decoration: none;">
            <div class="glass-card" style="text-align: center; padding: 15px 15px !important; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100px;">
                <img src="https://img.icons8.com/fluency/96/bar-chart.png" width="35" style="margin-bottom: 8px;">
                <div style="font-size: 0.75rem; font-weight: 600; line-height: 1.1;">{t('yield_pred')}</div>
            </div>
        </a>
        """, unsafe_allow_html=True)

    with sc4:
        st.markdown(f"""
        <a href="Weather_Info" target="_self" style="text-decoration: none;">
            <div class="glass-card" style="text-align: center; padding: 15px 5px !important; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100px;">
                <img src="https://img.icons8.com/fluency/96/partly-cloudy-day.png" width="35" style="margin-bottom: 8px;">
                <div style="font-size: 0.75rem; font-weight: 600; line-height: 1.1;">{t('weather_det')}</div>
            </div>
        </a>
        """, unsafe_allow_html=True)

    # Use the transparent black robot farmer icon
    ai_icon_path = os.path.join("assets", "black_robot_farmer_final.png")
    if os.path.exists(ai_icon_path):
        with open(ai_icon_path, "rb") as f:
            data = f.read()
            encoded = base64.b64encode(data).decode()
        ai_icon_src = f"data:image/png;base64,{encoded}"
    else:
        ai_icon_src = "https://img.icons8.com/3d-fluency/94/robot-2.png" 

    st.markdown(f"""
    <style>
    @keyframes float {{
        0% {{ transform: translate(0px, 0px) rotate(0deg); }}
        25% {{ transform: translate(10px, -5px) rotate(2deg); }}
        50% {{ transform: translate(0px, -10px) rotate(0deg); }}
        75% {{ transform: translate(-10px, -5px) rotate(-2deg); }}
        100% {{ transform: translate(0px, 0px) rotate(0deg); }}
    }}
    .floating-agent {{
        animation: float 5s ease-in-out infinite;
    }}
    </style>
    <a href="AI_Agronomist" target="_self" style="text-decoration: none;">
        <div class="ai-banner" style="display: flex; align-items: center; justify-content: center; gap: 30px; margin-top: 40px; margin-bottom: 80px; position: relative; overflow: visible; background: transparent !important; border: none !important; box-shadow: none !important;">
            <div style="display: flex; align-items: center; gap: 15px;">
                <img src="{ai_icon_src}" width="80" class="floating-agent" style="margin-left: -5px;">
                <div>
                    <div style="font-size: 1.3rem; font-weight: 800; color: #1B2631; text-shadow: 0 2px 4px rgba(255,255,255,0.5);">{t('ask_ai_title')}</div>
                    <div style="font-size: 0.85rem; font-weight: 600; color: #1B2631; opacity: 1;">{t('ask_ai_subtitle')}</div>
                </div>
            </div>
            <div style="background: transparent !important; border: 2px solid #1B2631; padding: 8px 20px; border-radius: 25px; font-size: 0.9rem; font-weight: 700; color: #1B2631;">
                {t('chat_now')}
            </div>
        </div>
    </a>
    """, unsafe_allow_html=True)


    
    # --- RENDER BOTTOM NAV ---
    render_bottom_nav(active_tab='Home')
    st.markdown("<br><br><br>", unsafe_allow_html=True)


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
