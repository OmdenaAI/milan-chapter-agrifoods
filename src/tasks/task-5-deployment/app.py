import streamlit as st
import ast
from PIL import Image
import leafmap.foliumap as leafmap

st.set_page_config(layout="wide")
image = Image.open('data/logo.png')
header = st.container()

#Using "with" notation

with st.sidebar:
    logo = st.image(image)
    add_radio = st.radio(
        "Menu",
        ("Home", "EDA", "Modelling", "Demo")
    )

def get_layers(url):
    options = leafmap.get_wms_layers(url)
    return options


with header:
    st.title("AI for sustainable agriculture and foood systems:Use of Satellite Imagery!")
    st.text('''Over five weeks in October 2022, Omdena-Milan Local Chapter collaborators completed
a local chapter challenge on applying Artificial Intelligence (AI) and Satellite imagery for
sustainable agri-food systems.To this end, the Omdena-Milan Local Chapter collaborators explored
various machine learning (ML) and data science techniques and geographic information systems (GIS)
methods. The team worked on different tasks which are independent of each other to address the same 
project goal. For demonstration, the team integrated all of them into one dashboard with good usability
for non-technical decision-makers. 
''')
    #mp = st.image(it_map)

row1_col1, row1_col2 = st.columns([3, 1.3])
width = 800
height = 600
layers = None


url = "https://services.terrascope.be/wms/v2"

m = leafmap.Map(center=(42.3, 14), zoom=6)

if layers is not None:
    for layer in layers:
        m.add_wms_layer(
            url, layers=layer, name=layer, attribution=" ", transparent=True
        )

m.to_streamlit(height=height)