from celapp.tasks import mul, su
from redbeat import RedBeatSchedulerEntry as Entry

def test_celery_raw_fixtures(celery_app, celery_worker):
    assert mul.delay(4, 4).get(timeout=10) == 16


def test_create_task(celery_app, celery_worker):
    @celery_app.task
    def mul(x, y):
        return x * y

    celery_worker.reload()
    assert mul.delay(4, 4).get(timeout=10) == 16

def test_su(celery_app, celery_worker):
    assert su.delay(4, 4).get(timeout=10) == 8


def test_add_shceeduler(celery_app, celery_worker):
    anentry = Entry('mul', 'celapp.tasks.mul', schedule=1.0, args=[1, 2], app=celery_app)
    anentry.save()
    assert True
