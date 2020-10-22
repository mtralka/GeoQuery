# FLICKR API Wrapper

import json
import time
import random
import requests
from .env import SECRET, KEY
from pathlib import Path

import geopandas as gpd
#from shapely.geometry import Point

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

def executeSearch(params, user, request_page= 1, search_id= 0, master= False):
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
    
    #Path(f"./response/{user}/{search_id}").mkdir(parents= True, exist_ok= True)
    #with open(f'./response/{user}/{search_id}/{request_page}.json', 'w') as f:
    #    json.dump(response, f)
    #    f.close()

    # read to df
    # create geodf w/ shapely

    #if master:
    #    master_df = gpd.read_file(response, geometry=)

    # TODO
    # Add append to master.json
    """
    # id is now id not timestamp, adjust accordingly
    with open(f'../response/{user}/{search_id}/{master}.json', 'w') as f:
        json.dump(MASTER, f)
        f.close()
    """
    try:
        current_page = response['photos']['page']
        total_page = response['photos']['pages']
    except ValueError:
        print('Value Error')
        print(response)
    
    return current_page, total_page

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

    current_page, total_page = executeSearch(param, user, search_id = timestamp, master=True)

    # walk search
    while current_page <= total_page:
        current_page, total_page = executeSearch(param, user, request_page= current_page, search_id= timestamp)
        print(f'Page {current_page} of {total_page}')
        current_page += 1

        self.update_state(state=f'PROGRESS',
            meta={'current': current_page, 'total': total_page,'status': 'in progress'})

    return {'current': current_page, 'total': total_page, 'status': 'Task completed',
            'result': 'resulting'}
        

