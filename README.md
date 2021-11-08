
## How to

Install the dependencies

```
$ pip3 install -r requirements.txt
```

start a ``redis`` service (the following one-liner uses docker)

```
$ docker run -d -p 6379:6379 redis
```

and finally start the celery worker

```
$ celery -A app worker --loglevel info

$ celery -A app beat --loglevel info
```


