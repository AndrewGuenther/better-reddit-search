create table text_block (
   id serial,
   thing_id varchar(7),
   ups int,
   downs int,
   wilson real,

   parent int references text_block(id),

   primary key(id)
);

create table word (
   id serial,
   string varchar(20),
   freq int,

   text_of int references text_block(id),

   primary key(id)
);

create table post (
   id int references text_block(id),
   title text,
   link text,

   primary key(id)
);

create table comment (
   id int references text_block(id),
   parent int references text_block(id),

   primary key(id)
);

create table search (
   id serial,
   num_results_reddit int,
   num_results_mine int,
   reddit_relevant int,
   mine_relevant int,
   reddit_irrelevant int,
   mine_irrelevant int,

   primary key(id)
);
