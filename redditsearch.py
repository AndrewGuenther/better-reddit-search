from flask import Flask, request
import psycopg2
from nltk import word_tokenize

DATABASE = 'redditsearch'
USERNAME = 'andrew'
PASSWORD = 'password'

app = Flask(__name__)
app.config.from_object(__name__)

@app.route("/")
def hello():
   return "Hello World!"

@app.route("/s")
def search():
   conn = connect_db()
   cur = conn.cursor()

   query = request.args['q']

   cur.execute('select title from search(%s, %s) where rank > 0', [word_tokenize(query), 15])

   out = ""
   for result in cur.fetchall():
      out += '''%s<br>''' % result[0]

   return out


def connect_db():
   return psycopg2.connect(database=app.config['DATABASE'], user=app.config['USERNAME'], password=app.config['PASSWORD'])

if __name__ == "__main__":
    app.run(debug=True)
