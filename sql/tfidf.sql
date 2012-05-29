CREATE OR REPLACE FUNCTION idf(text) RETURNS numeric
    AS 'select log(2.0, ((select count(*) from post) / (select df from word where word=$1))::numeric);'
    LANGUAGE SQL
    IMMUTABLE;

CREATE OR REPLACE FUNCTION tfidf(text, text, integer) RETURNS float
    AS 'select ((select freq from word_instance where word=$1 and pid=$2 and kind=$3) / (select max(freq) from word_instance where pid=$2 and kind=$3) * idf($1));'
    LANGUAGE SQL
    IMMUTABLE;

CREATE OR REPLACE FUNCTION sim(text, text[], integer) RETURNS float 
   AS 'select coalesce((((select sum(tfidf(word, $1, $3) * idf(word)) from word where word = any ($2))) / |/((select sum(tfidf(word, $1, $3) ^ 2.0) from word where word = any ($2)) * (select sum(idf(word) ^ 2.0) from word where word = any ($2)))), 0.0);'
   LANGUAGE SQL
   IMMUTABLE;

CREATE OR REPLACE FUNCTION search(text[], integer) RETURNS table(id char(5), title varchar(300), rank float)
   AS 'select id, title, ((1.5 * sim(id, $1, 0)) + (1.25 * sim(id, $1, 1)) + sim(id, $1, 2)) as rank from post order by rank desc limit $2;'
   LANGUAGE SQL
   IMMUTABLE;
