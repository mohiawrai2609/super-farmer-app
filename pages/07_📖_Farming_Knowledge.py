import streamlit as st
from logic import KNOWLEDGE_BASE
from utils import apply_custom_style, t

st.set_page_config(page_title="Farming Knowledge", page_icon="📖", layout="wide")
apply_custom_style()

# Get current language from session state
current_lang = st.session_state.get('language', 'English')
kb_data = KNOWLEDGE_BASE.get(current_lang, KNOWLEDGE_BASE['English'])

st.title(t('kb_title'))

tab1, tab2, tab3, tab4, tab5 = st.tabs([t('tab_seasons'), t('tab_pests'), t('tab_schemes'), t('tab_labs'), t('tab_health')])

with tab1:
    st.subheader(t('sub_seasons'))
    for item in kb_data.get("Seasons", []):
        with st.expander(item["Season"]):
            st.write(f"**Crops:** {item['Crops']}")
            st.write(f"**Care Tips:** {item['Care']}")
            
with tab2:
    st.subheader(t('sub_pests'))
    for item in kb_data.get("Pests", []):
        with st.expander(item["Pest"]):
            st.write(f"**Symptoms:** {item['Symptoms']}")
            st.write(f"**Treatment:** {item['Cure']}")

with tab3:
    st.subheader(t('sub_schemes'))
    for item in kb_data.get("Schemes", []):
        with st.expander(item["Name"]):
            st.write(f"**Benefit:** {item['Benefit']}")
            st.write(f"**Eligibility:** {item['Eligibility']}")

with tab4:
    st.subheader(t('sub_labs'))
    for item in kb_data.get("SoilLabs", []):
        with st.expander(item["Center"]):
            st.write(f"**Address:** {item['Address']}")
            st.write(f"**Contact:** {item['Contact']}")
            
with tab5:
    st.subheader(t('sub_health'))
    for item in kb_data.get("SoilHealth", []):
         with st.expander(item["Title"]):
             st.write(item["Tip"])
