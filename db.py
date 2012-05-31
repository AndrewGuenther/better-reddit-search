import psycopg2
import dj_database_url

db = dj_database_url.config()
cur = psycopg2.connect(database=db.get('NAME', 'redditsearch'), user=db.get('USER', 'andrew'), password=db.get('PASSWORD', 'password'), host=db.get('HOST', 'localhost')).cursor()

cur.execute("create table post (\
   id char(5),\
   title varchar(300),\
   link text,\
   post_time numeric(11, 1),\
   ups integer,\
   downs integer,\
\
   primary key(id)\
);\
")

cur.execute("create table word (\
   word varchar(20) primary key,\
   df real\
);\
")

cur.execute("create table word_instance (\
   freq real,\
\
   word varchar(20) references word(word),\
   pid char(5) references post(id),\
   kind int not null,\
\
   primary key(word, pid, kind)\
);")


