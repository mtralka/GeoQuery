
from . import celery
from .flickr_wrapper import flickrControl


@celery.task(bind=True)
def newSearch(self, raw_query, user, timestamp, friendly_id):
    """ Controls master execution of all search functions
    Parameters:
        raw_query (dict): raw user dict
        user (string): primary key of user
        timestamp (string): UNIX Timestamp
     """
    celery_task = self

    # Launch Flickr Search
    flickrControl(raw_query, user, timestamp, celery_task)

    return {'current': '2', 'total': '1', 'status': '',
            'result': f'/results/{friendly_id}/map'}
