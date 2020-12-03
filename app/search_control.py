from . import celery
from .scraper.flickr import flickr


@celery.task(bind=True)
def new_search(self, data, user, task_time, friendly_id, task):

    celery_task = self

    flckr = flickr(user, task_time, friendly_id, celery_task, data)
    flckr.search(first_run=True)
    flckr.make_files()

    return {
        "current": flckr.current_page,
        "total": flckr.total_page,
        "status": "FINISHED"
    }
