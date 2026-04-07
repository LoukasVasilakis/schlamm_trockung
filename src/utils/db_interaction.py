from psycopg2.extensions import cursor


def select_something(cur: cursor):
    cur.execute("SELECT * FROM events LIMIT 150")
    events = cur.fetchall()
    return events
