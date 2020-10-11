# FLICKR API Wrapper


import json
import time
import random
import requests
from .env import SECRET, KEY
from pathlib import Path

URL = 'https://api.flickr.com/services/rest/?method=flickr.photos.search'

DEFAULT_PARAM = { 'per_page' : '500', 'page' : '1' , 'format' : 'json', 'nojsoncallback' : '1', 'has_geo' : '1', 
    'extras' : 'description, license, date_upload, date_taken, owner_name, icon_server, original_format, last_update, geo, tags, url_sq'}

def formatInput(raw):
    """ Calls flickr flickr.photos.search API method. Store results in ../response as asigned by user and request_page

    Parameters:
        raw (dict): dict of user search

    Returns:
        dict: flickr usable dict

    """
    OPTIONS = ('radius', 'radius_unit', 'accuracy', 'min_taken', 'max_taken', 'tags')
    param = {'lat' : raw['lat'], 'lon' : raw['lon'] }

    for option in OPTIONS:
        if option in raw:
            param.update({'option', raw[option]})


    return raw

def executeSearch(params, user, request_page= 1, search_id= 0):
    """ Calls flickr flickr.photos.search API method. Store results in ../response as asigned by user and request_page

    Parameters:
        request_page (int): page of results to query, default to 1
        user (int): primary key of user

    Returns:
        int: current page, total pages in results

    """
    r = requests.get(url= URL, params= params)
    response = r.json()

    print(f'Status: {r}')
    
    Path(f"../response/{user}/{search_id}").mkdir(parents= True, exist_ok= True)
    with open(f'../response/{user}/{search_id}/{request_page}.json', 'w') as f:
        json.dump(response, f)
        f.close()


    # TODO
    # Add append to master.json
    """
    with open(f'../response/{user}/{search_id}/{master}.json', 'w') as f:
        json.dump(MASTER, f)
        f.close()
    """

    # handled by either db or sessions in production
    current_page = response['photos']['page']
    total_page = response['photos']['pages']

    return current_page, total_page

def newSearch(raw_query, user, timestamp):
    """ to be callable from main.py """

    query = formatInput(raw_query)

    
    param = {**DEFAULT_PARAM, **query}
    print(param)

    # find search control variables
    #current_page, total_page = executeSearch(param, user)

    # walk search
    #while current_page <= total_page:
     #   current_page, total_page = executeSearch(param, user, request_page= current_page, search_id= timestamp)
     #   print(f'Page {current_page} of {total_page}')
      #  current_page += 1

