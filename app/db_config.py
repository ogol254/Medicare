from flask import current_app
from contextlib import closing
import psycopg2
import os


def connection(url):
    con = psycopg2.connect(url)
    return con


def init_db():
    """Set up the database to stode the user data
    """
    db_url = current_app.config['DATABASE_URL']
    conn = connection(db_url)
    with conn as conn, conn.cursor() as cursor:
        with current_app.open_resource('sql_tables.sql', mode='r') as sql:
            cursor.execute(sql.read())
        conn.commit()
        return conn


def init_test_db():
    conn = connection(os.getenv('DATABASE_TEST_URL'))
    destroy_db()
    with conn as conn, conn.cursor() as cursor:
        with current_app.open_resource('sql_tables.sql', mode='r') as sql:
            cursor.execute(sql.read())
        conn.commit()
        return conn


def destroy_db():
    conn = connection(os.getenv('DATABASE_TEST_URL'))
    curr = conn.cursor()
    blacklist = """DROP TABLE IF EXISTS blacklist CASCADE; """
    users = """DROP TABLE IF EXISTS users CASCADE; """
    incidents = """DROP TABLE IF EXISTS incidents CASCADE; """
    comments = """DROP TABLE IF EXISTS comments CASCADE; """
    records = """DROP TABLE IF EXISTS records CASCADE; """
    facilities = """DROP TABLE IF EXISTS facilities CASCADE; """
    queries = [blacklist, users, incidents, comments, records, facilities]
    try:
        for query in queries:
            curr.execute(query)
        conn.commit()
    except:
        print("Fail")


# INSERT INTO users (first_name, last_name, id_num, role, password, address, tell) VALUES
#('Admin', 'Admin', '123456789', 'admin', 'pbkdf2:sha256:50000$0UJC97AT$4767261ce2cf04ce16128bc8a75eb4a7f04aa413936e9253309fc7d705a32a4a', 'ADMIN_address', '790463533');
