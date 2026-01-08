import streamlit as st
import os
from dotenv import load_dotenv
from utils import apply_custom_style, t
from logic import get_market_trends_data, get_mandi_prices
import pandas as pd
import plotly.express as px

load_dotenv()

st.set_page_config(page_title="Market Prices", page_icon="💰", layout="wide")
apply_custom_style()

st.title(t('mandi_title'))

# Filters
col1, col2, col3 = st.columns(3)
with col1:
    state = st.selectbox(t('select_state'), ["Maharashtra", "Punjab", "Gujarat", "Madhya Pradesh", "Other"])
with col2:
    district = st.text_input(t('select_district'), value="Nagpur")
with col3:
    commodity = st.text_input(t('select_commodity'), value="Wheat")

if st.button(t('check_prices')):
    
    # Use Logic function with OGD API integration
    api_key = os.getenv("DATA_GOV_KEY")
    with st.spinner("Fetching Mandi Rates..."):
        data, is_live = get_mandi_prices(api_key, state, district, commodity)
    
    if data:
        if is_live:
            st.success(f"✅ Live Data from OGD Platform India ({district})")

            
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)
    else:
        st.error("❌ No data available.")

    
    # Trends
    st.subheader(t('price_trend'))
    trend_data = get_market_trends_data(commodity) # From logic.py
    if trend_data:
         fig = px.line(x=trend_data['dates'], y=trend_data['prices'], labels={'x': 'Date', 'y': 'Price (₹/Qt)'})
         st.plotly_chart(fig, use_container_width=True)
    else:
         st.info("No trend data available.")
