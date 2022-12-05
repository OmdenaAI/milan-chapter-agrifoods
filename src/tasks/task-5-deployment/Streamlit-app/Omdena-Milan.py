# Contents of omdena-milan.py

import streamlit as st

st.set_page_config(
    page_title="Agrifood App",
    layout='wide')
st.title("Omdena-Milan")
st.sidebar.info('Omdena-Milan Agrifood')
st.sidebar.success('https://omdena.com/local-chapters/milan-italy-chapter/')
st.title("Crop Prediction Application 🌻")
with st.expander(" ℹ️ INFORMATION", expanded=True):
     st.write("""
            Omdena-Milan Demo application for crops prediction based on climate parameters, fertilizers and area by municipality and crop type. 
            """)
st.error(" ❗ ATTENTION: This application is for Demo purposes only.")
       




