from redbeat import RedBeatSchedulerEntry as Entry

from celery.schedules import crontab, schedule
from src.celery.tasks import mul, su


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


def test_add_redbeat(celery_app, celery_worker):
    @celery_app.task
    def test_task(x, y):
        return x * y

    sch = schedule(run_every=10.0)
    anentry = Entry(
        "test_task", "src.celery.tasks.test_task", schedule=sch, args=[1, 2], app=celery_app
    )
    anentry.save()
    entry = Entry.from_key("redbeat:test_task", app=celery_app)
    assert entry.enabled
    assert entry.name == "test_task"
    assert entry.task == "src.celery.tasks.test_task"
    assert entry.schedule == schedule(run_every=10.0)

    entry.enabled = False
    entry.save()
    entry = Entry.from_key("redbeat:test_task", app=celery_app)
    assert not entry.enabled

    sch = crontab(minute=10, hour=10)
    entry.schedule = sch
    entry.save()
    entry = Entry.from_key("redbeat:test_task", app=celery_app)
    assert entry.schedule == crontab(minute=10, hour=10)

    entry.delete()
    try:
        entry = Entry.from_key("redbeat:test_task", app=celery_app)
        assert False
    except KeyError:
        assert True
