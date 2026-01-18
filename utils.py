import json
import os
import streamlit as st
import base64

# --- CUSTOM CSS ---
def apply_custom_style(blur_bg=True):
    # Determine blur value
    blur_css = "filter: blur(10px); -webkit-filter: blur(10px); transform: scale(1.05);" if blur_bg else ""
    
    # --- AESTHETIC BACKGROUND ELEMENTS ---
    st.markdown("""
    <div id="bg-canvas"></div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

        /* MOBILE GREEN BACKGROUND -> SCENIC BACKGROUND */
        #bg-canvas {{
            position: fixed;
            top: 0; 
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: -3;
            background: url("https://images.unsplash.com/photo-1625246333195-58f214f063ce?q=80&w=2600&auto=format&fit=crop") no-repeat center center fixed;
            background-size: cover;
            {blur_css}
        }}

        /* 1. OVERRIDE DEFAULT BACKGROUND */
        .stApp {{
            background: rgba(255, 255, 255, 0.4) !important; /* Semi-transparent overlay for readability */
            font-family: 'Poppins', sans-serif !important;
            color: #1B2631 !important;
        }}

        /* HIDE SIDEBAR NAVIGATION */
        [data-testid="stSidebar"], [data-testid="stSidebarNav"] {{
            display: none !important;
        }}

        /* 2. MAIN CONTAINER */
        .block-container {{
            padding-top: 2rem;
            padding-bottom: 8rem;
            max-width: 100% !important;
        }}

        /* 3. MOBILE SYSTEM CARDS (Flat & Clean) -> REPLACED WITH ORANGE THEME */
        .glass-panel, .glass-card, .tool-card {{
            background: linear-gradient(135deg, #FF9800 0%, #EF6C00 100%) !important; /* Premium Orange Gradient */
            border-radius: 24px !important;
            padding: 16px !important;
            border: 1px solid rgba(255,255,255,0.2) !important;
            box-shadow: 0 4px 15px rgba(239, 108, 0, 0.3) !important;
            transition: all 0.2s ease;
            color: white !important; /* Text is now White */
            text-decoration: none !important;
        }}
        .ai-banner {{ background: transparent !important; }}
        
        .tool-card:active {{
            transform: scale(0.97);
            background: linear-gradient(135deg, #F57C00 0%, #E65100 100%) !important;
        }}

        /* 4. HEADLINES */
        .section-headline {{
            font-size: 1.1rem;
            font-weight: 700;
            color: #283747;
            margin: 20px 0 12px 0;
            padding-left: 5px;
        }}

        /* 5. WEATHER & AI BANNER GRADIENTS */
        .weather-banner {{
            background: linear-gradient(135deg, #5DADE2 0%, #2E86C1 100%) !important;
            color: white !important;
        }}
        .ai-banner {{
            background: linear-gradient(135deg, #DEEB8E 0%, #F1C40F 100%) !important;
            color: #1B2631 !important;
        }}

        /* 6. BOTTOM NAVIGATION (STYLIZED) */
        .bottom-nav {{
            position: fixed;
            bottom: 0px;
            left: 0;
            width: 100%;
            background: #FFFFFF;
            padding: 12px 10px 25px 10px;
            display: flex;
            justify-content: space-around;
            align-items: center;
            border-top: 1px solid #EBEDEF;
            z-index: 10000;
            box-shadow: 0 -4px 15px rgba(0,0,0,0.05);
        }}
        .nav-link {{
            text-align: center;
            text-decoration: none;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 4px;
        }}
        .nav-link.active {{
            background: #C8E6C9;
            padding: 8px 15px;
            border-radius: 12px;
        }}
        .nav-icon {{ height: 24px; width: 24px; object-fit: contain; }}
        .nav-label {{ font-size: 0.7rem; font-weight: 600; color: #5D6D7E; }}
        .active .nav-label {{ color: #1B5E20; }}

        /* Typography */
        h1, h2, h3, p, span, div {{
            color: inherit;
        }}

        /* Card Icon Wrappers */
        .card-icon-wrapper {{
            border-radius: 16px !important;
            padding: 8px !important;
        }}


        .glass-card:hover {{
            transform: translateY(-5px);
            background: linear-gradient(135deg, rgba(255,255,255,0.35), rgba(255,255,255,0.25));
        }}

        .card-icon {{
            width: 70px;
            margin-bottom: 12px;
            filter: drop-shadow(0 4px 6px rgba(0,0,0,0.1));
        }}
        
        .card-title {{
            font-size: 1.1rem;
            font-weight: 600;
            color: white;
            text-shadow: 0 1px 2px rgba(0,0,0,0.2);
        }}

        /* 5. SERVICES CARD (Wide) */
        .services-card {{
            width: 55%; 
            margin: 40px auto; 
            padding: 20px 40px;
            display: flex;
            flex-direction: row; 
            gap: 40px;
            justify-content: center;
        }}
        
        .service-item {{
             display: flex;
             flex-direction: column;
             align-items: center;
             color: white;
             font-size: 0.9rem;
        }}

        /* 7. HEADER BANNER (Golden Wheat) */
        .header-banner {{
            background: linear-gradient(rgba(0,0,0,0.2), rgba(0,0,0,0.2)), url("https://images.unsplash.com/photo-1500382017468-9049fed747ef?q=80&w=2600&auto=format&fit=crop") center/cover;
            border-radius: 30px;
            padding: 40px 20px;
            text-align: center;
            color: white;
            box-shadow: 0 15px 40px rgba(0,0,0,0.3);
            margin-bottom: 40px;
            border: 2px solid rgba(255, 255, 255, 0.4);
        }}
        
        .header-banner h1 {{
            font-family: 'Poppins', sans-serif;
            font-weight: 700;
            text-shadow: 0 4px 12px rgba(0,0,0,0.5);
            letter-spacing: 1px;
        }}

        /* 6. EXPERT BUTTON (Client Exact Reference) */
        .ai-btn-wrapper {{
            display:flex;
            justify-content:center;
            margin-top:40px;
        }}

        .ai-btn {{
            padding:16px 48px;
            border-radius:40px;
            font-size:17px;
            font-weight:600;
            color:#ffffff !important;
            text-decoration: none !important;
            background: linear-gradient(
                90deg,
                #66BB6A 0%,
                #FFCC80 100%
            );
            backdrop-filter: blur(10px);
            box-shadow:
                inset 0 1px 1px rgba(255,255,255,0.4),
                0 12px 25px rgba(0,0,0,0.25);
            transition: all 0.3s ease;
            cursor:pointer;
            display: inline-block;
        }}

        .ai-btn:hover {{
            transform: translateY(-2px);
            box-shadow:
                inset 0 1px 1px rgba(255,255,255,0.5),
                0 18px 35px rgba(0,0,0,0.35);
            color: #ffffff !important;
        }}

        /* 1. Crop Doctor - LUSH GREEN GRADIENT */
        .card-green {{
            background: linear-gradient(135deg, #E6F4D7 0%, #81C784 100%) !important;
            height: 260px;
        }}
        
        /* 2. Fertilizer - ORANGE-TO-GREEN GRADIENT (As per prompt) */
        .card-orange {{
            background: linear-gradient(180deg, #DCECC8 0%, #FFB74D 100%) !important;
            height: 260px;
        }}
        
        /* 3. Mandi - GREEN GLASS */
        .card-teal {{
            background: linear-gradient(180deg, #DCECC8 0%, #FFB74D 100%) !important;
            height: 120px;
        }}
        
        /* 4. Weather - GREEN GLASS */
        .card-blue {{
            background: linear-gradient(135deg, #E6F4D7 10%, #81C784 95%) !important;
            height: 120px;
        }}
        
        /* 5. Services - GREEN GLASS STRIP */
        .card-services {{
            background: linear-gradient(90deg, #66BB6A 0%, #FFCCBC 100%) !important;
            height: 120px;
            padding: 0 20px;
        }}

        /* 6. Irrigation - WATER BLUE GRADIENT */
        .card-water {{
            background: linear-gradient(135deg, #E6F4D7 10%, #81C784 95%) !important;
            height: 200px;
        }}

        /* 7. Yield - GOLDEN GROWTH GRADIENT */
        .card-gold {{
            background: linear-gradient(90deg, #66BB6A 0%, #FFCCBC 100%) !important;
            height: 200px;
        }}
        
        /* Hide Default Streamlit Elements */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}} w
        /* 10. HIDE SIDEBAR & TOP HEADER COMPLETELY */
        [data-testid="stSidebar"], div[data-testid="stSidebar"] {{
            display: none !important;
        }}
        
        button[data-testid="stBaseButton-headerNoPadding"], 
        header[data-testid="stHeader"] {
            display: none !important;
            height: 0 !important;
            visibility: hidden !important;
        }

        /* Adjust page top padding since header is gone */
        .stApp {{
            margin-top: -50px !important;
        }}

        /* 8. UTILITIES (Vision Pro) */
        .glass-panel {{
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(20px);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
        }}
        
        .glass-container {{
            padding: 20px; 
            border-radius: 20px; 
            background: rgba(255,255,255,0.05); 
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
            margin-bottom: 20px;
        }}

        .result-card {{
            background: rgba(255, 255, 255, 0.9);
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            border-left: 6px solid #4CAF50;
            margin-bottom: 15px;
            transition: transform 0.2s;
        }}
        .result-card:hover {{ transform: translateY(-3px); }}
        .result-label {{ font-size: 0.85rem; color: #666; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }}
        .result-val {{ font-size: 1.5rem; color: #2E7D32; font-weight: 700; }}
        

        /* 9. GLOBAL BUTTON STYLES */
        div.stButton > button, div[data-testid="stFormSubmitButton"] > button {{
            background: linear-gradient(90deg, #FF9800 0%, #F57F17 100%) !important; /* Warm Orange/Gold */
            color: white !important;
            border: none !important;
            padding: 12px 24px !important;
            border-radius: 30px !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            box-shadow: 0 4px 10px rgba(245, 127, 23, 0.3) !important;
            transition: all 0.3s ease !important;
            width: 100%;
        }}

        div.stButton > button:hover, div[data-testid="stFormSubmitButton"] > button:hover {{
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 15px rgba(245, 127, 23, 0.4) !important;
            background: linear-gradient(90deg, #F57C00 0%, #E65100 100%) !important;
        }}

        div.stButton > button:active, div[data-testid="stFormSubmitButton"] > button:active {{
            transform: translateY(1px) !important;
            box-shadow: 0 2px 5px rgba(245, 127, 23, 0.2) !important;
        }}

        </style>
    """, unsafe_allow_html=True)

