from celery.schedules import crontab, schedule
from redbeat import RedBeatSchedulerEntry as Entry

from src.celery.tasks import task4


def test_task4(celery_app, celery_worker):
    res = {"task": "task4", "result": 4 * 4}
    assert task4.delay(4, 4).get(timeout=10) == res


def create_task(celery_app):
    @celery_app.task
    def test_task(x, y, mult=1):
        return x * y * mult

    return test_task


def add_task_schedule(celery_app):
    sch = schedule(run_every=10.0)
    entry = Entry(
        "test_task",
        "tests.test_celery.test_task",
        schedule=sch,
        args=[1, 2],
        app=celery_app,
    )
    entry.save()
    return entry


def change_task_schedule(celery_app):
    entry = Entry.from_key("redbeat:test_task", app=celery_app)
    sch = crontab(minute=10, hour=10)
    entry.schedule = sch
    entry.save()
    entry = Entry.from_key("redbeat:test_task", app=celery_app)
    return entry


def disable_task(celery_app):
    entry = Entry.from_key("redbeat:test_task", app=celery_app)
    entry.enabled = False
    entry.save()
    return entry


def delete_task(celery_app):
    entry = Entry.from_key("redbeat:test_task", app=celery_app)
    entry.delete()
    return entry


def test_add_task(celery_app, celery_worker):
    test_task = create_task(celery_app)
    celery_worker.reload()
    assert test_task.delay(4, 4, mult=4).get(timeout=10) == 64


def test_add_task_schedule(celery_app, celery_worker):
    create_task(celery_app)
    add_task_schedule(celery_app)
    entry = Entry.from_key("redbeat:test_task", app=celery_app)
    assert entry.enabled
    assert entry.name == "test_task"
    assert entry.task == "tests.test_celery.test_task"
    assert entry.schedule == schedule(run_every=10.0)


def test_change_task_schedule(celery_app, celery_worker):
    create_task(celery_app)
    add_task_schedule(celery_app)
    entry = change_task_schedule(celery_app)
    assert entry.schedule == crontab(minute=10, hour=10)


def test_disable_task(celery_app, celery_worker):
    create_task(celery_app)
    add_task_schedule(celery_app)
    change_task_schedule(celery_app)
    entry = disable_task(celery_app)
    assert not entry.enabled


def test_delete_task(celery_app, celery_worker):
    create_task(celery_app)
    add_task_schedule(celery_app)
    change_task_schedule(celery_app)
    disable_task(celery_app)
    delete_task(celery_app)
    try:
        Entry.from_key("redbeat:test_task", app=celery_app)
        assert False
    except KeyError:
        assert True
