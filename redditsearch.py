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

@app.route("/s")
def search():
   query = request.args['q']
   
   conn = connect_db()
   cur = conn.cursor()
   myresult = mysearch(query, cur)

   redditresult = redditsearch(query, cur)

   return render_template('result.html', result1=redditresult, result2=myresult) 


def connect_db():
   db = dj_database_url.config()
   return psycopg2.connect(database=db.get('NAME', 'redditsearch'), user=db.get('USER', 'andrew'), password=db.get('PASSWORD', 'password') host=db.get('HOST', 'localhost'))

if __name__ == "__main__":
    app.run(debug=True, port=int(sys.argv[1]), host='0.0.0.0')
