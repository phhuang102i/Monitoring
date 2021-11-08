"""
Generic module to demonstrate simple patterns for celery tasks.
"""
from app import app
from celery import Signature
RABBITMQ_USER = 'omnisegment'
RABBITMQ_PWD = 'symp5674xnbpvp6wngn6z8hfppc3cefp'
RABBITMQ_HOST = 'localhost:15672'
SLACK_WEBHOOK_URL = 'https://hooks.slack.com/services/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'


@app.task
def task_a(whatever: str):
    print(whatever)


@app.task
def task_b(whatever: str):
    print(whatever)


def build_chain(arg1, arg2, on_success, on_failure):
    return task_a.si(arg1).on_error(on_failure) | \
        task_b.si(arg2).on_error(on_failure) | \
        on_success


@app.task
def big_task(on_success_name, on_failure_name, *args):
    """This task chains the other two with some orchestration work."""
    # if you want to obtain also the traceback for the on_failure
    # you need to not use an immutable signature
    on_success = Signature(on_success_name, args=args)
    on_failure = Signature(on_failure_name, args=args)
    chain = build_chain('hello', 'world', on_success, on_failure)
    chain()


def fill_result(session, queue_name):
    import json

    response = session.get(f'http://{RABBITMQ_HOST}/api/queues/%2f/{queue_name}')
    content = json.loads(response.content)
    return {
        'num_of_message_ready': content['messages_ready'],
        'message_incoming_rate': content['message_stats']['publish_details']['rate'],
        'message_ack_rate': content['message_stats']['ack_details']['rate']
        
    }

@app.task
def check_queue_every_30_seconds():
    from .connect import setup_ssh_tunnel
    import requests
    import json
    setup_ssh_tunnel()
    session = requests.Session()
    session.auth = (RABBITMQ_USER, RABBITMQ_PWD)
    result = {}
    result['SEND_PQ'] = fill_result(session, 'send_pq')
    result['WORKFLOW_PQ'] = fill_result(session, 'workflow_pq')
    result['BEACON'] = fill_result(session, 'beacon')
    result['BATCH_QUERY'] = fill_result(session, 'batch-query')

    response = requests.post(SLACK_WEBHOOK_URL, json={'text':str(result)})
    
    return result