# --- TRANSLATIONS ---
TRANSLATIONS = {
    'English': {
        # App.py
        'app_name': 'Farmer Super App',
        'tagline': 'Your smart farming companion',
        'register': '🚀 Register (New User)',
        'login': '🔑 Login (Existing User)',
        'reg_sub': 'Start your journey with us today',
        'login_sub': 'Welcome back, farmer',
        'welcome_user': 'Welcome, Farmer! 🚜',
        'namaste': 'Namaste',
        'location': '📍 Location',
        'weather_err': '⚠️ Weather Unavailable',
        'quick_actions': '⚡ Quick Actions',
        'updates': '📢 Latest Updates',
        'crop_doc': 'Crop Doctor',
        'insurance': 'Insurance Calc',
        'mandi': 'Mandi Rates',
        'weather_det': 'Weather Detail',
        'trusted_partners': 'Trusted by Farmers & Agri Partners',
        'services_tools': 'Services & Tools',
        'humidity': 'Humidity',
        'wind': 'Wind',
        'ask_ai_title': 'Ask AI Expert 🤖',
        'ask_ai_subtitle': 'Get instant expert advice on crops & diseases',
        'chat_now': 'Chat Now ➔',
        'search': 'Search',
        'search_placeholder': '🔍 Search crops, mandi, or advice...',
        'ai_greet': 'Hello! I am your AI Agronomist. Ask me anything about pest control, crop diseases, or fertilizer schedules! 🚜',
        'ai_title': 'AI Agronomist',
        'ai_sub': 'Your 24/7 Smart Farming Assistant',
        'ai_placeholder': 'Ask me anything: Pests, crops, or fertilizers...',
        'weather_forecast': 'Real-time field conditions & forecast',
        'select_loc': '📍 Select Location',
        'feels_like': 'Feels like',
        'cond_details': 'Conditions Details',
        'wind_speed': 'Wind Speed',
        'max_temp': 'Max Temp',
        'min_temp': 'Min Temp',
        'smart_water': 'Smart Water Management',
        'rec_schedule': 'Recommended Schedule',
        'liters': 'Liters',
        'standard_freq': 'Standard schedule (every 10-12 days).',
        'sandy_freq': 'Sandy soil drains fast. Irrigate frequently (every 5-7 days).',
        'clayey_freq': 'Clay retains water. Irrigate less frequently (every 12-15 days).',
        'loamy_freq': 'Loamy soil is balanced. Irrigate every 8-10 days.',
        'ins_info_title': '📚 Govt Scheme Information',
        'ins_info_content': '- **PMFBY**: Best for yield loss due to non-preventable risks.\n- **WBCIS**: Pays if weather data deviates from normal.\n- **KCC Linkage**: Mandatory for KCC loan holders.',
        'mandi_sub': 'Live regional market rates and trends',
        'price_analysis': 'Real-Time Price Analysis & Forecast',
        'hist_trend': 'Historical Trend',
        'market_rates': 'Market Rates (Today)',
        'ai_forecast': 'AI Forecast (3-Days)',
        'chart_title': 'Live Market Analysis & Prediction',
        'date': 'Date',
        'price_qt': 'Price (₹/Qt)',
        'col_market': 'Market',
        'col_min': 'Min Price (₹/Qt)',
        'col_max': 'Max Price (₹/Qt)',
        'col_modal': 'Modal Price (₹/Qt)',
        'col_kg': 'Price (₹/Kg)',
        'col_date': 'Date',
        'soil_loamy': 'Normal/Loamy',
        'soil_sandy': 'Sandy (Low Water Retention)',
        'soil_clayey': 'Clayey (Water Logging Risk)',
        'soil_saline': 'Saline/Degraded',
        'weather_normal': 'Normal Rainfall',
        'weather_drought': 'Drought/Low Rainfall',
        'weather_heavy_rain': 'Heavy Rainfall/Flooding',
        'weather_heatwave': 'Heatwave',
        'soil_sandy_simple': 'Sandy',
        'soil_clayey_simple': 'Clayey',
        'soil_loamy_simple': 'Loamy',
        'season_kharif': 'Kharif',
        'season_rabi': 'Rabi',
        'season_zaid': 'Zaid',
        'season_year': 'Whole Year',
        'st_mh': 'Maharashtra',
        'st_pb': 'Punjab',
        'st_up': 'Uttar Pradesh',
        'st_gj': 'Gujarat',
        'st_hr': 'Haryana',
        'st_mp': 'Madhya Pradesh',
        'st_ka': 'Karnataka',
        'st_wb': 'West Bengal',
        'st_br': 'Bihar',
        'st_rj': 'Rajasthan',
        'st_ap': 'Andhra Pradesh',
        'st_tg': 'Telangana',
        'st_tn': 'Tamil Nadu',
        'st_od': 'Odisha',
        'st_ot': 'Other',
        'ask_ai': 'Ask AI Expert',
        'knowledge': 'Knowledge Hub',
        'fert_advisor': 'Fertilizer Advisor',
        'irrigation': 'Irrigation Hub',
        'yield_pred': 'Yield Prediction',
        'logout': '⬅️ Logout',
        'full_name': 'Full Name',
        'mobile': 'Mobile Number',
        'city': 'City',
        'create_acc': 'Create Account',
        'back': '⬅️ Back',
        'login_btn': 'Login',
        'enter_mobile': 'Enter Registered Mobile Number',
        'setup': '⚙️ First-Time Setup',
        'success_create': 'Account created! Let\'s personalize your experience.',
        'confirm_city': 'Confirm Your City',
        'select_crop': 'Select Main Crop',
        'save': 'Save & Continue',
        'user_not_found': 'User not found. Please Register.',
        'already_reg': 'Phone number already registered. Please Login.',
        'fill_all': 'Please fill all details.',
        'land_size': 'Land Size (Acres)',
        'password': 'Create Password (PIN)',
        'confirm_password': 'Confirm Password',
        'enter_password': 'Enter Password',
        'wrong_password': '❌ Incorrect Password!',
        'pass_mismatch': '❌ Passwords do not match!',
        'pass_too_short': '❌ Password must be at least 4 digits!',
        'total_premium': 'Total Premium',
        'updated': 'Updated Successfully!',
        'auth_success': '✅ Authentication Successful!',
        'nav_home': 'Home',
        'nav_crops': 'Crops',
        'nav_weather': 'Weather',
        'nav_chat': 'Expert',
        'nav_about': 'Knowledge',
        'prof_my_info': '📋 My Information',
        'prof_features': '🌟 Features',
        'prof_select_crop': 'Select Crop',
        'prof_change_lang': 'Change Lang',
        'prof_location': 'Location',
        'prof_full_profile': 'Full Profile',
        'prof_sign_out': 'Sign Out',
        'prof_crop_care': 'Crop Care',
        'prof_protection': 'Protection',
        'prof_fertilizer': 'Fertilizer',
        'prof_back_home': 'Back to Home',
        'logic_title': '💡 Recommendation Logic',
        'highly_suitable': 'Highly Suitable',
        'stage_pre_sowing': 'Pre-Sowing / Basal',
        'stage_veg': 'Vegetative / Growth',
        'stage_flowering': 'Flowering / Fruiting',
        'stage_post_harvest': 'Post-Harvest',
        
        # Crop Recommendation
        'crop_title': '🌱 Smart Crop Recommendation',
        'soil_health': 'Soil Health Card Data',
        'nitrogen': 'Nitrogen (N) - Ratio',
        'phosphorus': 'Phosphorus (P) - Ratio',
        'potassium': 'Potassium (K) - Ratio',
        'ph_level': 'Soil pH Level (0-14)',
        'fet_weather': 'Weather Conditions',
        'fetch_weather': '🔄 Fetch Live Weather',
        'predict_btn': '🔮 Predict Best Crop',
        'results': '🌾 Recommendation Results',
        'best_crop': 'Best Crop to Plant:',
        'ai_reasoning': '🧠 AI Agronomist Reasoning',
        'view_raw': '🔍 Debug: View Raw Weather API Response',
        'simulated_warn': '⚠️ API Key activating (401). Using SIMULATED live data...',
        
        # Insurance
        'ins_title': '🛡️ PMFBY Insurance Calculator',
        'ins_sub': 'Calculate your premium for Pradhan Mantri Fasal Bima Yojana',
        'crop_type': 'Crop Type',
        'sum_insured': 'Sum Insured (₹ per Hectare)',
        'area': 'Area (in Hectares)',
        'calc_premium': '🧮 Calculate Premium',
        'farmer_share': 'Farmer Share (Premium)',
        'govt_share': 'Govt Share (Subsidy)',
        'total_premium': 'Total Premium',
        'scheme_select': 'Select Insurance Scheme',
        'pmfby': 'PMFBY (Yield Based)',
        'wbcis': 'WBCIS (Weather Based)',
        'wbcis_desc': 'Protection against adverse weather (Drought/Excess Rain).',
        'weather_risk': 'Select Risk Coverage',
        'risk_drought': 'Drought / Low Rainfall',
        'risk_excess': 'Excess Rainfall / Floor',
        'risk_unseasonal': 'Unseasonal Rain',
        
        # Market Prices
        'mandi_title': '💰 Real-Time Market Prices (Mandi)',
        'select_state': 'Select State',
        'select_district': 'Select District',
        'select_commodity': 'Select Commodity',
        'check_prices': '🔍 Check Prices',
        'price_trend': '📈 Price Trends (Last 7 Days)',
        
        # Internal Fields
        'enter_crop': 'Enter Your Target Crop',
        'crop_placeholder': 'e.g. Wheat, Sugarcane',
        'select_soil': 'Select Soil Type',
        'farm_area': 'Farm Area (Hectares)',
        'get_fert_sugg': 'Get Fertilizer Suggestions',
        'calc_water': 'Calculate Water Requirement',
        'sugg_fert': 'Suggested Fertilizers',
        'req_water': 'Required Water',
        'input_method': 'Input Method',
        'manual': 'Enter Values (Manual)',
        'upload': 'Upload Photo/Soil Card',
        'drop_image': 'Upload Soil Image',
        'no_card': "I don't have soil details",
        'save_profile': 'Save Soil Profile',
        'profile_saved': 'Soil Profile Saved!',
        'using_avg': 'Using average values (50-50-50).',
        'find_lab': 'Find Soil Lab',
        'pest_obs': 'Any Pest/Disease observed? (Optional)',
        'pest_obs_ph': 'e.g. Yellowing leaves, spots, bugs',
        'rec_pest': 'Pest Control',
        'crop_stage_label': 'Crop Growth Stage',
        'rec_schedule': 'Fertilizer Schedule (Frequency)',
        'stage_options': ['Pre-Sowing / Basal', 'Vegetative / Growth', 'Flowering / Fruiting', 'Post-Harvest'],

        # Yield Prediction
        'yield_title': '📊 Smart Yield Predictor',
        'yield_desc': 'Estimate your crop production using AI-powered analysis.',
        'select_param': 'Select Parameters',
        'select_season': 'Select Season',
        'enter_crop': 'Enter Crop Name',
        'crop_ph': 'e.g. Wheat, Cotton',
        'cult_area': 'Cultivation Area (Acres)',
        'real_time_cond': '🌍 Real-Time Conditions',
        'curr_soil': 'Current Soil Status',
        'weather_outlook': 'Seasonal Weather Outlook',
        'predict_yield': 'Predict Yield 🚜',
        'analyzing_yield': 'Analyzing Location + Image + Data...',
        'asking_ai': 'Asking AI for prediction...',
        'est_prod': 'Estimated Production',
        'est_yield': 'Estimated Avg Yield',
        'ai_insight': '🤖 AI Insight',
        'ai_note': '⚠️ Note: This is an AI estimate based on general data.',
        'district_city': 'District/City',
        'village': 'Village',
        'upload_crop': '📸 Upload Crop/Field Photo (Optional)',
        'image_loaded': '✅ Image Loaded',
        'viz_analysis': 'Visual Analysis',
        
        # Scientific Calculator
        'scientific_calc': '🔬 Scientific Yield Calculator',
        'adv_inputs': 'Advanced Agronomy Inputs',
        'sowing_date': 'Sowing Date',
        'seed_variety': 'Seed Variety',
        'seed_ph': 'e.g. HD-2967, Pusa Basmati',
        'irrigation': 'Irrigation Method',
        'fertilizer': 'Fertilizer Applied',
        'fert_ph': 'e.g. DAP 50kg, Urea',
        'irri_flood': 'Flood Irrigation',
        'irri_drip': 'Drip Irrigation',
        'irri_sprinkler': 'Sprinkler',
        'irri_rainfed': 'Rainfed',
        'pest_ctrl': 'Pest Control Frequency',
        'pest_c_name': 'Pest Control Name',
        'pest_name_ph': 'e.g. Monocrotophos, Neem Oil',
        'pest_ph': 'e.g. 2 times, None',
        
        'tonnes': 'Tonnes',
        'tonnes_acre': 'Tonnes/Acre',
        'commercial': 'Commercial/Horticultural',
        'hi': 'Hi',
        'nagpur': 'Nagpur',
        'wheat': 'Wheat',
        'rice': 'Rice',
        'india': 'India',
        'ph_name': 'e.g. Ramesh Kumar',
        'ph_mobile': '10-digit number',
        'ph_city': 'Your City',
        'ph_pin': 'Minimum 4 digits',
        'ph_login_phone': 'Registered Number',
        'live_ogd': '✅ Live Data from OGD Platform India',
        'fetching_mandi': 'Fetching Live Mandi Rates...',
        'farmer_fb': 'Farmer',
        'lang_label': '🌐 Language',
        'fert_subtitle': 'Smart nutrient analysis for maximum yield',
        'upload_soil': '📸 Upload Soil Card / Image',
        'caption_uploaded': 'Uploaded Image',
        'crop_details': '🌾 Crop Details',
        'ai_analyzing': '🤖 AI Agronomist is analyzing your soil & crop needs...',
        'bg_err': 'BACKGROUND IMAGE NOT FOUND AT',
        'bg_load_err': 'Error loading background',
        'kharif_opt': 'Kharif',
        'rabi_opt': 'Rabi',
        'high_risk': '(High Risk)',
        'no_mandi_data': '❌ No data available.',
        'err_weather_fetch': '❌ Could not fetch weather for',
        'simulated_data_warn': '⚠️ Using Simulated Data (API Key invalid)',
        'simulated_text': '(Simulated)',
        'partly_cloudy': 'Partly Cloudy',
        'kb_subtitle': 'Your comprehensive guide to smart and sustainable farming',
        'login_first': 'Please login from the Home page first.',
        'go_home': 'Go to Home',
        'user_profile': 'User Profile',
        'logged_in_as': 'Logged in as',
        'fetching_weather': 'Fetching Weather...',
        'delhi': 'Delhi',
        'ai_err_general': 'AI Explanation unavailable. Check internet connection.',
        'ai_err_api': 'API Key not configured.',
        'ai_err_api_401': 'API Key error (401). Using SIMULATED live data for',
        'ai_analysis_complete': 'AI analysis complete.',
        'ai_analysis_failed': 'AI Analysis Failed',
        'ai_chat_trouble': 'I am having trouble connecting to the satellite. Please try again.',
        'modal': 'Modal Price (₹/Qt)',
        'min': 'Min Price (₹/Qt)',
        'max': 'Max Price (₹/Qt)',
        'price_analysis': 'Price Analysis',
        'knowledge': 'Knowledge Base',
        'yield_pred': 'Yield Prediction',
        'fert_advisor': 'Fertilizer Advisor',
        'st_mh': 'Maharashtra',
        'st_pb': 'Punjab',
        'st_up': 'Uttar Pradesh',
        'st_gj': 'Gujarat',
        'st_hr': 'Haryana',
        'st_mp': 'Madhya Pradesh',
        'st_ka': 'Karnataka',
        'st_wb': 'West Bengal',
        'st_br': 'Bihar',
        'st_rj': 'Rajasthan',
        'st_ap': 'Andhra Pradesh',
        'st_tg': 'Telangana',
        'st_tn': 'Tamil Nadu',
        'st_od': 'Odisha',
        'st_ot': 'Other',
        'season_kharif': 'Kharif',
        'season_rabi': 'Rabi',
        'season_zaid': 'Zaid',
        'season_year': 'Full Year',
        'weather_normal': 'Normal Rainfall',
        'weather_drought': 'Drought / Low Rainfall',
        'weather_heavy_rain': 'Heavy / Excess Rain',
        'weather_heatwave': 'Heatwave / High Temp',
        'soil_loamy': 'Loamy (Fertile)',
        'soil_sandy': 'Sandy (Well Drained)',
        'soil_clayey': 'Clayey (Water Retaining)',
        'soil_saline': 'Saline / Alkaline',
        'india': 'India',
        'rice': 'Rice',
        'wheat': 'Wheat',
        'nagpur': 'Nagpur',
        'delhi': 'Delhi',
        'pune': 'Pune',
        'haveli': 'Haveli',
        'ph_city_ex': 'e.g. Pune',
        'ph_village_ex': 'e.g. Haveli',
        
        # Knowledge Base
        'kb_title': '📖 Farming Knowledge Base',
        'tab_seasons': 'Seasonal Calendar',
        'tab_pests': 'Pest Control',
        'tab_schemes': 'Govt Schemes',
        'tab_labs': 'Soil Labs',
        'tab_health': 'Soil Health',
        'sub_seasons': 'Agriculture Seasons in India',
        'sub_pests': 'Common Pests & Cures',
        'sub_schemes': 'Key Government Schemes',
        'sub_labs': 'Soil Testing Centers',
        'sub_health': 'Expert Soil Health Tips',
        'kb_crops': 'Crops',
        'kb_care': 'Care Tips',
        'kb_symptoms': 'Symptoms',
        'kb_treatment': 'Treatment',
        'kb_benefit': 'Benefit',
        'kb_eligibility': 'Eligibility',
        'kb_address': 'Address',
        'kb_contact': 'Contact',
    },
    'Hindi': {
        # App.py
        'app_name': 'किसान सुपर ऐप',
        'tagline': 'आपका स्मार्ट खेती साथी',
        'register': '🚀 पंजीकरण (नया उपयोगकर्ता)',
        'login': '🔑 लॉग इन (मौजूदा उपयोगकर्ता)',
        'reg_sub': 'आज ही हमारे साथ अपनी यात्रा शुरू करें',
        'login_sub': 'वापसी पर स्वागत है, किसान भाई',
        'welcome_user': 'स्वागत है, किसान! 🚜',
        'namaste': 'नमस्ते',
        'location': '📍 स्थान',
        'weather_err': '⚠️ मौसम उपलब्ध नहीं',
        'quick_actions': '⚡ त्वरित कार्य',
        'updates': '📢 नवीनतम अपडेट',
        'crop_doc': 'फसल डॉक्टर',
        'insurance': 'बीमा कैलकुलेटर',
        'mandi': 'मंडी भाव',
        'weather_det': 'मौसम विवरण',
        'trusted_partners': 'किसानों और कृषि भागीदारों द्वारा विश्वसनीय',
        'services_tools': 'सेवाएं और उपकरण',
        'humidity': 'नमी',
        'wind': 'हवा',
        'ask_ai_title': 'AI विशेषज्ञ से पूछें 🤖',
        'ask_ai_subtitle': 'फसलों और बीमारियों पर तुरंत विशेषज्ञ सलाह लें',
        'chat_now': 'अभी चैट करें ➔',
        'search': 'खोजें',
        'search_placeholder': '🔍 फसलें, मंडी या सलाह खोजें...',
        'ai_greet': 'नमस्ते! मैं आपका AI कृषि विशेषज्ञ हूँ। मुझसे कीट नियंत्रण, फसल रोगों या उर्वरक कार्यक्रम के बारे में कुछ भी पूछें! 🚜',
        'ai_title': 'AI कृषि विशेषज्ञ',
        'ai_sub': 'आपका 24/7 स्मार्ट खेती सहायक',
        'ai_placeholder': 'मुझसे कुछ भी पूछें: कीट, फसलें, या उर्वरक...',
        'weather_forecast': 'वास्तविक समय की स्थिति और पूर्वानुमान',
        'select_loc': '📍 स्थान चुनें',
        'feels_like': 'महसूस होता है',
        'cond_details': 'स्थितियों का विवरण',
        'wind_speed': 'हवा की गति',
        'max_temp': 'अधिकतम तापमान',
        'min_temp': 'न्यूनतम तापमान',
        'smart_water': 'स्मार्ट जल प्रबंधन',
        'rec_schedule': 'अनुशंसित कार्यक्रम',
        'liters': 'लीटर',
        'standard_freq': 'मानक कार्यक्रम (प्रत्येक 10-12 दिनों में)।',
        'sandy_freq': 'रेतीली मिट्टी तेजी से सूखती है। बार-बार सिंचाई करें (प्रत्येक 5-7 दिनों में)।',
        'clayey_freq': 'मिट्टी पानी को सोख लेती है। कम बार सिंचाई करें (प्रत्येक 12-15 दिनों में)।',
        'loamy_freq': 'दोमट मिट्टी संतुलित होती है। प्रत्येक 8-10 दिनों में सिंचाई करें।',
        'ins_info_title': '📚 सरकारी योजना की जानकारी',
        'ins_info_content': '- **PMFBY**: गैर-निवारक जोखिमों के कारण होने वाले उपज नुकसान के लिए सबसे अच्छा।\n- **WBCIS**: यदि मौसम डेटा सामान्य से विचलित होता है तो भुगतान करता है।\n- **KCC लिंक**: KCC ऋण धारकों के लिए अनिवार्य।',
        'mandi_sub': 'लाइव क्षेत्रीय बाजार दरें और रुझान',
        'price_analysis': 'वास्तविक समय मूल्य विश्लेषण और पूर्वानुमान',
        'hist_trend': 'ऐतिहासिक रुझान',
        'market_rates': 'बाजार दरें (आज)',
        'ai_forecast': 'AI पूर्वानुमान (3-दिन)',
        'chart_title': 'लाइव मार्केट विश्लेषण और भविष्यवाणी',
        'date': 'तारीख',
        'price_qt': 'कीमत (₹/क्विंटल)',
        'col_market': 'बाजार',
        'col_min': 'न्यूनतम मूल्य (₹/क्विंटल)',
        'col_max': 'अधिकतम मूल्य (₹/क्विंटल)',
        'soil_loamy': 'सामान्य/दोमट (Normal/Loamy)',
        'soil_sandy': 'रेतीली (कम जल धारण क्षमता) - Sandy',
        'soil_clayey': 'मिट्टी वाली (जलजमाव का जोखिम) - Clayey',
        'soil_saline': 'खारी/अपघटित (Saline/Degraded)',
        'weather_normal': 'सामान्य वर्षा',
        'weather_drought': 'सूखा/कम वर्षा',
        'weather_heavy_rain': 'भारी वर्षा/बाढ़',
        'weather_heatwave': 'लू (Heatwave)',
        'soil_sandy_simple': 'रेतीली (Sandy)',
        'soil_clayey_simple': 'मिट्टी वाली (Clayey)',
        'soil_loamy_simple': 'दोमट (Loamy)',
        'season_kharif': 'खरीफ (Kharif)',
        'season_rabi': 'रबी (Rabi)',
        'season_zaid': 'जायद (Zaid)',
        'season_year': 'पूरे वर्ष',
        'st_mh': 'महाराष्ट्र',
        'st_pb': 'पंजाब',
        'st_up': 'उत्तर प्रदेश',
        'st_gj': 'गुजरात',
        'st_hr': 'हरियाणा',
        'st_mp': 'मध्य प्रदेश',
        'st_ka': 'कर्नाटक',
        'st_wb': 'पश्चिम बंगाल',
        'st_br': 'बिहार',
        'st_rj': 'राजस्थान',
        'st_ap': 'आंध्र प्रदेश',
        'st_tg': 'तेलंगाना',
        'st_tn': 'तमिलनाडु',
        'st_od': 'ओडिशा',
        'st_ot': 'अन्य',
        'col_modal': 'औसत मूल्य (₹/क्विंटल)',
        'col_kg': 'कीमत (₹/किलो)',
        'col_date': 'तारीख',
        'ask_ai': 'AI विशेषज्ञ से पूछें',
        'knowledge': 'ज्ञान केंद्र',
        'fert_advisor': 'उर्वरक सलाहकार',
        'irrigation': 'सिंचाई केंद्र',
        'yield_pred': 'उपज भविष्यवाणी',
        'logout': '⬅️ बाहर जाएं',
        'full_name': 'पूरा नाम',
        'mobile': 'मोबाइल नंबर',
        'city': 'शहर',
        'create_acc': 'खाता बनाएं',
        'back': '⬅️ पीछे',
        'login_btn': 'लॉग इन करें',
        'enter_mobile': 'पंजीकृत मोबाइल नंबर दर्ज करें',
        'setup': '⚙️ पहली बार सेटअप',
        'success_create': 'खाता बनाया गया! आइए आपके अनुभव को निजीकृत करें।',
        'confirm_city': 'अपने शहर की पुष्टि करें',
        'select_crop': 'मुख्य फसल चुनें',
        'save': 'सहेजें और जारी रखें',
        'user_not_found': 'उपयोगकर्ता नहीं मिला। कृपया पंजीकरण करें।',
        'already_reg': 'फोन नंबर पहले से पंजीकृत है। कृपया लॉग इन करें।',
        'fill_all': 'कृपया सभी विवरण भरें।',
        'land_size': 'भूमि का आकार (एकड़)',
        'password': 'पासवर्ड (PIN) बनाएं',
        'confirm_password': 'पासवर्ड की पुष्टि करें',
        'enter_password': 'पासवर्ड दर्ज करें',
        'wrong_password': '❌ गलत पासवर्ड!',
        'pass_mismatch': '❌ पासवर्ड मेल नहीं खाते!',
        'pass_too_short': '❌ पासवर्ड कम से कम 4 अंकों का होना चाहिए!',
        'total_premium': 'कुल प्रीमियम',
        'updated': 'सफलतापूर्वक अपडेट किया गया!',
        'auth_success': '✅ प्रमाणीकरण सफल!',
        'nav_home': 'होम',
        'nav_crops': 'फसलें',
        'nav_weather': 'मौसम',
        'nav_chat': 'विशेषज्ञ',
        'nav_about': 'ज्ञान',
        'prof_my_info': '📋 मेरी जानकारी',
        'prof_features': '🌟 सुविधाएं',
        'prof_select_crop': 'फसल चुनें',
        'prof_change_lang': 'भाषा बदलें',
        'prof_location': 'स्थान',
        'prof_full_profile': 'पूरी प्रोफाइल',
        'prof_sign_out': 'लॉग आउट',
        'prof_crop_care': 'फसल देखभाल',
        'prof_protection': 'सुरक्षा',
        'prof_fertilizer': 'उर्वरक',
        'prof_back_home': 'होम पर वापस',
        'logic_title': '💡 तर्क',
        'highly_suitable': 'अत्यधिक उपयुक्त',
        'stage_pre_sowing': 'बुवाई से पहले / बेसल',
        'stage_veg': 'शाकाहारी / विकास',
        'stage_flowering': 'फूल / फल आना',
        'stage_post_harvest': 'कटाई के बाद',
        'nav_home': 'होम',
        'nav_crops': 'फसलें',
        'nav_weather': 'मौसम',
        'nav_chat': 'विशेषज्ञ',
        
        # Crop Recommendation
        'crop_title': '🌱 स्मार्ट फसल सलाह',
        'soil_health': 'मृदा स्वास्थ्य कार्ड डेटा',
        'nitrogen': 'नाइट्रोजन (N)',
        'phosphorus': 'फॉस्फोरस (P)',
        'potassium': 'पोटेशियम (K)',
        'ph_level': 'मिट्टी का pH स्तर',
        'fet_weather': 'मौसम की स्थिति',
        'fetch_weather': '🔄 लाइव मौसम प्राप्त करें',
        'predict_btn': '🔮 सर्वश्रेष्ठ फसल का अनुमान लगाएं',
        'results': '🌾 परिणाम',
        'best_crop': 'लगाने के लिए सर्वोत्तम फसल:',
        'ai_reasoning': '🧠 AI कृषि विशेषज्ञ का तर्क',
        'view_raw': '🔍 डिबग: कच्चा मौसम डेटा देखें',
        'simulated_warn': '⚠️ API Key सक्रिय हो रही है। नकली डेटा का उपयोग किया जा रहा है...',

        # Insurance
        'ins_title': '🛡️ PMFBY बीमा कैलकुलेटर',
        'ins_sub': 'प्रधान मंत्री फसल बीमा योजना के लिए अपने प्रीमियम की गणना करें',
        'crop_type': 'फसल का प्रकार',
        'sum_insured': 'बीमा राशि (₹ प्रति हेक्टेयर)',
        'area': 'क्षेत्रफळ (हेक्टेयर में)',
        'calc_premium': '🧮 प्रीमियम की गणना करें',
        'farmer_share': 'किसान का हिस्सा (प्रीमियम)',
        'govt_share': 'सरकार का हिस्सा (सब्सिडी)',
        'total_premium': 'कुल प्रीमियम',
        'updated': 'सफलतापूर्वक अपडेट किया गया!',
        'scheme_select': 'बीमा योजना चुनें',
        'pmfby': 'PMFBY (उपज आधारित)',
        'wbcis': 'WBCIS (मौसम आधारित)',
        'wbcis_desc': 'प्रतिकूल मौसम (सूखा/बाढ़) के लिए सुरक्षा। उच्च प्रीमियम, तेज दावा।',
        'weather_risk': 'जोखिम कवरेज',
        'risk_drought': 'सूखा / कम वर्षा',
        'risk_excess': 'अधिक वर्षा',
        'risk_unseasonal': 'बेमौसम बारिश',
        
        # Market Prices
        'mandi_title': '💰 रीयल-टाइम मंडी भाव',
        'select_state': 'राज्य चुनें',
        'select_district': 'जिला चुनें',
        'select_commodity': 'फसल चुनें',
        'check_prices': '🔍 भाव देखें',
        'price_trend': '📈 मूल्य रुझान (पिछले 7 दिन)',
        
        # Internal Fields
        'enter_crop': 'फसल का नाम डालें',
        'crop_placeholder': 'उदा. गेहूं, गन्ना',
        'select_soil': 'मिट्टी का प्रकार चुनें',
        'farm_area': 'खेत का क्षेत्रफल (हेक्टेयर)',
        'get_fert_sugg': 'उर्वरक सुझाव प्राप्त करें',
        'calc_water': 'जल आवश्यकता की गणना करें',
        'sugg_fert': 'सुझाए गए उर्वरक',
        'req_water': 'आवश्यक पानी',
        'input_method': 'इनपुट विधि',
        'manual': 'मान (मैनुअल) दर्ज करें',
        'upload': 'फोटो/मृदा कार्ड अपलोड करें',
        'drop_image': 'मिट्टी की छवि अपलोड करें',
        'no_card': "मेरे पास मिट्टी का विवरण नहीं है",
        'save_profile': 'मृदा प्रोफाइल सहेजें',
        'profile_saved': 'मृदा प्रोफाइल सहेजा गया!',
        'using_avg': 'औसत मानों (50-50-50) का उपयोग करना।',
        'find_lab': 'मृदा प्रयोगशाला खोजें',
        'pest_obs': 'कोई कीट/रोग देखा गया? (वैकल्पिक)',
        'pest_obs_ph': 'उदा. पीली पत्तियां, धब्बे, कीड़े',
        'rec_pest': 'कीट नियंत्रण',
        'crop_stage_label': 'फसल विकास चरण',
        'rec_schedule': 'उर्वरक अनुसूची (आवृत्ति)',
        'stage_options': ['बुवाई पूर्व / बेसल', 'वनस्पति / विकास', 'फूल / फल आना', 'कटाई के बाद'],

        # Yield Prediction
        'yield_title': '📊 स्मार्ट उपज अनुमानक',
        'yield_desc': 'AI-संचालित विश्लेषण का उपयोग करके अपने फसल उत्पादन का अनुमान लगाएं।',
        'select_param': 'पैरामीटर चुनें',
        'select_season': 'सीजन चुनें',
        'enter_crop': 'फसल का नाम डालें',
        'crop_ph': 'उदा. गेहूं, कपास',
        'cult_area': 'खेती का क्षेत्रफल (एकड़)',
        'real_time_cond': '🌍 वास्तविक समय की स्थिति',
        'curr_soil': 'वर्तमान मिट्टी की स्थिति',
        'weather_outlook': 'मौसमी मौसम का दृष्टिकोण',
        'predict_yield': 'उपज का अनुमान लगाएं 🚜',
        'analyzing_yield': 'स्थान + छवि + डेटा का विश्लेषण किया जा रहा है...',
        'asking_ai': 'AI से भविष्यवाणी मांग रहा है...',
        'est_prod': 'अनुमानित उत्पादन',
        'est_yield': 'अनुमानित औसत उपज',
        'ai_insight': '🤖 AI अंतर्दृष्टि',
        'ai_note': '⚠️ नोट: यह सामान्य डेटा पर आधारित एक AI अनुमान है।',
        'district_city': 'जिला/शहर',
        'village': 'गाँव',
        'upload_crop': '📸 फसल/खेत का फोटो अपलोड करें (वैकल्पिक)',
        'image_loaded': '✅ छवि लोड की गई',
        'viz_analysis': 'दृश्य विश्लेषण',
        
        # Scientific Calculator
        'scientific_calc': '🔬 वैज्ञानिक उपज कैलकुलेटर',
        'adv_inputs': 'उन्नत कृषि इनपुट',
        'sowing_date': 'बुवाई की तारीख',
        'seed_variety': 'बीज की किस्म',
        'seed_ph': 'उदा. HD-2967, पूसा बासमती',
        'irrigation': 'सिंचाई विधि',
        'fertilizer': 'उर्वरक का प्रयोग',
        'fert_ph': 'उदा. DAP 50kg, यूरिया',
        'irri_flood': 'बाढ़ सिंचाई',
        'irri_drip': 'टपक सिंचाई',
        'irri_sprinkler': 'फव्वारा',
        'irri_rainfed': 'वर्षा सिंचित',
        'pest_ctrl': 'कीट नियंत्रण आवृत्ति',
        'pest_c_name': 'कीटनाशक का नाम',
        'pest_name_ph': 'उदा. मोनोक्रोटोफॉस, नीम का तेल',
        'pest_ph': 'उदा. 2 बार, कोई नहीं',
        'tonnes': 'टन (Tonnes)',
        'tonnes_acre': 'टन/एकड़ (Tonnes/Acre)',
        'commercial': 'वाणिज्यिक/बागवानी (Commercial/Horticultural)',
        'hi': 'नमस्ते',
        'nagpur': 'नागपुर (Nagpur)',
        'wheat': 'गेहूं (Wheat)',
        'rice': 'चावल (Rice)',
        'india': 'भारत (India)',
        'ph_name': 'उदा. रमेश कुमार',
        'ph_mobile': '10-अंकीय नंबर',
        'ph_city': 'आपका शहर',
        'ph_pin': 'न्यूनतम 4 अंक',
        'ph_login_phone': 'पंजीकृत नंबर',
        'live_ogd': '✅ भारत के OGD प्लेटफॉर्म से लाइव डेटा',
        'fetching_mandi': 'लाइव मंडी भाव प्राप्त कर रहा है...',
        'farmer_fb': 'किसान',
        'lang_label': '🌐 भाषा (Language)',
        'fert_subtitle': 'अधिकतम उपज के लिए स्मार्ट पोषक तत्व विश्लेषण',
        'upload_soil': '📸 सॉइल कार्ड / छवि अपलोड करें',
        'caption_uploaded': 'अपलोड की गई छवि',
        'crop_details': '🌾 फसल का विवरण',
        'ai_analyzing': '🤖 AI कृषि विशेषज्ञ आपकी मिट्टी और फसल की जरूरतों का विश्लेषण कर रहा है...',
        'bg_err': 'पृष्ठभूमि छवि यहाँ नहीं मिली:',
        'bg_load_err': 'पृष्ठभूमि लोड करने में त्रुटि',
        'kharif_opt': 'खरीफ',
        'rabi_opt': 'रबी',
        'high_risk': '(उच्च जोखिम)',
        'no_mandi_data': '❌ कोई डेटा उपलब्ध नहीं है।',
        'err_weather_fetch': '❌ मौसम की जानकारी प्राप्त नहीं हो सकी:',
        'simulated_data_warn': '⚠️ सिम्युलेटेड डेटा का उपयोग (API कुंजी अमान्य)',
        'simulated_text': '(सिम्युलेटेड)',
        'partly_cloudy': 'आंशिक रूप से बादल',
        'kb_subtitle': 'स्मार्ट और टिकाऊ खेती के लिए आपका व्यापक मार्गदर्शक',
        'login_first': 'कृपया पहले होम पेज से लॉग इन करें।',
        'go_home': 'होम पर जाएं',
        'user_profile': 'उपयोगकर्ता प्रोफ़ाइल',
        'logged_in_as': 'इस रूप में लॉग इन किया',
        'fetching_weather': 'मौसम की जानकारी प्राप्त कर रहा है...',
        'delhi': 'दिल्ली',
        'ai_err_general': 'AI विवरण उपलब्ध नहीं है। इंटरनेट कनेक्शन की जाँच करें।',
        'ai_err_api': 'API कुंजी कॉन्फ़िगर नहीं की गई है।',
        'ai_err_api_401': 'API कुंजी त्रुटि (401)। इसके लिए सिम्युलेटेड लाइव डेटा का उपयोग कर रहा हूँ:',
        'ai_analysis_complete': 'AI विश्लेषण पूरा हुआ।',
        'ai_analysis_failed': 'AI विश्लेषण विफल रहा',
        'ai_chat_trouble': 'मुझे सैटेलाइट से जुड़ने में परेशानी हो रही है। कृपया पुनः प्रयास करें।',
        'modal': 'औसत मूल्य (₹/क्विंटल)',
        'min': 'न्यूनतम मूल्य (₹/क्विंटल)',
        'max': 'अधिकतम मूल्य (₹/क्विंटल)',
        'price_analysis': 'मूल्य विश्लेषण',
        'knowledge': 'ज्ञान केंद्र',
        'yield_pred': 'उत्पन्न अंदाज',
        'fert_advisor': 'खत सल्लागार',
        'st_mh': 'महाराष्ट्र',
        'st_pb': 'पंजाब',
        'st_up': 'उत्तर प्रदेश',
        'st_gj': 'गुजरात',
        'st_hr': 'हरियाणा',
        'st_mp': 'मध्य प्रदेश',
        'st_ka': 'कर्नाटक',
        'st_wb': 'पश्चिम बंगाल',
        'st_br': 'बिहार',
        'st_rj': 'राजस्थान',
        'st_ap': 'आंध्र प्रदेश',
        'st_tg': 'तेलंगाना',
        'st_tn': 'तमिलनाडु',
        'st_od': 'ओडिशा',
        'st_ot': 'अन्य',
        'season_kharif': 'खरीफ',
        'season_rabi': 'रबी',
        'season_zaid': 'जायद',
        'season_year': 'पूरे साल',
        'weather_normal': 'सामान्य वर्षा',
        'weather_drought': 'सूखा / कम वर्षा',
        'weather_heavy_rain': 'भारी / अत्यधिक वर्षा',
        'weather_heatwave': 'लू / उच्च तापमान',
        'soil_loamy': 'दोमट (उपजाऊ)',
        'soil_sandy': 'रेतीली (निकासी वाली)',
        'soil_clayey': 'मृण्मय (जल धारण करने वाली)',
        'soil_saline': 'खारी / क्षारीय',
        'india': 'भारत',
        'rice': 'चावल',
        'wheat': 'गेहूं',
        'nagpur': 'नागपुर',
        'delhi': 'दिल्ली',
        'pune': 'पुणे',
        'haveli': 'हवेली',
        'ph_city_ex': 'उदा. पुणे',
        'ph_village_ex': 'उदा. हवेली',

        # Knowledge Base
        'kb_title': '📖 कृषि ज्ञान केंद्र',
        'tab_seasons': 'मौसमी कैलेंडर',
        'tab_pests': 'कीट नियंत्रण',
        'tab_schemes': 'सरकारी योजनाएं',
        'tab_labs': 'मृदा प्रयोगशालाएं',
        'tab_health': 'मृदा स्वास्थ्य',
        'sub_seasons': 'भारत में कृषि मौसम',
        'sub_pests': 'सामान्य कीट और उपचार',
        'sub_schemes': 'प्रमुख सरकारी योजनाएं',
        'sub_labs': 'मृदा परीक्षण केंद्र',
        'sub_health': 'विशेषज्ञ मृदा स्वास्थ सुझाव',
        'kb_crops': 'फसलें',
        'kb_care': 'देखभाल के उपाय',
        'kb_symptoms': 'लक्षण',
        'kb_treatment': 'उपचार',
        'kb_benefit': 'लाभ',
        'kb_eligibility': 'पात्रता',
        'kb_address': 'पता',
        'kb_contact': 'संपर्क',
    },
    'Marathi': {
        # App.py
        'app_name': 'शेतकरी सुपर ॲप',
        'tagline': 'तुमचा स्मार्ट शेती सोबती',
        'register': '🚀 नोंदणी (नवीन वापरकर्ता)',
        'login': '🔑 लॉग इन (विद्यमान वापरकर्ता)',
        'reg_sub': 'आजच तुमचा प्रवास आमच्यासोबत सुरू करा',
        'login_sub': 'परत स्वागत आहे, शेतकरी मित्र',
        'welcome_user': 'स्वागत आहे, शेतकरी! 🚜',
        'namaste': 'नमस्ते',
        'location': '📍 ठिकाण',
        'weather_err': '⚠️ हवामान उपलब्ध नाही',
        'quick_actions': '⚡ जलद क्रिया',
        'updates': '📢 नवीन अपडेट्स',
        'crop_doc': 'पीक डॉक्टर',
        'insurance': 'विमा कॅल्क्युलेटर',
        'mandi': 'मंडी भाव',
        'weather_det': 'हवामान तपशील',
        'trusted_partners': 'शेतकरी आणि कृषी भागीदारांचा विश्वास',
        'services_tools': 'सेवा आणि साधने',
        'humidity': 'आद्रता',
        'wind': 'वारा',
        'ask_ai_title': 'AI तज्ञाला विचारा 🤖',
        'ask_ai_subtitle': 'पिके आणि रोगांवर त्वरित तज्ञांचा सल्ला मिळवा',
        'chat_now': 'आताच चॅट करा ➔',
        'search': 'शोधा',
        'search_placeholder': '🔍 पिके, मंडी किंवा सल्ला शोधा...',
        'ai_greet': 'नमस्कार! मी तुमचा AI कृषी तज्ञ आहे. मला कीटक नियंत्रण, पिकांचे रोग किंवा खतांच्या वेळापत्रकांबद्दल काहीही विचारा! 🚜',
        'ai_title': 'AI कृषी तज्ञ',
        'ai_sub': 'तुमचा 24/7 स्मार्ट शेती सहाय्यक',
        'ai_placeholder': 'मला काहीही विचारा: कीटक, पिके किंवा खते...',
        'weather_forecast': 'वास्तविक वेळ स्थिती आणि अंदाज',
        'select_loc': '📍 ठिकाण निवडा',
        'feels_like': 'असे वाटते',
        'cond_details': 'स्थिती तपशील',
        'wind_speed': 'वाऱ्याचा वेग',
        'max_temp': 'जास्तीत जास्त तापमान',
        'min_temp': 'किमान तापमान',
        'smart_water': 'स्मार्ट पाणी व्यवस्थापन',
        'rec_schedule': 'शिफारस केलेले वेळापत्रक',
        'liters': 'लिटर',
        'standard_freq': 'मानक वेळापत्रक (दर १०-१२ दिवसांनी).',
        'sandy_freq': 'रेताड माती वेगाने निचरा करते. वारंवार पाणी द्या (दर ५-७ दिवसांनी).',
        'clayey_freq': 'काळी माती पाणी धरून ठेवते. कमी वारंवार पाणी द्या (दर १२-१५ दिवसांनी).',
        'loamy_freq': 'लोमी माती संतुलित आहे. दर ८-१० दिवसांनी पाणी द्या.',
        'ins_info_title': '📚 सरकारी योजना माहिती',
        'ins_info_content': '- **PMFBY**: प्रतिबंध न करता येणाऱ्या जोखमींमुळे होणाऱ्या उत्पादनातील नुकसानीसाठी सर्वोत्तम.\n- **WBCIS**: हवामान डेटा सामान्य पेक्षा वेगळा असल्यास पैसे देते.\n- **KCC लिंक**: KCC कर्जधारकांसाठी अनिवार्य.',
        'mandi_sub': 'थेट प्रादेशिक बाजार दर आणि कल',
        'price_analysis': 'वास्तविक वेळ भाव विश्लेषण आणि अंदाज',
        'hist_trend': 'ऐतिहासिक कल',
        'market_rates': 'बाजार भाव (आज)',
        'ai_forecast': 'AI अंदाज (३-दिवस)',
        'chart_title': 'थेट बाजार विश्लेषण आणि अंदाज',
        'date': 'तारीख',
        'price_qt': 'भाव (₹/क्विंटल)',
        'col_market': 'बाजार',
        'col_min': 'किमान भाव (₹/क्विंटल)',
        'col_max': 'कमाल भाव (₹/क्विंटल)',
        'soil_loamy': 'सामान्य/पोयटा (Normal/Loamy)',
        'soil_sandy': 'रेताड (कमी पाणी धरून ठेवणारी) - Sandy',
        'soil_clayey': 'चिकनमाती (पाणी साचण्याचा धोका) - Clayey',
        'soil_saline': 'खारवट/निकृष्ट (Saline/Degraded)',
        'weather_normal': 'सामान्य पाऊस',
        'weather_drought': 'दुष्काळ/कमी पाऊस',
        'weather_heavy_rain': 'अतिवृष्टी/पूर',
        'weather_heatwave': 'उष्णतेची लाट (Heatwave)',
        'soil_sandy_simple': 'रेताड (Sandy)',
        'soil_clayey_simple': 'चिकनमाती (Clayey)',
        'soil_loamy_simple': 'पोयटा (Loamy)',
        'season_kharif': 'खरीप (Kharif)',
        'season_rabi': 'रब्बी (Rabi)',
        'season_zaid': 'उन्हाळी (Zaid)',
        'season_year': 'वर्षभर',
        'st_mh': 'महाराष्ट्र',
        'st_pb': 'पंजाब',
        'st_up': 'उत्तर प्रदेश',
        'st_gj': 'गुजरात',
        'st_hr': 'हरियाणा',
        'st_mp': 'मध्य प्रदेश',
        'st_ka': 'कर्नाटक',
        'st_wb': 'पश्चिम बंगाल',
        'st_br': 'बिहार',
        'st_rj': 'राजस्थान',
        'st_ap': 'आंध्र प्रदेश',
        'st_tg': 'तेलंगणा',
        'st_tn': 'तामिळनाडू',
        'st_od': 'ओडिशा',
        'st_ot': 'इतर',
        'col_modal': 'सरासरी भाव (₹/क्विंटल)',
        'col_kg': 'भाव (₹/किलो)',
        'col_date': 'तारीख',
        'ask_ai': 'AI तज्ञाला विचारा',
        'knowledge': 'ज्ञान केंद्र',
        'fert_advisor': 'खत सल्लागार',
        'irrigation': 'सिंचन केंद्र',
        'yield_pred': 'उत्पन्न अंदाज',
        'logout': '⬅️ बाहेर पडा',
        'full_name': 'पूर्ण नाव',
        'mobile': 'मोबाईल नंबर',
        'city': 'शहर',
        'create_acc': 'खाते तयार करा',
        'back': '⬅️ मागे',
        'login_btn': 'लॉग इन करा',
        'enter_mobile': 'नोंदणीकृत मोबाईल नंबर टाका',
        'setup': '⚙️ प्रथम सेटअप',
        'success_create': 'खाते तयार झाले! चला तुमचा अनुभव वैयक्तिकृत करूया.',
        'confirm_city': 'तुमच्या शहराची पुष्टी करा',
        'select_crop': 'मुख्य पीक निवडा',
        'save': 'जतन करा आणि पुढे जा',
        'user_not_found': 'वापरकर्ता सापडला नाही. कृपया नोंदणी करा.',
        'already_reg': 'फोन नंबर आधीच नोंदणीकृत आहे. कृपया लॉग इन करा.',
        'fill_all': 'कृपया सर्व तपशील भरा.',
        'land_size': 'जमिनीचे क्षेत्रफळ (एकर)',
        'password': 'पासवर्ड (PIN) तयार करा',
        'confirm_password': 'पासवर्डची पुष्टी करा',
        'enter_password': 'पासवर्ड टाका',
        'wrong_password': '❌ चुकीचा पासवर्ड!',
        'pass_mismatch': '❌ पासवर्ड जुळत नाहीत!',
        'pass_too_short': '❌ पासवर्ड किमान 4 अंकी असावा!',
        'updated': 'यशस्वीरित्या अपडेट केले!',
        'auth_success': '✅ प्रमाणीकरण यशस्वी!',
        'nav_home': 'होम',
        'nav_crops': 'पिके',
        'nav_weather': 'हवामान',
        'nav_chat': 'तज्ञ',
        'nav_about': 'माहिती',
        'prof_my_info': '📋 माझी माहिती',
        'prof_features': '🌟 वैशिष्ट्ये',
        'prof_select_crop': 'पीक निवडा',
        'prof_change_lang': 'भाषा बदला',
        'prof_location': 'स्थान',
        'prof_full_profile': 'पूर्ण प्रोफाइल',
        'prof_sign_out': 'लॉग आउट',
        'prof_crop_care': 'पीक काळजी',
        'prof_protection': 'संरक्षण',
        'prof_fertilizer': 'खत',
        'prof_back_home': 'होम वर परत',
        'logic_title': '💡 तर्क',
        'highly_suitable': 'अत्यंत योग्य',
        'stage_pre_sowing': 'पेरणीपूर्व / बेसल',
        'stage_veg': 'वनस्पती / वाढ',
        'stage_flowering': 'फुलणे / फळ येणे',
        'stage_post_harvest': 'कापणीनंतर',
        'nav_home': 'होम',
        'nav_crops': 'पिके',
        'nav_weather': 'हवामान',
        'nav_chat': 'तज्ञ',
        'nav_about': 'माहिती',
        
        # Crop Recommendation
        'crop_title': '🌱 स्मार्ट पीक सल्ला',
        'soil_health': 'मृदा आरोग्य दिन डेटा',
        'nitrogen': 'नायट्रोजन (N)',
        'phosphorus': 'फॉस्फरस (P)',
        'potassium': 'पोटॅशियम (K)',
        'ph_level': 'मातीचा pH स्तर',
        'fet_weather': 'हवामान स्थिती',
        'fetch_weather': '🔄 थेट हवामान मिळवा',
        'predict_btn': '🔮 सर्वोत्तम पिकाचा अंदाज घ्या',
        'results': '🌾 निकाल',
        'best_crop': 'लागवडीसाठी सर्वोत्तम पीक:',
        'ai_reasoning': '🧠 AI कृषी तज्ञाचे स्पष्टीकरण',
        'view_raw': '🔍 डीबग: कच्चा हवामान डेटा पहा',
        'simulated_warn': '⚠️ API Key सक्रिय होत आहे. सिम्युलेटेड डेटा वापरला जात आहे...',
        
        # Insurance
        'ins_title': '🛡️ PMFBY विमा कॅल्क्युलेटर',
        'ins_sub': 'पंतप्रधान पीक विमा योजनेसाठी आपल्या हप्त्याची गणना करा',
        'crop_type': 'पिकाचा प्रकार',
        'sum_insured': 'विमा रक्कम (₹ प्रति हेक्टर)',
        'area': 'क्षेत्रफळ (हेक्टेयर में)',
        'calc_premium': '🧮 हप्ता गणना करा',
        'farmer_share': 'शेतकऱ्याचा वाटा (हप्ता)',
        'govt_share': 'सरकार का वाटा (सबसिडी)',
        'total_premium': 'एकूण हप्ता',
        'scheme_select': 'विमा योजना निवडा',
        'pmfby': 'PMFBY (उत्पन्न आधारित)',
        'wbcis': 'WBCIS (हवामान आधारित)',
        'wbcis_desc': 'प्रतिकूल हवामानासाठी संरक्षण (दुष्काळ/पूर). उच्च हप्ता, जलद दावा.',
        'weather_risk': 'जोखीम संरक्षण',
        'risk_drought': 'दुष्काळ / कमी पाऊस',
        'risk_excess': 'अतिवृष्टी / पूर',
        'risk_unseasonal': 'अवकाळी पाऊस',
        
        # Market Prices
        'mandi_title': '💰 रिअल-टाइम मंडी भाव',
        'select_state': 'राज्य निवडा',
        'select_district': 'जिल्हा निवडा',
        'select_commodity': 'पीक निवडा',
        'check_prices': '🔍 भाव तपासा',
        'price_trend': '📈 किंमत कल (गेले ७ दिवस)',
        
        # Internal Fields
        'enter_crop': 'पिकाचे नाव प्रविष्ट करा',
        'crop_placeholder': 'उदा. गहू, ऊस',
        'select_soil': 'मातीचा प्रकार निवडा',
        'farm_area': 'शेताचे क्षेत्रफळ (हेक्टेयर)',
        'get_fert_sugg': 'खत सल्ला मिळवा',
        'calc_water': 'पाण्याची आवश्यकता मोजा',
        'sugg_fert': 'सुचवलेली खते',
        'req_water': 'आवश्यक पानी',
        'input_method': 'इनपुट पद्धत',
        'manual': 'मूल्ये (मॅन्युअल) प्रविष्ट करा',
        'upload': 'फोटो/मृदा कार्ड अपलोड करा',
        'drop_image': 'मातीची प्रतिमा अपलोड करा',
        'no_card': "माझ्याकडे मातीचे विवरण नाही",
        'save_profile': 'माती प्रोफाइल सेव्ह करा',
        'profile_saved': 'माती प्रोफाइल सेव्ह झाले!',
        'using_avg': 'सरासरी मूल्ये (50-50-50) वापरत आहे.',
        'find_lab': 'माती प्रयोगशाळा शोधा',
        'pest_obs': 'कीड/रोग आढळले का? (पर्यायी)',
        'pest_obs_ph': 'उदा. पाने पिवळी पडणे, डाग, अळ्या',
        'rec_pest': 'कीटक नियंत्रण',
        'crop_stage_label': 'पीक वाढीचा टप्पा',
        'rec_schedule': 'खत वेळापत्रक (वारंवारता)',
        'stage_options': ['पेरणी पूर्व / बेसल', 'शाकीय वाढ / वाढ', 'फुलोरा / फळधारणा', 'कापणी पश्चात'],

        # Yield Prediction
        'yield_title': '📊 स्मार्ट उत्पन्न अंदाज',
        'yield_desc': 'AI-शक्तीवर आधारित विश्लेषण वापरून तुमच्या पीक उत्पादनाचा अंदाज घ्या.',
        'select_param': 'पॅरामीटर्स निवडा',
        'select_season': 'हंगाम निवडा',
        'enter_crop': 'पिकाचे नाव प्रविष्ट करा',
        'crop_ph': 'उदा. गहू, कापूस',
        'cult_area': 'लागवड क्षेत्र (एकर)',
        'real_time_cond': '🌍 वास्तविक वेळेची स्थिती',
        'curr_soil': 'सध्याची मातीची स्थिती',
        'weather_outlook': 'हंगामी हवामान अंदाज',
        'predict_yield': 'उत्पन्न अंदाज घ्या 🚜',
        'analyzing_yield': 'स्थान + प्रतिमा + डेटा विश्लेषण करत आहे...',
        'asking_ai': 'AI कडे अंदाज मागत आहे...',
        'est_prod': 'अंदाजित उत्पादन',
        'est_yield': 'अंदाजित सरासरी उत्पन्न',
        'ai_insight': '🤖 AI अंतर्दृष्टी',
        'ai_note': '⚠️ टीप: हा सामान्य डेटावर आधारित AI अंदाज आहे.',
        'district_city': 'जिल्हा/शहर',
        'village': 'गाव',
        'upload_crop': '📸 पीक/शेताचा फोटो अपलोड करा (पर्यायी)',
        'image_loaded': '✅ प्रतिमा लोड केली',
        'viz_analysis': 'दृश्य विश्लेषण',
        
        # Scientific Calculator
        'scientific_calc': '🔬 वैज्ञानिक उत्पन्न कॅल्क्युलेटर',
        'adv_inputs': 'प्रगत कृषी इनपुट',
        'sowing_date': 'पेरणीची तारीख',
        'seed_variety': 'बियाणे विविधता',
        'seed_ph': 'उदा. HD-2967, पुसा बासमती',
        'irrigation': 'सिंचन पद्धत',
        'fertilizer': 'खत वापर',
        'fert_ph': 'उदा. DAP 50kg, युरिया',
        'irri_flood': 'पूर सिंचन',
        'irri_drip': 'ठिबक सिंचन',
        'irri_sprinkler': 'तुषार',
        'irri_rainfed': 'कोरडवाहू (पावसावर)',
        'pest_ctrl': 'कीटक नियंत्रण वारंवारता',
        'pest_c_name': 'कीटकनाशकाचे नाव',
        'pest_name_ph': 'उदा. मोनोक्रोटोफॉस, नीम तेल',
        'pest_ph': 'उदा. २ वेळा, नाही',
        'tonnes': 'टन (Tonnes)',
        'tonnes_acre': 'टन/एकर (Tonnes/Acre)',
        'commercial': 'व्यावसायिक/बागायती (Commercial/Horticultural)',
        'hi': 'नमस्ते',
        'nagpur': 'नागपूर (Nagpur)',
        'wheat': 'गहू (Wheat)',
        'rice': 'तांदूळ (Rice)',
        'india': 'भारत (India)',
        'ph_name': 'उदा. रमेश कुमार',
        'ph_mobile': '१०-अंकी नंबर',
        'ph_city': 'तुमचे शहर',
        'ph_pin': 'किमान ४ अंक',
        'ph_login_phone': 'नोंदणीकृत नंबर',
        'live_ogd': '✅ OGD प्लॅटफॉर्म इंडिया कडून थेट डेटा',
        'fetching_mandi': 'थेट मंडी भाव मिळवत आहे...',
        'farmer_fb': 'शेतकरी',
        'lang_label': '🌐 भाषा (Language)',
        'fert_subtitle': 'जास्तीत जास्त उत्पादनासाठी स्मार्ट पोषक तत्व विश्लेषण',
        'upload_soil': '📸 सॉइल कार्ड / प्रतिमा अपलोड करा',
        'caption_uploaded': 'अपलोड केलेली प्रतिमा',
        'crop_details': '🌾 पिकाचा तपशील',
        'ai_analyzing': '🤖 AI कृषी तज्ञ तुमच्या माती आणि पिकाच्या गरजांचे विश्लेषण करत आहे...',
        'bg_err': 'पार्श्वभूमी प्रतिमा येथे आढळली नाही:',
        'bg_load_err': 'पार्श्वभूमी लोड करताना त्रुटी',
        'kharif_opt': 'खरीप',
        'rabi_opt': 'रब्बी',
        'high_risk': '(उच्च जोखीम)',
        'no_mandi_data': '❌ कोणताही डेटा उपलब्ध नाही.',
        'err_weather_fetch': '❌ साठी हवामान मिळवता आले नाही:',
        'simulated_data_warn': '⚠️ सिम्युलेटेड डेटा वापरत आहे (API की अवैध)',
        'simulated_text': '(सिम्युलेटेड)',
        'partly_cloudy': 'अंशतः ढगाळ',
        'kb_subtitle': 'स्मार्ट आणि शाश्वत शेतीसाठी तुमचे सर्वसमावेशक मार्गदर्शक',
        'login_first': 'कृपया प्रथम होम पेजवरून लॉग इन करा.',
        'go_home': 'होमवर जा',
        'user_profile': 'वापरकर्ता प्रोफाइल',
        'logged_in_as': 'म्हणून लॉग इन केले',
        'fetching_weather': 'हवामान मिळवत आहे...',
        'delhi': 'दिल्ली',
        'ai_err_general': 'AI स्पष्टीकरण उपलब्ध नाही. इंटरनेट कनेक्शन तपासा.',
        'ai_err_api': 'API की कॉन्फिगर केलेली नाही.',
        'ai_err_api_401': 'API की त्रुटी (401). यासाठी सिमुलेटेड थेट डेटा वापरत आहे:',
        'ai_analysis_complete': 'AI विश्लेषण पूर्ण झाले.',
        'ai_analysis_failed': 'AI विश्लेषण अयशस्वी झाले',
        'ai_chat_trouble': 'मला उपग्रहाशी जोडण्यात त्रास होत आहे. कृपया पुन्हा प्रयत्न करा.',
        'modal': 'सरासरी भाव (₹/क्विंटल)',
        'min': 'किमान भाव (₹/क्विंटल)',
        'max': 'कमाल भाव (₹/क्विंटल)',
        'price_analysis': 'किंमत विश्लेषण',
        'knowledge': 'ज्ञान केंद्र',
        'yield_pred': 'उत्पन्न अंदाज',
        'fert_advisor': 'खत सल्लागार',
        'st_mh': 'महाराष्ट्र',
        'st_pb': 'पंजाब',
        'st_up': 'उत्तर प्रदेश',
        'st_gj': 'गुजरात',
        'st_hr': 'हरियाणा',
        'st_mp': 'मध्य प्रदेश',
        'st_ka': 'कर्नाटक',
        'st_wb': 'पश्चिम बंगाल',
        'st_br': 'बिहार',
        'st_rj': 'राजस्थान',
        'st_ap': 'आंध्र प्रदेश',
        'st_tg': 'तेलंगणा',
        'st_tn': 'तमिळनाडू',
        'st_od': 'ओडिशा',
        'st_ot': 'इतर',
        'season_kharif': 'खरीप',
        'season_rabi': 'रब्बी',
        'season_zaid': 'उन्हाळी',
        'season_year': 'पूर्ण वर्ष',
        'weather_normal': 'सामान्य पाऊस',
        'weather_drought': 'दुष्काळ / कमी पाऊस',
        'weather_heavy_rain': 'अतिवृष्टी / जास्त पाऊस',
        'weather_heatwave': 'उष्णतेची लाट / उच्च तापमान',
        'soil_loamy': 'लोमी (सुपीक)',
        'soil_sandy': 'रेताड (पाण्याचा निचरा होणारी)',
        'soil_clayey': 'काळी / चिकनमाती',
        'soil_saline': 'खारवट / विम्लधर्मी',
        'india': 'भारत',
        'rice': 'तांदूळ',
        'wheat': 'गहू',
        'nagpur': 'नागपूर',
        'delhi': 'दिल्ली',
        'pune': 'पुणे',
        'haveli': 'हवेली',
        'ph_city_ex': 'उदा. पुणे',
        'ph_village_ex': 'उदा. हवेली',

        # Knowledge Base
        'kb_title': '📖 कृषी ज्ञान केंद्र',
        'tab_seasons': 'हंगामी दिनदर्शिका',
        'tab_pests': 'कीटक नियंत्रण',
        'tab_schemes': 'सरकारी योजना',
        'tab_labs': 'मृदा प्रयोगशाळा',
        'tab_health': 'मृदा आरोग्य',
        'sub_seasons': 'भारतातील कृषी हंगाम',
        'sub_pests': 'कीटक आणि उपाय',
        'sub_schemes': 'महत्त्वाच्या सरकारी योजना',
        'sub_labs': 'मृदा चाचणी केंद्र',
        'sub_health': 'माती आरोग्यासाठी तज्ज्ञांच्या टिप्स',
        'kb_crops': 'पिके',
        'kb_care': 'काळजी घेण्याच्या टिप्स',
        'kb_symptoms': 'लक्षणे',
        'kb_treatment': 'उपाय',
        'kb_benefit': 'फायदा',
        'kb_eligibility': 'पात्रता',
        'kb_address': 'पत्ता',
        'kb_contact': 'संपर्क',
    }
}

