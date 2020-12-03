# :earth_americas: GeoQuery

### *Search, Know, Change*

![Code_Grade](https://www.code-inspector.com/project/16749/status/svg) ![Code_Quality_Score](https://www.code-inspector.com/project/16749/score/svg) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) <br/>
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) ![GitHub language count](https://img.shields.io/github/languages/count/mtralka/GeoQuery) [![Generic badge](https://img.shields.io/badge/Status-Development-orange.svg)](https://shields.io/) 



#### **Objective**

 Create an online platform to facilitate cross-service social media spatio-temporal searches and analysis. Bringing big-data information retreival to all.
 

#### Project Status

 Currently, GeoQuery is in an early (but operational) Beta mode. Initial V1 release with Flickr integration is estimated for mid-November. Facebook and Twitter integration will follow.
 

 
**Task**|**Description**|**Status**|**Finished**
:-----:|:-----:|:-----:|:-----:
Flickr Integration|validated to 200k results / 20 minutes|done| :heavy_check_mark:
FB Integration| |not started| :heavy_minus_sign:
Twitter Integration| |not started| :heavy_minus_sign:
Results page|fully implemented, design could use work|usable|   :soon:
home page|design could use work|in progress|  :heavy_minus_sign:
about page| |in progress| :heavy_minus_sign:
DB|done|done| :heavy_check_mark:
login / signup page|backend implemented, needs front|in progress| :soon:
Async tasking| celery /redis (docker) |done| :heavy_check_mark:
task id shortening| |done| :heavy_check_mark:
results management|geojson & csv implemened |done |  :heavy_check_mark:
AJAX endpoint|fully implemented, review edge cases|done| :heavy_check_mark:
scheduled searches | |not started| :heavy_minus_sign:
email alerts | |not started| :heavy_minus_sign:
dynamic mapping | folium |done| :heavy_check_mark:
results serving | map done. need CSV + GeoJSON |in progress| :soon:
css transition | adoption of tailwindcss |in progress| :soon:

*this ReadMe is a work in progress. Please check back soon or contact me for more information.*


#### Examples

**frontend re-design in progress**
*Current as of 10.26 - subject to change*


- [CSV results](example/exampleCSV.csv)
- [GeoJSON results](example/exampleGeoJSON.geojson)

 <a href="url"><img src="example/resultsPage.PNG" align="center" height="400" width="" ></a><br/>
*status of results page*


 <a href="url"><img src="example/searchPage.PNG" align="center" height="400" width="" ></a><br/>
 *status of search page*
 
 
