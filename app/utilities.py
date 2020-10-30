import string, random, folium, branca
import geopandas as gpd
import pandas as pd
from datetime import datetime

from folium import plugins
from pathlib import Path

from . import db
from .model import Query

""" return UNIX timestamp from string """
def create_timestamp(val):
    return datetime.strptime(str(val), '%Y-%m-%d').timestamp()


""" Create unique ID not in DB """
def create_unique_id(length= 5):

    while True:

        id = ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(length))

        if Query.query.filter_by(friendly_id= id).first():
            pass
        else:
            break

    return id


def toGeo(df):
    """ convert dataframe to geodataframe """
    return gpd.GeoDataFrame(df, geometry= gpd.points_from_xy(df.longitude, df.latitude))

def toFile(df, user, timestamp, format='GeoJSON'):

    file_path = f"./response/{user}/{timestamp}"
    Path(file_path).mkdir(parents= True, exist_ok= True)

    if format == 'GeoJSON':
        df = toGeo(df)
        df.to_file(file_path + '/master.geojson', driver='GeoJSON')
    
    elif format == 'CSV':
        df.to_csv(file_path + '/master.csv', index=False)

    elif format == 'PICKLE':
        df.to_pickle(file_path + 'master.pkl')

def toMap(df, user, timestamp, lat, lon):

    file_path = f"app/templates/maps/{user}/{timestamp}"
    df = toGeo(df)

    m = folium.Map(
        location=[lat, lon],
        API_key='pk.eyJ1IjoibXRyYWxrYSIsImEiOiJja2VjNm5hdWEwNjQ4MnZ0cHlycXlndnN5In0.mfQAFUPzfGZeMht0EToJBA',
        attr='Mapbox | <strong>GeoQuery by Matthew Tralka</strong>',
        zoom_start= 14,
        min_zoom= 1,
        prefer_canvas=True,
        tiles="https://api.mapbox.com/styles/v1/mapbox/satellite-v8/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibXRyYWxrYSIsImEiOiJja2VjNm5hdWEwNjQ4MnZ0cHlycXlndnN5In0.mfQAFUPzfGZeMht0EToJBA"
    )
    
    points = folium.FeatureGroup(name= 'Flickr Points')

    for ownername, title, date_taken, tags, latitude, longitude, accuracy, url_l in zip(
        df['ownername'], df['title'], df['datetaken'], df['tags'], df['latitude'], df['longitude'],
        df['accuracy'], df['url_l'] ):

        html = f"""
        <a href='{url_l}' target='_blank'> {title}</a>
        <br/><strong>Owner:</strong> {ownername}
        <br/><strong>Date Taken:</strong> {date_taken}
        <br/><strong>Accuracy:</strong> {accuracy}
        <br/><strong>Tags:</strong> {tags}
        """

        iframe = branca.element.IFrame(html= html , width = 220, height= 130)

        points.add_child(folium.CircleMarker(location=[latitude,longitude] , fill_opacity=.7, 
            fill_color='blue', radius=4, color='red', opacity=.6, popup=(folium.Popup(iframe, max_width= 220))))

    m.add_child(points)

    fullscreen = plugins.Fullscreen()
    m.add_child(fullscreen)

    minimap = plugins.MiniMap(zoom_level_offset=-4, toggle_display=True)
    m.add_child(minimap)
    print(file_path)
    Path(file_path).mkdir(parents= True, exist_ok= True)
    m.save(file_path + '/master.html')
    print('creted')


