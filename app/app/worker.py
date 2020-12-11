import os

from celery import Celery

from . import create_app


def create_celery(app):

    celery = Celery(
        app.import_name,
        backend=os.environ.get("CELERY_BACKEND"),
        broker=os.environ.get("CELERY_BROKER"),
        ignore_result=False,
        task_ignore_result=False,
    )

    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):

            with app.app_context():

                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


celery = create_celery(create_app())
