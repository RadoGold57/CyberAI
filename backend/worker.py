import os
from redis import Redis
from rq import Worker, Queue, Connection

listen = ["scans"]

default_host = "redis" if os.environ.get("DOCKER_ENV") else "localhost"
redis_conn = Redis(host=os.getenv("REDIS_HOST", default_host), port=6379)

if __name__ == "__main__":
    with Connection(redis_conn):
        worker = Worker(map(Queue, listen))
        worker.work()
