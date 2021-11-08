from celery import Celery
from celery.schedules import crontab

app = Celery('tasks', broker='redis://localhost')

app.conf.imports = (
    'foo.tasks',
)

app.conf.beat_schedule = {
    'check-queue-every-5-mins': {
        'task': 'foo.tasks.check_queue_every_5_mins',
        'schedule': crontab(minute='*/5',
                            hour='1-15'),
        'args': ()
    },
}