def t(key):
    # Safe import inside function to avoid circular issues if st is missing (unlikely)
    import streamlit as st
    lang = st.session_state.get('language', 'English')
    return TRANSLATIONS.get(lang, {}).get(key, key)

# --- PERSISTENCE HELPERS ---
DB_FILE = "user_db.json"

def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_db(data):
    try:
        with open(DB_FILE, "w") as f:
            json.dump(data, f)
    except Exception as e:
        print(f"Error saving DB: {e}")

# --- BOTTOM NAVIGATION ---
def render_bottom_nav(active_tab='Home'):
    st.markdown(f"""
    <style>
    .bottom-nav {{
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: white;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
        display: flex;
        justify-content: space-around;
        align-items: center;
        padding: 8px 0;
        z-index: 99999;
        border-top: 1px solid #e0e0e0;
    }}
    .nav-link {{
        text-align: center;
        color: #5D6D7E; /* Default icon/text color */
        text-decoration: none;
        font-size: 0.75rem;
        flex: 1;
        transition: color 0.3s, background-color 0.3s;
        padding: 5px 0;
        border-radius: 8px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }}
    .nav-link:hover {{
        color: #1B5E20; /* Dark green on hover */
        background-color: rgba(27, 94, 32, 0.1); /* Light green background on hover */
    }}
    .nav-link.active {{
        color: #1B5E20; /* Dark green for active tab */
        font-weight: bold;
    }}
    .nav-icon {{
        width: 24px; /* Adjust icon size */
        height: 24px;
        display: block;
        margin-bottom: 2px;
    }}
    .nav-label {{
        display: block;
        font-weight: 500;
    }}
    /* Hide Streamlit footer to avoid overlap */
    footer {{visibility: hidden !important;}}
    </style>

    <div class="bottom-nav">
        <a href="/" target="_self" class="nav-link {'active' if active_tab == 'Home' else ''}">
            <img src="https://img.icons8.com/ios-filled/50/{'1B5E20' if active_tab == 'Home' else '5D6D7E'}/home.png" class="nav-icon">
            <span class="nav-label">{t('nav_home')}</span>
        </a>
        <a href="Crop_Recommendation" target="_self" class="nav-link {'active' if active_tab == 'Crops' else ''}">
            <img src="https://img.icons8.com/ios-filled/50/{'1B5E20' if active_tab == 'Crops' else '5D6D7E'}/wheat.png" class="nav-icon">
            <span class="nav-label">{t('nav_crops')}</span>
        </a>
        <a href="Weather_Info" target="_self" class="nav-link {'active' if active_tab == 'Weather' else ''}">
            <img src="https://img.icons8.com/ios-filled/50/{'1B5E20' if active_tab == 'Weather' else '5D6D7E'}/partly-cloudy-day.png" class="nav-icon">
            <span class="nav-label">{t('nav_weather')}</span>
        </a>
        <a href="AI_Agronomist" target="_self" class="nav-link {'active' if active_tab == 'Chat' else ''}">
            <img src="https://img.icons8.com/ios-filled/50/{'1B5E20' if active_tab == 'Chat' else '5D6D7E'}/chat.png" class="nav-icon">
            <span class="nav-label">{t('nav_chat')}</span>
        </a>
        <a href="Farming_Knowledge" target="_self" class="nav-link {'active' if active_tab == 'About' else ''}">
            <img src="https://img.icons8.com/ios-filled/50/{'1B5E20' if active_tab == 'About' else '5D6D7E'}/info.png" class="nav-icon">
            <span class="nav-label">{t('nav_about')}</span>
        </a>
    </div>
    """, unsafe_allow_html=True)
