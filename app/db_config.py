from flask import current_app
import psycopg2


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
    conn = connection(current_app.config['DATABASE_TEST_URL'])
    destroy_db()
    with conn as conn, conn.cursor() as cursor:
        with current_app.open_resource('sql_tables.sql', mode='r') as sql:
            cursor.execute(sql.read())

        conn.commit()
        return conn


def destroy_db():
    test_url = current_app.config['DATABASE_TEST_URL']
    conn = connection(test_url)
    curr = conn.cursor()
    blacklist = "DROP TABLE IF EXISTS blacklist CASCADE"
    users = "DROP TABLE IF EXISTS users CASCADE"
    queries = [blacklist, users]
    try:
        for query in queries:
            curr.execute(query)
        conn.commit()
    except:
        print("Fail")
