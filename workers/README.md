# Running Worker Poll

## Prerequisites

```bash
pip install celery
```

Also requires **placement** package, which is not publicly available.
For development, there is a folder called 'dist', there will be closed packages
to be installed during image preparation. 

## Running up a RabbitMQ queue

In the parent directory execute

```bash
docker-compose up -d rabbitmq
```

## Running one worker

In the parent (above, ../) directory executre


```bash
celery -A workers worker --loglevel=info
```