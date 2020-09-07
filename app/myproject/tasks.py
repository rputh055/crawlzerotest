import time

from myproject.celery_app import app as celery_app


@celery_app.task
def do_some_queries():
    time.sleep(10)
    return "Hello"


@celery_app.task
def query_every_five_mins():
    pass