from celery import Celery
from celery.schedules import schedule, crontab
from redbeat import RedBeatSchedulerEntry as Entry

# celery -A celapp worker
# celery -A celapp beat -S redbeat.RedBeatScheduler

app = Celery(
    'celapp', 
    broker='redis://localhost:6379/0', 
    backend='redis://localhost:6379/0',
    redbeat_redis_url = "redis://localhost:6379/1",
    redbeat_lock_key = None
)
app.autodiscover_tasks(['celapp'])

interval = schedule(run_every=60)

entry = Entry('mul', 'celapp.tasks.mul', interval, args=[1, 2], app=app)
entry.save()
