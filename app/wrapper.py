# FLICKR API Wrapper

import json
import time
import random
import requests
from .env import SECRET, KEY
from pathlib import Path
import os

import geopandas as gpd
import pandas as pd

from . import celery

URL = 'https://api.flickr.com/services/rest/?method=flickr.photos.search'

DEFAULT_PARAM = { 'per_page' : '500' , 'format' : 'json', 'nojsoncallback' : '1', 'has_geo' : '1', 'api_key' : KEY, 
    'extras' : 'description, license, date_upload, date_taken, owner_name, icon_server, original_format, last_update, geo, tags, url_sq'}

def formatInput(raw):
    """ convert user input to usable api dict

    Parameters:
        raw (dict): dict of user search

    Returns:
        dict: flickr usable dict

    """

    POSSIBLE_PARAMS = ('radius', 'radius_unit', 'accuracy', 'min_taken', 'max_taken', 'tags')
    param = {'lat' : raw['lat'], 'lon' : raw['lon'] }

    for term in POSSIBLE_PARAMS:
        if term in raw and len(raw[term]) > 0:
            param[term] = raw[term]

    return param

def executeSearch(params, user, request_page= 1, search_id= 0, master= False, df=None, total_page=None):
    """ Calls flickr flickr.photos.search API method. Store results in ../response as asigned by user and request_page

    Parameters:
        request_page (int): page of results to query, default to 1
        user (int): primary key of user

    Returns:
        int: current page, total pages in results

    """
    params['page'] = request_page
    r = requests.get(url= URL, params= params)
    response = r.json()

    print(f'Status: {r}')

    if master:
        df = pd.DataFrame.from_dict(response['photos']['photo'], orient='columns')
        total_page = response['photos']['pages']
        
    else:
        df = df.append( pd.DataFrame.from_dict(response['photos']['photo'], orient='columns') , ignore_index=True )
   
    try:
        current_page = response['photos']['page']
        
    except ValueError:
        print('Value Error')
        print(response)

    if str(response['photos']['pages']) == '0':
        print(response)
        time.sleep(10)

        current_page = current_page - 1
    
    return current_page, total_page, df, total_page

def toGeo(df):
    """ convert dataframe to geodataframe """
    return gpd.GeoDataFrame(df, geometry= gpd.points_from_xy(df.longitude, df.latitude))

@celery.task(bind= True)
def newSearch(self, raw_query, user, timestamp):
    """ master seach initiation
    
    Parameters:
        raw_query (dict): raw user dict
        user (string): primary key of user
        timestamp (string): UNIX Timestamp
    
     """

    query = formatInput(raw_query)
    param = {**DEFAULT_PARAM, **query}

    current_page, total_page, master_df,total_page = executeSearch(param, user, search_id = timestamp, master=True)

    # walk search
    while current_page <= total_page:
        current_page, total_page, master_df, total_page = executeSearch(param, user, request_page= current_page, search_id= timestamp, df=master_df, total_page= total_page)
        print(f'Page {current_page} of {total_page}')
        current_page += 1

        self.update_state(state=f'IN PROGRESS',
            meta={'current': current_page, 'total': total_page,'status': 'searching...'})

        time.sleep(.5)

    # create geodf
    master_df = toGeo(master_df)
    print('Count' + str(master_df.count))
    # write to file
    file_path = f"./response/{user}/{timestamp}"
    Path(file_path).mkdir(parents= True, exist_ok= True)
    master_df.to_file(file_path + '/master.geojson', driver='GeoJSON')

    return {'current': current_page, 'total': total_page, 'status': '',
            'result': 'resulting'}