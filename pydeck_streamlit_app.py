import pydeck as pdk
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import streamlit as st

# Page config
st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded"
)

# Write title
st.title('Volcano Sample Around the World')

# Import data
@st.cache_data
def load_data():
    volcanos = gpd.read_file('https://services.arcgis.com/BG6nSlhZSAWtExvp/arcgis/rest/services/World_Volcanoes/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson')
    volcanos['color'] = volcanos.ELEV.apply(lambda x: [(i * 255) for i in plt.cm.Blues((x-volcanos.ELEV.min()) / (volcanos.ELEV.max() - volcanos.ELEV.min()))[0:3]])
    return volcanos
volcanos = load_data()

# Type selector
sel_type = st.multiselect('Simple Type', volcanos.SimpleType.unique(), default=volcanos.SimpleType.unique())

# View State
view_state = pdk.ViewState(
                longitude=volcanos.Lon.mean(),
                latitude=volcanos.Lat.mean(),
                zoom=1,
                min_zoom=1,
                max_zoom=15
            )

# Points Layer
layer_pts = pdk.Layer(
    type="ScatterplotLayer",
    data=volcanos[volcanos.SimpleType.isin(sel_type)],
    get_fill_color='[color[0], color[1], color[2]]',
    get_radius=1,
    pickable=True,
    radius_scale=1,
    radius_min_pixels=5,
    radius_max_pixels=500,
    get_position='[Lon, Lat]'
    )

# Pydeck object
pdk_map = pdk.Deck(
            map_provider='carto',
            map_style='light',
            initial_view_state=view_state,
            layers=[layer_pts]
            )

# Display pydeck map
st.pydeck_chart(pdk_map)
