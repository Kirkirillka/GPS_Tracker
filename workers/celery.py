import os
from celery import Celery
from config.utils import get_project_config

DEFAULT_CONFIG = get_project_config()

QUEUE_NAME = os.environ.get("RABBITMQ_QUEUE_NAME") or DEFAULT_CONFIG['queue']['queue_name']
HOST = os.environ.get("RABBITMQ_HOST") or DEFAULT_CONFIG['queue']['host']
PORT = os.environ.get("RABBITMQ_PORT") or DEFAULT_CONFIG['queue']['port']
USER = os.environ.get("RABBITMQ_USER") or DEFAULT_CONFIG['queue']['user']
PASSWORD = os.environ.get("RABBITMQ_USERPASS") or DEFAULT_CONFIG['queue']['password']

connection_string = f'pyamqp://{USER}:{PASSWORD}@{HOST}:{PORT}//'

celery_app = Celery(QUEUE_NAME, broker=connection_string,
                    backend='rpc://',
                    include=['workers.tasks'])

# Optional configuration, see the application user guide.
celery_app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    celery_app.start()
