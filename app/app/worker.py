from celery import Celery

from . import create_app


def create_celery(app):

    celery = Celery(
        app.import_name,
        backend="redis://redis:6379/0",
        broker="redis://redis:6379/0",
        ignore_result=False,
        task_ignore_result=False,
        #include=[f'{app.import_name}.search_control']
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
