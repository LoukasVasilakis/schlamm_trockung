import psycopg2

def test_db_connection():
    conn = psycopg2.connect(
        dbname="pro2d_db", user="postgres", password="postgres", host="localhost", port="5432"
    )
    
    cur = conn.cursor()

    cur.execute("SELECT * FROM events LIMIT 5")
    events = cur.fetchall()
    for event in events:
        print(event)
    
    cur.close()
    conn.close()
    assert True