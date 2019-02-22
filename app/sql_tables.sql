CREATE TABLE IF NOT EXISTS blacklist (
    tokens character varying(200) NOT NULL
);


CREATE TABLE IF NOT EXISTS users (
    first_name character varying(50) NOT NULL,
    last_name character varying(50),
    id_num character varying(50) PRIMARY KEY NOT NULL,
    user_type character varying(50) DEFAULT ("Normal"),
    date_created timestamp with time zone DEFAULT ('now'::text)::date NOT NULL,
    password character varying(500) NOT NULL,
    address character varying(50),
    tell character varying(50) NOT NULL,
    
);