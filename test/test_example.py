import os

import psycopg2
import pytest

import utils.db_interaction as dbi


@pytest.fixture
def cursor():
    host = "db" if os.getenv("GITLAB_CI") else "localhost"
    conn = psycopg2.connect(
        dbname="pro2d_db", user="postgres", password="postgres", host=host, port="5432"
    )
    cur = conn.cursor()
    yield cur
    cur.close()
    conn.close()


def test_example(cursor):
    events = dbi.select_something(cursor)
    assert len(events) == 150
