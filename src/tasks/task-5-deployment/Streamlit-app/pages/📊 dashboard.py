import streamlit as st
import pandas as pd
import geopandas as gpd
from millify import millify
import folium
from PIL import Image
from streamlit_folium import st_folium

APP_TITLE = "Italy Agrifoods Data"
APP_SUB_TITLE = "by Omdena Milan chapter 👇 (https://omdena.com/local-chapters/milan-italy-chapter/)"
image = Image.open('data/logo.png')
image=image.resize((100,100))



def display_time_filters(df):
    year_list = list(df['TIME'].unique())
    year_list.sort()
    year = st.selectbox('Year', year_list, len(year_list)-1)
    #st.header(f'{year}')
    return year

def display_product():
    product_list= ['Cereals', 'Vegetables', 'Fruits', 'Olive']
    product = st.selectbox('Agricultural Product',product_list)
    return product 

def display_state_filter(df, Region):
    region_list = [''] + list(df['Region'].unique())
    region_list.sort()
    state_index = region_list.index(Region) if Region and Region in region_list else 0
    return st.selectbox('Region', region_list, state_index)

def display_yield(df, year, region, metric_title):
    df = df[df["TIME"] == year]
    if region:
        df = df[df["Region"] == region]
    total = df['Value'].sum()
    st.metric(metric_title, millify(total))

def display_map(df, year):
    df = df[df["TIME"] == year]
    map = folium.Map(location=[42.3, 13], zoom_start=5,scrollWheelZoom=False,  tiles='CartoDB positron')
    gpd_data = gpd.read_file("data/Italy_regions.zip")
    #st.write(gpd_data[gpd_data['NAME_1']=="Valle d'Aosta"])
    #st.write(gpd_data)
    ch = folium.Choropleth(
            geo_data=gpd_data,
            data=df,
            columns=['region_code', 'Value'],
            key_on="feature.properties.ID_1",
            fill_color='YlGn',
            highlight=True
    ).add_to(map)
    ch.geojson.add_child(
        folium.features.GeoJsonTooltip(['NAME_1'], labels=False)
    )
    st_map = st_folium(map, width=700, height= 450)
    
    region_name = ''
    if st_map['last_active_drawing']:
        region_name = st_map['last_active_drawing']['properties']['NAME_1']
        if region_name == 'Sicily':
            return 'Sicilia'
        if region_name == 'Apulia':
            return 'Puglia'
    return region_name

def main():
    st.set_page_config(APP_TITLE, layout="centered")
    st.title(APP_TITLE)
    

    image = Image.open('data/logo.png')
    image=image.resize((100,100))

    with st.sidebar:
        logo = st.image(image)
        st.caption(APP_SUB_TITLE)

    #load data
    df_olives = pd.read_csv("data/Italy_regions_with_code_grapes_olives.csv")    
    df_cereals = pd.read_csv("data/Italy_regions_with_code_cereals.csv")
    df_veg = pd.read_csv("data/Italy_regions_with_code_fresh_veg.csv")
    df_fruit = pd.read_csv("data/Italy_regions_with_code_fruit.csv")
    df = df_fruit
    year = ''
    region = ""
    
    

    #st.write(df.shape)
    #st.write(df.head())

    
    product = display_product()
    col1, col2 = st.columns(2)
    
    #display map
    with col1:
        
        year = display_time_filters(df)
        
    #st.header('{Header!!!!}')
    
    
    with col2:
        #display metric
        region = display_state_filter(df, region)
        metric_title = f"{product} Harvested Production in Quintals {region} - Italy: {year}"     
        display_yield(df, year, region, metric_title)
         
    region = display_map(df, year)
        
    #st.header('{Header!!!!}')
   
    

    
    #metric_title = f"Harvested Production in Quintals {region} - Italy: {year}" 

if __name__ == "__main__":
    main()
    