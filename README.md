
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
 -------------- celery@whatever v5.0.5 (singularity)
--- ***** ----- 
-- ******* ---- Linux-5.9.0-5-amd64-x86_64-with-glibc2.29 2021-01-28 15:38:25
- *** --- * --- 
- ** ---------- [config]
- ** ---------- .> app:         tasks:0x7f47d06bf2b0
- ** ---------- .> transport:   redis://localhost:6379//
- ** ---------- .> results:     disabled://
- *** --- * --- .> concurrency: 8 (prefork)
-- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
--- ***** ----- 
 -------------- [queues]
                .> celery           exchange=celery(direct) key=celery
                

```
$ celery -A app beat --loglevel info

