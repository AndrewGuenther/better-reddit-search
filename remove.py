import psycopg2
import dj_database_url

db = dj_database_url.config()
conn = psycopg2.connect(database=db.get('NAME', 'redditsearch'), user=db.get('USER', 'andrew'), password=db.get('PASSWORD', 'password'), host=db.get('HOST', 'localhost'))
cur = conn.cursor()

stopwords = [x.strip() for x in open("stopwords.txt", "r").readlines()]

for word in stopwords:
   cur.execute("delete from word where word = %s;", [word])
   cur.execute("delete from word_instance where word = %s;", [word])

conn.commit()
