create table post (
   id char(5),
   title varchar(300),
   link text,
   post_time timestamp,

   primary key(id)
);

create table word (
   word varchar(20) primary key,
   df real
);


--kind = {0: "title", 1: "self", 2: "comment"}
create table word_instance (
   freq real,

   word varchar(20) references word(word),
   pid char(5) references post(id),
   kind int not null,

   primary key(word, pid, kind)
);
