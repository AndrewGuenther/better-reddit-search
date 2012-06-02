import sys
import nltk
import reddit
from time import time
from doc import DocCollection
from rq import Queue
from worker import conn

def index(after):
   q = Queue(connection=conn)
   r = reddit.Reddit(user_agent='better-reddit-search /u/andrewguenther')

   i = 0
   d = DocCollection()

   log_time = time() - (129600 * days)
   index_time = log_time + 1

   submissions = r.get_subreddit('technology').get_new(limit=25, url_data={'sort': 'new', 'after': "t3_" + after})

   i = 0
   for submission in submissions:
      print(submission.id)
      d.add(submission)
      if i == 24:
         q.enqueue(index, submission.id)
      i+=1

   print("")
