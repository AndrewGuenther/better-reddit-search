from rq import Queue
from worker import conn
from workerindex import index
import sys
import reddit

q = Queue(connection=conn)

r = reddit.Reddit(user_agent='better-reddit-search /u/andrewguenther')
submissions = r.get_subreddit('technology').get_new(limit=1, url_data={'sort': 'new'})
first = submissions.next()

q.enqueue(index, first.id)
