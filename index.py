import nltk
import reddit
from doc import DocCollection

r = reddit.Reddit(user_agent='better-reddit-search /u/andrewguenther')

d = DocCollection()
old = 't3_' + d.oldest()

submissions = r.get_subreddit('technology').get_new(limit=20, url_data={'before': old})

for submission in submissions:
   d.add(submission)
