import csv
import sqlite3
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DB_FILE = BASE_DIR / "events.sqlite"
CSV_DIR = Path(
    "C:/Users/janis/OneDrive - FHNW/"
    "P-pro2Db_Ausfälle-in-Schlammtrockungsanlage_M365 - STRAG AG/"
    "Data/Logger"
)


CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS events (
    "Datum" TEXT,
    "Prio" INTEGER,
    "Msr" TEXT,
    "Ort" TEXT,
    "Objekt" TEXT,
    "Meldung" TEXT,
    "Zustand" TEXT,
    "Benutzer" TEXT,
    "evtID" INTEGER,
    "evtTyp" TEXT
);
"""


def parse_datum(value: str):
    if value is None or value.strip() == "":
        return None

    value = value.strip()

    if value.count(":") >= 3:
        left, right = value.rsplit(":", 1)
        value = left + "." + right

    dt = datetime.strptime(value, "%d.%m.%y %H:%M:%S.%f")
    return dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]


def to_int_or_none(value: str):
    if value is None or value.strip() == "":
        return None

    return int(value)


def init_database(connection):
    connection.execute(CREATE_TABLE_SQL)


def import_csv_file(connection, csv_file: Path):
    print(f"Importiere {csv_file}...")

    insert_sql = """
        INSERT INTO events (
            "Datum",
            "Prio",
            "Msr",
            "Ort",
            "Objekt",
            "Meldung",
            "Zustand",
            "Benutzer",
            "evtID",
            "evtTyp"
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """

    rows_to_insert = []

    with csv_file.open("r", encoding="latin-1", newline="") as file:
        reader = csv.DictReader(file, delimiter=";")

        for row in reader:
            rows_to_insert.append(
                (
                    parse_datum(row.get("Datum")),
                    to_int_or_none(row.get("Prio")),
                    row.get("Msr"),
                    row.get("Ort"),
                    row.get("Objekt"),
                    row.get("Meldung"),
                    row.get("Zustand"),
                    row.get("Benutzer"),
                    to_int_or_none(row.get("evtID")),
                    row.get("evtTyp"),
                )
            )

    connection.executemany(insert_sql, rows_to_insert)
    print(f"  {len(rows_to_insert)} Zeilen importiert.")


def main():
    if not CSV_DIR.exists():
        print(f"Ordner nicht gefunden: {CSV_DIR}")
        return

    csv_files = sorted(CSV_DIR.rglob("*.csv"))

    if not csv_files:
        print(f"Keine CSV-Dateien gefunden in: {CSV_DIR}")
        return

    with sqlite3.connect(DB_FILE) as connection:
        init_database(connection)

        for csv_file in csv_files:
            import_csv_file(connection, csv_file)

        connection.commit()

    print(f"Fertig. Datenbank: {DB_FILE}")


if __name__ == "__main__":
    main()
