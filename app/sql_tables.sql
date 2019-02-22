CREATE TABLE IF NOT EXISTS blacklist (
    tokens character varying(200) NOT NULL
);


CREATE TABLE IF NOT EXISTS users (
    first_name character varying(50) NOT NULL,
    last_name character varying(50),
    id_num numeric (10) PRIMARY KEY NOT NULL,
    role character varying(50) DEFAULT ('Normal'),
    date_created timestamp with time zone DEFAULT ('now'::text)::date NOT NULL,
    password character varying(500) NOT NULL,
    address character varying(50),
    tell character varying(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS incidents (
    incident_id serial PRIMARY KEY NOT NULL,
    created_by character varying(20) NOT NULL,
    type character varying(20)  NOT NULL,
    description character varying(200) NOT NULL,
    status character varying(50) DEFAULT 0,
    location character varying(200) NULL,
    created_on timestamp with time zone DEFAULT ('now'::text)::date NOT NULL
 );

CREATE TABLE IF NOT EXISTS records (
    record_id serial PRIMARY KEY NOT NULL,
    created_by character varying(20) NOT NULL,
    id_num numeric (10) NOT NULL,
    persona character varying(20)  NOT NULL,
    description character varying(200) NOT NULL,
    tell character varying(50) DEFAULT 0,
    hospital_attended character varying(200) NULL,
    created_on timestamp with time zone DEFAULT ('now'::text)::date NOT NULL
 );


CREATE TABLE IF NOT EXISTS comments (
    comment_id serial PRIMARY KEY NOT NULL,
    incident_id numeric NOT NULL,
    created_by character varying(20) NOT NULL,
    comment character varying(1000) NOT NULL,
    date_created timestamp with time zone DEFAULT ('now'::text)::date NOT NULL
);

CREATE TABLE IF NOT EXISTS sms (
    sms_id serial PRIMARY KEY NOT NULL,
    sms_details character varying(20) NOT NULL,
    to_cell numeric (15) NOT NULL, 
    created_by character varying(20) NOT NULL,
    comment character varying(1000) NOT NULL,
    date_created timestamp with time zone DEFAULT ('now'::text)::date NOT NULL
);




