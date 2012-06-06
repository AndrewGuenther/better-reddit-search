import sys
from flask import Flask, request, render_template
import psycopg2
import dj_database_url
from helpers import mysearch, redditsearch

app = Flask(__name__)
app.config.from_object(__name__)

@app.route("/")
def hello():
   return render_template('index.html')

@app.route("/feedback")
def feedback():
   direction = int(request.args['dir'])
   who = int(request.args['who'])
   id = int(request.args['id'])

   conn = connect_db()
   cur = conn.cursor()

   if direction == 1 and who == 0:
     cur.execute("update search set reddit_relevant = reddit_relevant + 1 where id = %s", [id])
   elif direction == 0 and who == 0:
      cur.execute("update search set reddit_irrelevant = reddit_irrelevant + 1 where id = %s", [id])
   elif direction == 1 and who == 1:
      cur.execute("update search set mine_relevant = mine_relevant + 1 where id = %s", [id])
   elif direction == 0 and who == 1:
      cur.execute("update search set mine_irrelevant = mine_irrelevant + 1 where id = %s", [id])

   conn.commit()

   return 'OK'

@app.route("/s")
def search():
   query = request.args['q']
   
   conn = connect_db()
   cur = conn.cursor()

   myresult = mysearch(query, cur)
   redditresult = redditsearch(query, cur)

   cur.execute("insert into search (query, num_results_reddit, num_results_mine) values (%s, %s, %s) returning id;", [query, len(redditresult), len(myresult)])
   searchid = cur.fetchone()[0]
   conn.commit()

   return render_template('result.html', result1=redditresult, result2=myresult, searchid=searchid) 


def connect_db():
   db = dj_database_url.config()
   return psycopg2.connect(database=db.get('NAME', 'redditsearch2'), user=db.get('USER', 'andrew'), password=db.get('PASSWORD', 'password'), host=db.get('HOST', 'localhost'))

if __name__ == "__main__":
    app.run(debug=True, port=int(sys.argv[1]), host='0.0.0.0')
