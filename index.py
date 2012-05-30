import sys
import nltk
import reddit
from doc import DocCollection

r = reddit.Reddit(user_agent='better-reddit-search /u/andrewguenther')

i = 0
d = DocCollection()
#old = 't3_' + d.oldest()
old = 't3_' + sys.argv[1]

while True:
   submissions = r.get_subreddit('technology').get_new(limit=25, url_data={'before': old, 'sort': 'new'})

   i = 0
   for submission in submissions:
      print(submission.id + ": " + str(submission.created))
      d.add(submission)
      if i == 0:
         old = 't3_'+submission.id
      i+=1

   print("")
   if i < 24:
      break
