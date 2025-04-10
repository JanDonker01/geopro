import streamlit as st
import folium
from streamlit_folium import st_folium
from fastkml import kml
from shapely.geometry import Polygon

st.set_page_config(layout='wide')
st.title('GeoPercel PRO – Webversie')

uploaded_file = st.file_uploader('Upload een KML-bestand', type=['kml'])
if uploaded_file:
    kml_str = uploaded_file.read().decode('utf-8')
    k = kml.KML()
    k.from_string(kml_str)
    placemarks = []
    for feature in k.features():
        for sub_feature in feature.features():
            if hasattr(sub_feature, 'geometry'):
                placemarks.append(sub_feature)
    m = folium.Map(location=[52.372, 4.896], zoom_start=16)
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri', name='Esri Satellite', overlay=False, control=True
    ).add_to(m)
    for placemark in placemarks:
        geom = placemark.geometry
        if isinstance(geom, Polygon):
            coords = list(geom.exterior.coords)
            latlon = [(lat, lon) for lon, lat in coords]
            folium.Polygon(
                locations=latlon, color='blue', weight=2,
                fill=True, fill_opacity=0.4,
                popup=placemark.name or 'Perceel'
            ).add_to(m)
    st_folium(m, width=1000, height=600)
