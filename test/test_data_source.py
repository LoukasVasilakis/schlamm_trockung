import os

import psycopg2
import pytest

from utils.db_interaction import EventDataSource


@pytest.fixture
def connection():
    host = "db" if os.getenv("GITLAB_CI") else "localhost"

    conn = psycopg2.connect(
        dbname="pro2d_db", user="postgres", password="postgres", host=host, port="5432"
    )

    yield conn
    conn.close()


@pytest.fixture
def data_source(connection):
    return EventDataSource(connection)


def test_data_source(data_source: EventDataSource):
    events = data_source.get_all_events()

    assert events is not None
