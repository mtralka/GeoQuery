from datetime import datetime
from pathlib import Path
import random
import string

import branca
import folium
from folium import plugins
import geopandas as gpd
import pandas as pd

from . import db
from .model import Query


""" return UNIX timestamp from string """


def create_timestamp(val):
    return datetime.strptime(str(val), "%Y-%m-%d").timestamp()


""" Create unique ID not in DB """


def create_unique_id(length=5):

    while True:

        id = "".join(
            random.choice(string.ascii_uppercase + string.digits) for i in range(length)
        )

        if Query.query.filter_by(friendly_id=id).first():
            pass
        else:
            break

    return id


def toGeo(df):
    """ convert dataframe to geodataframe """
    return gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude))


def toFile(df, user, timestamp, format="GeoJSON"):

    file_path = f"./response/{user}/{timestamp}"
    Path(file_path).mkdir(parents=True, exist_ok=True)

    if format == "GeoJSON":
        df = toGeo(df)
        df.to_file(file_path + "/master.geojson", driver="GeoJSON")
    elif format == "CSV":
        df.to_csv(file_path + "/master.csv", index=False)

    elif format == "PICKLE":
        df.to_pickle(file_path + "master.pkl")
