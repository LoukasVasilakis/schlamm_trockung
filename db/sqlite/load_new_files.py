import csv
import os
import sqlite3
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_FILE = BASE_DIR / "events.sqlite"
# Assuming there's an 'import' directory in db/sqlite or elsewhere.
# Let's make it configurable via environment or default to a local 'import' folder.
FILE_DIR = Path(os.getenv("IMPORT_DATA_PATH", str(BASE_DIR / "import")))


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
    if not FILE_DIR.exists():
        print(f"Ordner nicht gefunden: {FILE_DIR}")
        return

    csv_files = sorted(FILE_DIR.rglob("*.csv"))

    if not csv_files:
        print(f"Keine neuen CSV-Dateien gefunden in: {FILE_DIR}")
        return

    with sqlite3.connect(DB_FILE) as connection:
        for csv_file in csv_files:
            try:
                import_csv_file(connection, csv_file)
                os.remove(csv_file)
            except Exception as e:
                print(f"Fehler beim Importieren oder Löschen von {csv_file}: {e}")
                continue
            else:
                connection.commit()

    print(f"Import abgeschlossen. {len(csv_files)} Dateien verarbeitet.")


if __name__ == "__main__":
    main()
