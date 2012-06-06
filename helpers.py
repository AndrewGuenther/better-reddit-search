import nltk
import reddit
from string import lower
from math import sqrt

def exists(id, cur):
   cur.execute('select count(*) from post natural join text_block where thing_id=%s;', [id])
   res = cur.fetchone()

   if int(res[0]) == 1:
      return True
   else:
      return False

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

   cur.execute('select id, title, link from search(%s, %s) where rank > 0', [parsed_query, 100])

   return cur.fetchall()

def redditsearch(query, cur):
   r = reddit.Reddit(user_agent='better-reddit-search /u/andrewguenther')

   api_results = r.get_subreddit('technology').search(query, limit=100, sort='new')

   filtered_results = []

#   cur.execute('select min(post_time) from post;')
#   oldest = cur.fetchone()[0]

   for result in api_results:
#      if result.created > oldest and exists(result.id, cur):
      if exists(result.id, cur):
         filtered_results.append((result.id, result.title.encode('utf-8'), result.url.encode('utf-8'), result.ups, result.downs))

   filtered_results = sorted(filtered_results, key=wilson_sort, reverse=True)

   return filtered_results
