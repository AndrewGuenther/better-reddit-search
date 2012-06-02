import sys
import nltk
import reddit
from time import time
from doc import DocCollection

def index(days):
   r = reddit.Reddit(user_agent='better-reddit-search /u/andrewguenther')

   i = 0
   d = DocCollection()

   log_time = time() - (129600 * days)
   index_time = log_time + 1

   submissions = r.get_subreddit('technology').get_new(limit=25, url_data={'sort': 'new'})
   while index_time > log_time:

      i = 0
      for submission in submissions:
         print(submission.id + ": " + str(submission.created))
         d.add(submission)
         if i == 24:
            old = 't3_'+submission.id
            index_time = submission.created
         i+=1

      print("")
      if i < 24:
         break
      
      submissions = r.get_subreddit('technology').get_new(limit=25, url_data={'after': old, 'sort': 'new'})
