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
