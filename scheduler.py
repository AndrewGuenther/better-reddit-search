from rq import Queue
from worker import conn
from newindex import index
import sys

q = Queue(connection=conn)

q.enqueue(index, int(sys.argv[1]))
