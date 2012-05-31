from rq import Queue
from worker import conn
from newindex import index

q = Queue(connection=conn)

q.enqueue(index)
