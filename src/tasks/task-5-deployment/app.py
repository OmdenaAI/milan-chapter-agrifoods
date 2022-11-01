import streamlit as st
from streamlit_option_menu import option_menu
import ast
from PIL import Image
import leafmap.foliumap as leafmap
from apps import home,eda,models,demo

st.set_page_config(layout="wide")
image = Image.open('data/logo.png')
image=image.resize((100,100))
header = st.container()

apps = [
    {"func": home.app, "title": "Home", "icon": "house"},
    {"func": eda.app, "title": "EDA", "icon": "bar-chart"},
    {"func": models.app, "title": "Models", "icon": "cpu"},
    {"func": demo.app, "title": "Demo", "icon": "cloud-upload"},
]

titles = [app["title"] for app in apps]
titles_lower = [title.lower() for title in titles]
icons = [app["icon"] for app in apps]

#Using "with" notation

with st.sidebar:
    logo = st.image(image)
    selected = option_menu(
        "Main Menu",
        options=titles,
        icons=icons,
        menu_icon="cast",
    )

for app in apps:
    if app["title"] == selected:
        app["func"]()
        break
