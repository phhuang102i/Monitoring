from celery import Celery

app = Celery('tasks', broker='redis://localhost')

app.conf.imports = (
    'foo.tasks',
)

app.conf.beat_schedule = {
    'check-queue-every-30-seconds': {
        'task': 'foo.tasks.check_queue_every_30_seconds',
        'schedule': 30.0,
        'args': ()
    },
}
