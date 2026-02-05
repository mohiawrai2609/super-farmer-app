import streamlit as st
import os
import base64
from dotenv import load_dotenv

st.set_page_config(page_title="AI Agronomist", page_icon="🤖", layout="wide")

from logic import get_ai_response
from utils import apply_custom_style, t, render_bottom_nav

load_dotenv()

# Apply Global Style - Blurred Background as base
apply_custom_style(blur_bg=True)

# --- STATE INITIALIZATION ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# If messages exist but language changed, update the first greeting
default_greetings = [
    "Hello! I am your AI Agronomist. Ask me anything about pest control, crop diseases, or fertilizer schedules! 🚜", # English
    "नमस्ते! मैं आपका AI कृषि विशेषज्ञ हूँ। मुझसे कीट नियंत्रण, फसल रोगों या उर्वरक कार्यक्रम के बारे में कुछ भी पूछें! 🚜", # Hindi
    "नमस्कार! मी तुमचा AI कृषी तज्ञ आहे. मला कीटक नियंत्रण, पिकांचे रोग किंवा खतांच्या वेळापत्रकांबद्दल काहीही विचारा! 🚜" # Marathi
]

if not st.session_state.messages:
    st.session_state.messages.append({"role": "assistant", "content": t('ai_greet')})
elif len(st.session_state.messages) == 1 and st.session_state.messages[0]["role"] == "assistant" and st.session_state.messages[0]["content"] in default_greetings:
    st.session_state.messages[0]["content"] = t('ai_greet')


# --- CLEAN MINIMAL HEADER ---
st.markdown(f"""
<div style="padding: 20px 20px 10px 20px; text-align: center;">
    <div style="display:flex; flex-direction: column; align-items:center; gap:10px;">
        <img src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png" style="width: 60px; height: 60px; drop-shadow: 0 4px 6px rgba(0,0,0,0.3);">
        <h1 style="color: #ffffff; font-size: 28px; font-weight: 800; margin:0; font-family: 'Poppins', sans-serif; text-shadow: 0 2px 8px rgba(0,0,0,0.8);">{t('ai_title')}</h1>
    </div>
    <p style="color: #ffffff; font-size: 16px; margin-top: 5px; font-weight: 700; text-shadow: 0 2px 4px rgba(0,0,0,0.8);">
        {t('ai_sub')}
    </p>
</div>
""", unsafe_allow_html=True)

# --- LOAD BACKGROUND IMAGE ---
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

bg_img_path = os.path.join("assets", "bg_ai_robot_v2.png")
if os.path.exists(bg_img_path):
    bin_str = get_base64_of_bin_file(bg_img_path)
    bg_image_css = f"""
    [data-testid="stAppViewContainer"], .stApp {{
        background: url("data:image/png;base64,{bin_str}") no-repeat center center fixed !important;
        background-size: cover !important;
        background-attachment: fixed !important;
    }}
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0, 0, 0, 0.4); /* Elegant dark overlay */
        backdrop-filter: blur(5px) !important; 
        -webkit-backdrop-filter: blur(5px) !important;
        z-index: -1;
    }}
    """
else:
    bg_image_css = """
    [data-testid="stAppViewContainer"], .stApp {
        background: url("https://images.unsplash.com/photo-1625246333195-58f214f063ce?q=80&w=2600") no-repeat center center fixed !important;
        background-size: cover !important;
    }
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(5px) !important;
        -webkit-backdrop-filter: blur(5px) !important;
        z-index: -1;
    }
    """

# --- CSS INJECTION ---
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

/* 1. Full Page Background - CLEAR */
{bg_image_css}

/* Hide the default background canvas */
#bg-canvas {{
    display: none !important;
}}

/* 2. Hide Top Header Strip */
header[data-testid="stHeader"] {{
    display: none !important;
}}
.block-container {{
    padding-top: 1rem !important;
    padding-bottom: 8rem !important;
}}

/* 3. Chat Bubbles - Glassmorphism */
[data-testid="stChatMessage"] {{
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 10px !important;
}}

/* Assistant Bubble - Transparent Dark Glass (Vision Pro Style) */
[data-testid="stChatMessage"][data-testid="assistant"] {{
    background: rgba(0, 0, 0, 0.6) !important; 
    backdrop-filter: blur(15px) !important;
    -webkit-backdrop-filter: blur(15px) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    border-radius: 0 20px 20px 20px !important;
    margin-right: 40px !important;
    color: white !important;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37) !important;
}}

/* User Bubble - Vibrant Green */
[data-testid="stChatMessage"][data-testid="user"] {{
    background: linear-gradient(135deg, #43A047 0%, #1B5E20 100%) !important;
    border-radius: 20px 0 20px 20px !important;
    margin-left: 40px !important;
    flex-direction: row-reverse;
    color: white !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
}}

/* Text Colors - WHITE */
.stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, 
.stMarkdown h4, .stMarkdown h5, .stMarkdown h6, .stMarkdown span, 
.stMarkdown div, .stMarkdown li, .stMarkdown td, .stMarkdown th, .stMarkdown strong {{
    color: #ffffff !important;
    font-family: 'Poppins', sans-serif !important;
    text-shadow: 0 1px 2px rgba(0,0,0,0.5);
}}

[data-testid="stChatInput"] {{
    position: fixed !important;
    bottom: 80px !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    right: auto !important;
    width: 90% !important;
    max-width: 700px !important;
    background: rgba(0, 0, 0, 0.8) !important;
    backdrop-filter: blur(15px) !important;
    border-radius: 30px !important;
    border: 1px solid rgba(255,255,255,0.3) !important;
    z-index: 2000 !important;
}}

div[data-testid="stChatInput"] textarea {{
    color: #ffffff !important;
}}

[data-testid="stChatMessageAvatar"] {{
    background-color: transparent !important;
}}
</style>
""", unsafe_allow_html=True)

# --- MESSAGES ---
for message in st.session_state.messages:
    avatar = "🧑‍🌾" if message["role"] == "user" else "https://cdn-icons-png.flaticon.com/512/4712/4712109.png"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# --- INPUT ---
if prompt := st.chat_input(t('ai_placeholder')):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍🌾"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="https://cdn-icons-png.flaticon.com/512/4712/4712109.png"):
        message_placeholder = st.empty()
        full_response = ""
        current_lang = st.session_state.get('language', 'English')
        for chunk in get_ai_response(prompt, language=current_lang):
            full_response += chunk
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Render Bottom Navigation
render_bottom_nav(active_tab='Chat')
st.markdown("<br><br><br>", unsafe_allow_html=True)
