import sqlite3
from pathlib import Path


def test_db_connection():
    db_path = Path(__file__).resolve().parent.parent / "db" / "sqlite" / "events.sqlite"
    conn = sqlite3.connect(db_path)

    cur = conn.cursor()

    cur.execute("SELECT * FROM events LIMIT 25")
    events = cur.fetchall()
    for event in events:
        print(event)

    cur.close()
    conn.close()
    assert len(events) == 25
