import streamlit as st
import leafmap.foliumap as leafmap

def app():

    st.title("AI for sustainable agriculture and food systems:Use of Satellite Imagery")
    st.markdown('''Over five weeks in October 2022, Omdena-Milan Local Chapter collaborators completed
    a local chapter challenge on applying Artificial Intelligence (AI) and Satellite imagery for
    sustainable agri-food systems.To this end, the Omdena-Milan Local Chapter collaborators explored
    various machine learning (ML) and data science techniques and geographic information systems (GIS)
    methods. The team worked on different tasks which are independent of each other to address the same 
    project goal. For demonstration, the team integrated all of them into one dashboard with good usability
    for non-technical decision-makers. 
    ''')

    



    #mp = st.image(it_map)

    # row1_col1, row1_col2 = st.columns([3, 1.3])
    # width = 800
    height = 600
    # layers = None


    url = "https://services.terrascope.be/wms/v2"

    m = leafmap.Map(center=(42.3, 14), zoom=6)
    m.add_geojson("data/limits_IT_provinces.geojson")
    # if layers is not None:
    #     for layer in layers:
    #         m.add_wms_layer(
    #             url, layers=layer, name=layer, attribution=" ", transparent=True
    #         )

    m.to_streamlit(height=height)


# def get_layers(url):
#         options = leafmap.get_wms_layers(url)
#     return options    
