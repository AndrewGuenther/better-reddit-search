import nltk
import reddit
import psycopg2
import time
from math import sqrt
from string import lower
from consts import TITLE, SELF, COMMENT

class DocCollection:

   def __init__ (self):
      self.conn = psycopg2.connect("dbname=redditsearch user=andrew password=password")
      self.conn.autocommit = False
      self.cur = self.conn.cursor()     

   def wilson (self, ups, downs):
      n = ups + downs
      z = 1.6 #1.0 = 85%, 1.6 = 95%
      phat = float(ups) / n
      return sqrt(phat+z*z/(2*n)-z*((phat*(1-phat)+z*z/(4*n))/n))/(1+z*z/n)
     

   def build_dist (self, body, wilson):
      stemmer = nltk.stem.porter.PorterStemmer()

      stems = []

      for word in nltk.word_tokenize(body):
         if len(word) < 20:
            stems.append(stemmer.stem(lower(word)))
      stems = [w for w in stems if not w in nltk.corpus.stopwords.words('english')]

      freqs = nltk.probability.FreqDist(stems)

      for key in freqs:
         if freqs[key] > 0:
            freqs[key] = freqs[key] #*= wilson
         else:
            del(freqs[key])
      
      return freqs

   def insert_dist (self, dist, post_id, kind):
      for word in dist:
         if dist[word] > 0:
            self.cur.execute("update word set df = df + 1 where word=%s;", [word])
            self.cur.execute("insert into word (word, df) select %s, 1 where not exists (select 1 from word where word=%s);",
               [word, word])
            self.cur.execute("update word_instance set freq = freq + %s where word=%s and pid=%s and kind=%s;",
               [dist[word], word, post_id, kind])
            self.cur.execute("insert into word_instance select %s, %s, %s, %s where not exists (select 1 from word_instance where word=%s and pid=%s and kind=%s)",
               [dist[word], word, post_id, kind, word, post_id, kind])

   def add (self, post):
      post_wilson = self.wilson(post.ups, post.downs)

      self.cur.execute("insert into post values (%s, %s, %s, %s);", [post.id, post.title, post.url, post.created])

      dist = self.build_dist(post.title, post_wilson)
      self.insert_dist(dist, post.id, TITLE)

      if post.is_self:
         is_self = true
         dist = self.build_dist(post.self, post_wilson)
         self.insert_dist(dist, post.id, SELF)

      for idx in range(len(post.comments) - 1):
         comment_wilson = self.wilson(post.comments[idx].ups, post.comments[idx].downs)
         dist = self.build_dist(post.comments[idx].body, comment_wilson)
         self.insert_dist(dist, post.id, COMMENT)

      self.conn.commit()

   def oldest (self):
      self.cur.execute("select post_time from post where post_time = (select max(post_time) from post);")
      res = self.cur.fetchone()[0]
      cur_time = time.time() - 86400
      
      if res > cur_time:
         start = cur_time
      else:
         start = res

      self.cur.execute("select id from post where post_time >= %s order by post_time desc limit 1;", [start])

      return self.cur.fetchone()[0]
