from celery import Celery
from celapp.rb import load_redbeat_tasks
import yaml

# celery -A celapp worker
# celery -A celapp beat -S redbeat.RedBeatScheduler

app = Celery(
    'celapp',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
    redbeat_redis_url="redis://localhost:6379/1",
    redbeat_lock_key=None
)

app.autodiscover_tasks(['celapp'])


with open("celapp/cel.yml", "r") as f:
    tasks_config = yaml.safe_load(f) or {}

load_redbeat_tasks(app, tasks_config)
