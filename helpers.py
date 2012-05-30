import nltk
import reddit
from string import lower
from math import sqrt

def wilson_sort(elem):
   #assumes [0] = ups & [1] = downs
   ups = elem[3]
   downs = elem[4]

   n = ups + downs
   z = 1.6 #1.0 = 85%, 1.6 = 95%

   if n > 0:
      phat = float(ups) / n
   else:
      return 0

   return sqrt(phat+z*z/(2*n)-z*((phat*(1-phat)+z*z/(4*n))/n))/(1+z*z/n)

def mysearch(query, cur):
   toks = nltk.word_tokenize(query)
   stemmer = nltk.stem.porter.PorterStemmer()
   parsed_query = []

   for tok in toks:
      parsed_query.append(stemmer.stem(lower(tok)))

   cur.execute('select id, title, link from search(%s, %s) where rank > 0', [parsed_query, 15])

   return cur.fetchall()

def redditsearch(query, cur):
   r = reddit.Reddit(user_agent='better-reddit-search /u/andrewguenther')

   api_results = r.get_subreddit('technology').search(query, limit=100, sort='new')

   filtered_results = []

   cur.execute('select min(post_time) from post;')
   oldest = cur.fetchone()[0]

   for result in api_results:
      if result.created > oldest:
         filtered_results.append((result.id, result.title, result.url, result.ups, result.downs))

   filtered_results = sorted(filtered_results, key=wilson_sort, reverse=True)

   return filtered_results
