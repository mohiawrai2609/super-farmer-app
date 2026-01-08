import streamlit as st
from utils import apply_custom_style, t

apply_custom_style()

st.header(t('ins_title'))
st.write(t('ins_sub'))

st.markdown("---")

# Scheme Selection using Tabs
tab1, tab2 = st.tabs([t('pmfby'), t('wbcis')])

with tab1:
    st.info("### " + t('pmfby'))
    col1, col2 = st.columns([1, 1])
    
    with col1:
        crop_type = st.selectbox(t('crop_type'), ["Kharif", "Rabi", "Commercial/Horticultural"], key="pmfby_crop")
        sum_insured = st.number_input(t('sum_insured'), min_value=10000, value=50000, key="pmfby_sum")
        area = st.number_input(t('area'), min_value=0.1, value=1.0, key="pmfby_area")

        # Calculate Premium
        # Rates: Kharif=2%, Rabi=1.5%, Commercial=5%
        rate = 0.02
        if crop_type == "Rabi":
            rate = 0.015
        elif crop_type == "Commercial/Horticultural":
            rate = 0.05
        
        farmer_share = sum_insured * area * rate
        govt_share = sum_insured * area * (0.12 - rate) # Hypothetical total premium 12%
        if govt_share < 0: govt_share = 0

        if st.button(t('calc_premium'), key="btn_pmfby"):
            st.session_state['premium_pmfby'] = {
                "farmer": farmer_share,
                "govt": govt_share,
                "total": farmer_share + govt_share
            }

    with col2:
        if 'premium_pmfby' in st.session_state:
            res = st.session_state['premium_pmfby']
            st.success(f"### {t('farmer_share')}: ₹{res['farmer']:.2f}")
            st.info(f"{t('govt_share')}: ₹{res['govt']:.2f}")
            st.write(f"**{t('total_premium')}: ₹{res['total']:.2f}**")
        else:
            st.write("👈 " + t('calc_premium'))

with tab2:
    st.warning("### " + t('wbcis'))
    st.caption(t('wbcis_desc'))
    
    c1, c2 = st.columns([1, 1])
    with c1:
        risk_type = st.selectbox(t('weather_risk'), [t('risk_drought'), t('risk_excess'), t('risk_unseasonal')])
        w_sum_insured = st.number_input(t('sum_insured'), min_value=15000, value=60000, key="wbcis_sum")
        w_area = st.number_input(t('area'), min_value=0.1, value=1.0, key="wbcis_area")
        
        # WBCIS Rates are significantly higher (approx 8-10%)
        w_rate = 0.08
        if risk_type == t('risk_unseasonal'):
            w_rate = 0.10
        elif risk_type == t('risk_excess'):
            w_rate = 0.09
            
        w_farmer_share = w_sum_insured * w_area * w_rate
        w_govt_share = w_sum_insured * w_area * 0.05 # Fixed subsidy
        
        if st.button(t('calc_premium'), key="btn_wbcis"):
            st.session_state['premium_wbcis'] = {
                "farmer": w_farmer_share,
                "govt": w_govt_share,
                "total": w_farmer_share + w_govt_share
            }
            
    with c2:
         if 'premium_wbcis' in st.session_state:
            res = st.session_state['premium_wbcis']
            st.error(f"### {t('farmer_share')}: ₹{res['farmer']:.2f}")
            st.info(f"{t('govt_share')}: ₹{res['govt']:.2f}")
            st.write(f"**{t('total_premium')}: ₹{res['total']:.2f}**")
         else:
            st.write("👈 " + t('calc_premium'))

# Schemes Info Section
st.markdown("---")
with st.expander("📚 Govt Scheme Information / सरकारी योजना माहिती"):
    st.markdown("""
    - **PMFBY**: Best for yield loss due to non-preventable risks (Drought, Pest, Disease).
    - **WBCIS**: Pays if weather data (rain/temp) deviates from normal. No field visit needed.
    - **KCC Linkage**: If you have a KCC Loan, insurance is often mandatory/auto-deducted.
    """)
