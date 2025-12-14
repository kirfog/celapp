from celery import shared_task
# from celapp.celery import app

@shared_task
def mul(x, y):
    return x * y


# @app.task
@shared_task
def su(x, y):
    return x + y