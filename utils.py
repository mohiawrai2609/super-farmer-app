import json
import os
import streamlit as st

# --- CUSTOM CSS ---
def apply_custom_style():
    st.markdown("""
        <style>
        /* Import Font */
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
        
        /* Global App Style */
        .stApp {
            background: linear-gradient(180deg, #F1F8E9 0%, #FFFFFF 100%);
            font-family: 'Poppins', sans-serif;
        }
        
        /* Headers */
        h1, h2, h3 {
            color: #1B5E20 !important;
            font-weight: 700 !important;
        }
        
        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #2E7D32;
            color: white;
        }
        section[data-testid="stSidebar"] * {
            color: #E8F5E9 !important;
        }
        
        /* Button Styling - Gradient & Shadow */
        .stButton>button {
            background: linear-gradient(90deg, #43A047 0%, #2E7D32 100%);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 12px 24px;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.2);
            background: linear-gradient(90deg, #66BB6A 0%, #388E3C 100%);
        }
        
        /* Input Fields (Text, Number, Date, Select) */
        .stTextInput>div>div>input, .stNumberInput>div>div>input, .stDateInput>div>div>input, .stSelectbox>div>div>div {
            border: 2px solid #C8E6C9;
            border-radius: 10px;
            background-color: white;
            color: #333;
        }
        .stTextInput>div>div>input:focus, .stNumberInput>div>div>input:focus {
            border-color: #43A047;
            box-shadow: 0 0 0 2px rgba(67, 160, 71, 0.2);
        }
        
        /* Info/Success/Warning Boxes */
        .stAlert {
            border-radius: 12px;
            border: 1px solid rgba(0,0,0,0.05);
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }
        
        /* Custom Dashboard Card Class (Usage in st.markdown) */
        .dashboard-card {
            background: white;
            border-left: 5px solid #43A047;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            margin-bottom: 20px;
            transition: transform 0.2s;
        }
        .dashboard-card:hover {
            transform: translateX(5px);
        }
        .dashboard-card h3 {
            margin-top: 0;
            color: #2E7D32 !important;
        }
        
        /* Circular Icon Styling */
        .icon-image {
            border-radius: 50%;
            background: white;
            padding: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            transition: transform 0.2s;
            margin: 0 auto;
            display: block;
            cursor: pointer;
        }
        .icon-image:hover {
            transform: scale(1.1);
        }
        
        /* Rounded Search Input */
        div[data-testid="stTextInput"] input {
            border-radius: 30px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            border: 1px solid #E0E0E0;
            padding-left: 40px !important; 
        }

        /* Profile Green Icon Box */
        .profile-icon-box {
            background-color: #2E7D32;
            border-radius: 15px;
            padding: 15px;
            text-align: center;
            color: white;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.2s;
            cursor: pointer;
            margin-bottom: 5px;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 80px;
            width: 80px;
            margin: 0 auto;
        }
        .profile-icon-box:hover {
            transform: scale(1.05);
            background-color: #1B5E20;
        }
        .profile-label {
            font-size: 0.8rem;
            text-align: center;
            color: #333;
            font-weight: 500;
            margin-top: 5px;
            line-height: 1.2;
        }
        
        .nav-label {
            text-align: center;
            font-size: 0.85rem;
            font-weight: 600;
            color: #333;
            margin-top: 5px;
            margin-bottom: 20px;
        }
        
        /* Expander Styling */
        .streamlit-expanderHeader {
            background-color: #FFFFFF;
            border-radius: 10px;
            border: 1px solid #E0E0E0;
        }
        
        /* Remove Default Footer */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
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
    },
    'Hindi': {
        # App.py
        'app_name': 'किसान सुपर ऐप',
        'tagline': 'आपका स्मार्ट खेती साथी',
        'register': '🚀 पंजीकरण (नया उपयोगकर्ता)',
        'login': '🔑 लॉग इन (मौजूदा उपयोगकर्ता)',
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
    },
    'Marathi': {
        # App.py
        'app_name': 'शेतकरी सुपर ॲप',
        'tagline': 'तुमचा स्मार्ट शेती सोबती',
        'register': '🚀 नोंदणी (नवीन वापरकर्ता)',
        'login': '🔑 लॉग इन (विद्यमान वापरकर्ता)',
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
def render_bottom_nav():
    st.markdown("""
    <style>
    .bottom-nav {
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
    }
    .nav-item {
        text-align: center;
        color: #757575 !important;
        text-decoration: none !important;
        font-size: 0.75rem;
        flex: 1;
        transition: color 0.3s;
    }
    .nav-item:hover {
        color: #2E7D32 !important;
        background-color: rgba(46, 125, 50, 0.05);
        border-radius: 8px;
    }
    .nav-icon {
        font-size: 1.4rem;
        display: block;
        margin-bottom: 2px;
    }
    .nav-text {
        display: block;
        font-weight: 500;
    }
    /* Hide Streamlit footer to avoid overlap */
    footer {visibility: hidden !important;}
    </style>

    <div class="bottom-nav">
        <a href="/" target="_self" class="nav-item">
            <span class="nav-icon">🏠</span>
            <span class="nav-text">Home</span>
        </a>
        <a href="Crop_Recommendation" target="_self" class="nav-item">
            <span class="nav-icon">🌱</span>
            <span class="nav-text">Crops</span>
        </a>
        <a href="Weather_Info" target="_self" class="nav-item">
            <span class="nav-icon">☁️</span>
            <span class="nav-text">Weather</span>
        </a>
        <a href="AI_Agronomist" target="_self" class="nav-item">
            <span class="nav-icon">🤖</span>
            <span class="nav-text">Chat</span>
        </a>
        <a href="10_👤_User_Profile" target="_self" class="nav-item">
            <span class="nav-icon">👤</span>
            <span class="nav-text">Profile</span>
        </a>
    </div>
    """, unsafe_allow_html=True)
