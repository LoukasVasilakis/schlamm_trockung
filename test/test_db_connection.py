import os

import psycopg2


def test_db_connection():
    host = "db" if os.getenv("GITLAB_CI") else "localhost"
    conn = psycopg2.connect(
        dbname="pro2d_db", user="postgres", password="postgres", host=host, port="5432"
    )

    cur = conn.cursor()

    cur.execute("SELECT * FROM events LIMIT 25")
    events = cur.fetchall()
    for event in events:
        print(event)

    cur.close()
    conn.close()
    assert len(events) == 25
