CREATE OR REPLACE FUNCTION idf(varchar(20)) RETURNS numeric
    AS 'select coalesce(log(2.0, ((select count(*) from text_block)::numeric / nullif((select count(*) from word where string = $1)::numeric, 0.0))), 0.0);'
    LANGUAGE SQL
    IMMUTABLE;

CREATE OR REPLACE FUNCTION tfidf(word_id varchar(20), text_of varchar(7)) RETURNS numeric 
    AS 'select ((select freq from word where string = $1 and text_of = $2)::numeric / (select max(freq) from word where text_of=$2) * idf($1));'
    LANGUAGE SQL
    IMMUTABLE;

CREATE OR REPLACE FUNCTION sim(doc varchar(7), query text[]) RETURNS float
   AS 'select coalesce(((select sum(tfidf(string, $1) * idf(string)) from word where text_of = $1 and string = any ($2))::numeric / |/((select sum(tfidf(string, $1) ^ 2.0) from word where text_of = $1) * (select distinct sum(idf(string) ^ 2.0) from word where string = any ($2)))), 0.0);'
   LANGUAGE SQL
   IMMUTABLE;

CREATE OR REPLACE FUNCTION comment_sim(doc varchar(7), query text[]) RETURNS float
   AS 'select coalesce(((select sum(tfidf(string, $1) * idf(string)) from word inner join comment on word.text_of = comment.thing_id where parent = $1 and string = any ($2))::numeric / |/nullif(((select sum(tfidf(string, $1) ^ 2.0) from word inner join comment on word.text_of = comment.thing_id where parent = $1) * (select sum(idf(string) ^ 2.0) from word where string = any ($2))), 0.0)), 0.0);'
   LANGUAGE SQL
   IMMUTABLE;

CREATE OR REPLACE FUNCTION search(query text[], most integer) RETURNS table(id char(5), title varchar(300), link text, rank float)
   AS 'select thing_id, title, link, wilson * (1.5 * sim(thing_id, $1) + comment_sim(thing_id, $1)) as rank from post natural join text_block where thing_id = any (select text_of from word where string = any ($1)) or thing_id = any (select parent from word inner join comment on word.text_of = comment.thing_id where string = any($1)) order by rank desc limit $2;'
   LANGUAGE SQL
   IMMUTABLE;
