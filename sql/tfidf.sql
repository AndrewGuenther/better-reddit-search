CREATE OR REPLACE FUNCTION idf(integer) RETURNS numeric
    AS 'select coalesce(log(2.0, ((select count(*) from text_block)::numeric / nullif((select count(*) from word where string = (select string from word where id = $1))::numeric, 0.0))), 0.0);'
    LANGUAGE SQL
    IMMUTABLE;

CREATE OR REPLACE FUNCTION tfidf(word_id integer, text_of integer) RETURNS numeric 
    AS 'select ((select freq from word where id=$1)::numeric / (select max(freq) from word where text_of=$2) * idf($1));'
    LANGUAGE SQL
    IMMUTABLE;

CREATE OR REPLACE FUNCTION sim(doc integer, query text[]) RETURNS float
   AS 'select coalesce(((select sum(tfidf(id, $1) * idf(id)) from word where text_of = $1 and string = any ($2))::numeric / |/((select sum(tfidf(id, $1) ^ 2.0) from word where text_of = $1) * (select distinct sum(idf(id) ^ 2.0) from word where string = any ($2)))), 0.0);'
   LANGUAGE SQL
   IMMUTABLE;

CREATE OR REPLACE FUNCTION comment_sim(doc integer, query text[]) RETURNS float
   AS 'select coalesce(((select sum(tfidf(id, $1) * idf(id)) from word natural join text_block where parent = $1 and string = any ($2))::numeric / |/nullif(((select sum(tfidf(id, $1) ^ 2.0) from word natural join text_block where parent = $1) * (select sum(idf(id) ^ 2.0) from word where string = any ($2))), 0.0)), 0.0);'
   LANGUAGE SQL
   IMMUTABLE;

CREATE OR REPLACE FUNCTION search(query text[], most integer) RETURNS table(id char(5), title varchar(300), link text, rank float)
   AS 'select thing_id, title, link, wilson * (1.5 * sim(id, $1) + comment_sim(id, $1)) as rank from post natural join text_block where id = any (select text_of from word where string = any ($1)) or id = any (select parent from word natural join text_block where string = any($1)) order by rank desc limit $2;'
   LANGUAGE SQL
   IMMUTABLE;
