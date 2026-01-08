import streamlit as st
import os
from logic import get_ai_response
from utils import apply_custom_style
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI Agronomist", page_icon="🤖", layout="wide")
apply_custom_style()

api_key = os.getenv("GOOGLE_API_KEY")

st.title("🤖 AI Agronomist Chat")
st.markdown("Ask our AI any question about your farm, pests, or crops.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ex: How to handle leaf blight in rice?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    with st.chat_message("assistant"):
        response = get_ai_response(prompt, api_key)
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
