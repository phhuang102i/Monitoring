"""
Generic module to demonstrate simple patterns for celery tasks.
"""
from app import app
from celery import Signature
RABBITMQ_USER = 'omnisegment'
RABBITMQ_PWD = ''
RABBITMQ_HOST = 'localhost:15672'
SLACK_WEBHOOK_URL = ''




def get_current_stat_of_queue(session, queue_name):
    import json

    response = session.get(f'http://{RABBITMQ_HOST}/api/queues/%2f/{queue_name}')
    content = json.loads(response.content)
    return {
        'num_of_message_ready': content['messages_ready'],
        'message_incoming_rate': content['message_stats']['publish_details']['rate'],
        'message_ack_rate': content['message_stats']['ack_details']['rate']
        
    }

@app.task
def check_queue_every_5_mins():
    from .connect import setup_ssh_tunnel
    import requests
    import json
    setup_ssh_tunnel()
    session = requests.Session()
    session.auth = (RABBITMQ_USER, RABBITMQ_PWD)
    result = {}
    result['SEND_PQ'] = get_current_stat_of_queue(session, 'send_pq')
    result['WORKFLOW_PQ'] = get_current_stat_of_queue(session, 'workflow_pq')
    result['BEACON'] = get_current_stat_of_queue(session, 'beacon')
    result['BATCH_QUERY'] = get_current_stat_of_queue(session, 'batch-query')

    response = requests.post(SLACK_WEBHOOK_URL, json={'text':str(result)})
    
    return result
