import streamlit as st
from PIL import Image
import folium
from streamlit_folium import st_folium

st.set_page_config(layout="centered")
image = Image.open('data/logo.png')
image=image.resize((100,100))
APP_SUB_TITLE = "by Omdena Milan chapter 👇 (https://omdena.com/local-chapters/milan-italy-chapter/)"
with st.sidebar:
    logo = st.image(image)
    st.caption(APP_SUB_TITLE)

import streamlit as st


st.title("AI for sustainable agriculture and foood systems:Use of Satellite Imagery")

st.markdown('''Over five weeks in October 2022, Omdena-Milan Local Chapter collaborators completed
a local chapter challenge on applying Artificial Intelligence (AI) and Satellite imagery for
sustainable agri-food systems.To this end, the Omdena-Milan Local Chapter collaborators explored
various machine learning (ML) and data science techniques and geographic information systems (GIS)
methods. The team worked on different tasks which are independent of each other to address the same 
project goal. For demonstration, the team integrated all of them into one dashboard with good usability
for non-technical decision-makers. 
''')


