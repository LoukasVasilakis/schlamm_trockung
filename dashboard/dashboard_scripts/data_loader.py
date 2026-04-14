import pandas as pd
import psycopg2

# Dataset

def load_data():
    # Establish a connection to the PostgreSQL database
    conn = psycopg2.connect(
        dbname="pro2d_db",  # dbname: name of the database
        user="postgres", # user/password: login credentials
        password="postgres",
        host="localhost", # host: where the database server is running (localhost = this machine)
        port="5432" # port: default PostgreSQL port
    )

    df = pd.read_sql('SELECT "Datum", "Meldung", "evtTyp", "Prio", "Benutzer" FROM events',conn) # Dataframe erstellen

    conn.close() # Close the database connection, avoid open connections (resource leaks)

    # Prepare dates
    df["Datum"] = pd.to_datetime(df["Datum"], errors="coerce") # Feature Datum in panda datatime konvertieren
    df = df.sort_values("Datum") # korrekte Reihenfolge sichern

    # Fix typo in user name
    df["Benutzer"] = df["Benutzer"].replace(
        "Vinzenzo Signorelli",
        "Vincenzo Signorelli"
    )

    # Clean data for dashboard
    df = df.dropna(subset=["Datum"]).copy()
    df["Meldung"] = df["Meldung"].fillna("").astype(str)

    dates = pd.to_datetime(
        df["Datum"].dropna().sort_values().dt.normalize().unique() # Eindeutige Datumswerte ohne Uhrzeit für Slider und Kalender
    )


    return df, dates


df, dates = load_data()