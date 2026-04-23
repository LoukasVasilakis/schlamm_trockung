import os

import psycopg2

from utils.db_interaction import EventDataSource

host = "db" if os.getenv("GITLAB_CI") else "localhost"

conn = psycopg2.connect(
    dbname="pro2d_db", user="postgres", password="postgres", host=host, port="5432"
)

db = EventDataSource(conn)

# Alle Events aus der Datenbank abrufen
all_events = db.get_all_events()

# Alle Login/Logout-Events abrufen
events_login_logout = db.get_events_by_type(["Login/Logout"])

# Alle Events mit zusätzlichen Zeitfeldern für die Analyse abrufen
events_time_analysis = db.get_time_analysis_data()

# Alle Events von Vincenzo und Roland abrufen
user_events = db.get_events_by_user(["Vincenzo Signorelli", "Ronald Reinle"])

# Alle Event mit MSR 1, 2, 5 und 8 abrufen
msr_events = db.filter_events(column_to_filter="Msr", values=["1", "2", "5", "8"])

# Alle Events von Vincenzo und Roland mit MSR 1, 2, 5 und 8 abrufen
user_msr_events = db.filter_events(
    column_to_filter="Msr", values=["1", "2", "5", "8"], df=user_events
)

# Zusätzliche Zeitfelder zu den Events von Vincenzo und Roland mit MSR 1, 2, 5 und 8 hinzufügen
user_msr_events_time_analysis = db.get_time_analysis_data(user_msr_events)
