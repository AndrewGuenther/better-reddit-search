create table text_block (
   thing_id varchar(7),

   primary key(thing_id)
);

create table word (
   string varchar(20),
   freq int,

   text_of varchar(7) references text_block(thing_id),

   primary key(string, text_of)
);

create table post (
   thing_id varchar(7) references text_block(thing_id),
   title text,
   link text,

   ups int,
   downs int,
   wilson real,

   primary key(thing_id)
);

create table comment (
   thing_id varchar(7) references text_block(thing_id),
   parent varchar(7) references text_block(thing_id),

   primary key(thing_id)
);

create table search (
   id serial,
   query text,
   num_results_reddit int default 0,
   num_results_mine int default 0,
   reddit_relevant int default 0,
   mine_relevant int default 0,
   reddit_irrelevant int default 0,
   mine_irrelevant int default 0,

   primary key(id)
);
