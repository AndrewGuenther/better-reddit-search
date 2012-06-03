CREATE OR REPLACE FUNCTION wilson(integer, integer) RETURNS numeric
    AS 'select coalesce((($1 + 1.9208) / ($1 + $2) - 1.96 * SQRT(($1 * $2) / ($1 + $2) + 0.9604) / ($1 + $2)) / (1 + 3.8416 / ($1 + $2)), 0.0);'
    LANGUAGE SQL
    IMMUTABLE;

CREATE OR REPLACE FUNCTION idf(text, integer) RETURNS numeric
    AS 'select log(2.0, ((select count(*) from post) / (select count(*) from word_instance where word=$1 and kind=$2))::numeric);'
    LANGUAGE SQL
    IMMUTABLE;

CREATE OR REPLACE FUNCTION tfidf(text, text, integer) RETURNS float
    AS 'select ((select freq from word_instance where word=$1 and pid=$2 and kind=$3) / (select max(freq) from word_instance where pid=$2 and kind=$3) * idf($1, $3));'
    LANGUAGE SQL
    IMMUTABLE;

CREATE OR REPLACE FUNCTION sim(text, text[], integer) RETURNS float 
   AS 'select coalesce((((select sum(tfidf(word, $1, $3) * idf(word, $3)) from word_instance where kind = $3 and pid = $1 and word = any ($2))) / |/((select sum(tfidf(word, $1, $3) ^ 2.0) from word_instance where kind = $3 and pid = $1) * (select sum(idf(word, $3) ^ 2.0) from word_instance where kind = $3 and word = any ($2)))), 0.0);'
   LANGUAGE SQL
   IMMUTABLE;

CREATE OR REPLACE FUNCTION search(text[], integer) RETURNS table(id char(5), title varchar(300), link text, rank float)
   AS 'select id, title, link, wilson(ups, downs) * ((1.5 * sim(id, $1, 0)) + (1.25 * sim(id, $1, 1)) + sim(id, $1, 2)) as rank from post order by rank desc limit $2;'
   LANGUAGE SQL
   IMMUTABLE;
