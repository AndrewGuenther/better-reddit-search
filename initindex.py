import sys
import nltk
import reddit
from time import time
from doc import DocCollection

r = reddit.Reddit(user_agent='better-reddit-search /u/andrewguenther')

i = 0
d = DocCollection()

first = r.get_subreddit('technology').get_new(limit=1, url_data={'sort': 'new'})
after = first.next().id

subreddit = r.get_subreddit('technology')
submissions = subreddit.get_new(limit=25, url_data={'sort': 'new', 'after': "t3_" + after})

while True:
   i = 0
   for submission in submissions:
      print(submission.id)
      d.add(submission)
      if i == 24:
         after = submission.id
      i+=1

   if i != 25:
      break
   else:
      submissions = subreddit.get_new(limit=25, url_data={'sort': 'new', 'after': "t3_" + after})
      
   print("")
