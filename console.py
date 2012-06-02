import psycopg2
import dj_database_url

db = dj_database_url.config()
conn = psycopg2.connect(database=db.get('NAME', 'redditsearch'), user=db.get('USER', 'andrew'), password=db.get('PASSWORD', 'password'), host=db.get('HOST', 'localhost'))

cur = conn.cursor()
user = db.get('USER', 'andrew')
database = db.get('NAME', 'redditsearch')

result = []

while True:
   command = raw_input(user + "/" + database + ": ")
   if command == "quit":
      break

   try:
      cur.execute(command)
      result = cur.fetchall()
   except psycopg2.ProgrammingError:
      print("Malformed query")

   for row in result:
      print(row)
