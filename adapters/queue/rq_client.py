from redis import Redis
from rq import Queue
import os

redis_conn = Redis.from_url(os.getenv("REDIS_URL"))
queue = Queue(connection=redis_conn)