import nltk
import dj_database_url
import reddit
import psycopg2
import time
from math import sqrt
from string import lower
from consts import TITLE, SELF, COMMENT

class DocCollection:

   def __init__ (self):
      db = dj_database_url.config()
      self.conn = psycopg2.connect(database=db.get('NAME', 'redditsearch2'), user=db.get('USER', 'andrew'), password=db.get('PASSWORD', 'password'), host=db.get('HOST', 'localhost'))
      self.conn.autocommit = False
      self.cur = self.conn.cursor()     

   def wilson (self, ups, downs):
      n = ups + downs
      z = 1.6 #1.0 = 85%, 1.6 = 95%
   
      if n > 0:
         phat = float(ups) / n
      else:
         return 0

      return sqrt(phat+z*z/(2*n)-z*((phat*(1-phat)+z*z/(4*n))/n))/(1+z*z/n)
     

   def build_dist (self, body, wilson):
      stemmer = nltk.stem.porter.PorterStemmer()

      stopwords = [x.strip() for x in open("stopwords.txt", "r").readlines()]
      clean = [w.lower() for w in nltk.word_tokenize(body) if not w.lower() in stopwords]
      
      stems = []
      for word in clean:
         if len(word) < 20:
            stems.append(stemmer.stem(lower(word)))

      freqs = nltk.probability.FreqDist(stems)

      for key in freqs:
         if freqs[key] > 0:
            freqs[key] = freqs[key] #*= wilson
         else:
            del(freqs[key])
      
      return freqs

   def insert_dist (self, dist, parent_id):
      for word in dist:
         if dist[word] > 0:
#            print("test")
            self.cur.execute("insert into word (string, freq, text_of) values (%s, %s, %s);",
               [word, dist[word], parent_id])

   def add (self, post):
      post_wilson = self.wilson(post.ups, post.downs)

      self.cur.execute("select count(*) from post where thing_id=%s;", [post.id])
      if self.cur.fetchone()[0] == 1:
         self.cur.execute("update post set ups=%s, downs=%s, wilson=%s where thing_id=%s;", [post.ups, post.downs, post_wilson, post.id])
      else:
         self.cur.execute("insert into text_block values (%s);", [post.id]);
         self.cur.execute("insert into post values (%s, %s, %s, %s, %s, %s);", [post.id, post.title, post.url, post.ups, post.downs, post_wilson])

         dist = self.build_dist(post.title, post_wilson)
         self.insert_dist(dist, post.id)

      comment_text = ""
      comment_wilson = 0
      for idx in range(len(post.comments) - 1):
         comment = post.comments[idx]
         comment_wilson = self.wilson(comment.ups, comment.downs)

         comment_text += " " + comment.body

      self.cur.execute("delete from word where text_of = %s", [post.id + "c"])
      self.cur.execute("delete from comment where thing_id = %s", [post.id + "c"])
      self.cur.execute("delete from text_block where thing_id = %s", [post.id + "c"])

      self.cur.execute("insert into text_block values (%s);", [post.id + "c"])
      self.cur.execute("insert into comment values (%s, %s);", [post.id + "c", post.id])      

      dist = self.build_dist(comment_text, comment_wilson)
      self.insert_dist(dist, post.id + "c")
      
      self.conn.commit()
