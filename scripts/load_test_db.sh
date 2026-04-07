#!/usr/bin/env bash
set -euo pipefail

DB_HOST="${POSTGRES_HOST:-db}"
DB_PORT="${POSTGRES_PORT:-5432}"
DB_NAME="${POSTGRES_DB:-pro2d_db}"
DB_USER="${POSTGRES_USER:-postgres}"
CSV_DIR="test/data"

until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" >/dev/null 2>&1; do
  sleep 1
done

psql -v ON_ERROR_STOP=1 -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -f db/init/01_init.sql

find "$CSV_DIR" -name "*.csv" | sort | while IFS= read -r file; do
  echo "Importing $file"

  psql -v ON_ERROR_STOP=1 -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" <<SQL
CREATE TABLE IF NOT EXISTS events (
    "Datum" TIMESTAMP,
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

  DROP TABLE IF EXISTS tmp_events;
  CREATE TEMP TABLE temp_events AS SELECT * FROM events WITH NO DATA;

\copy tmp_events FROM '$file' WITH (FORMAT csv, HEADER true, DELIMITER ';', ENCODING 'LATIN1');

INSERT INTO events ("Datum", "Prio", "Msr", "Ort", "Objekt", "Meldung", "Zustand", "Benutzer", "evtID", "evtTyp")
SELECT
  TO_TIMESTAMP(regexp_replace("Datum", ':(\d{3})$', '.\1'), 'DD.MM.YY HH24:MI:SS.MS'),
  NULLIF("Prio", '')::INTEGER,
  "Msr",
  "Ort",
  "Objekt",
  "Meldung",
  "Zustand",
  "Benutzer",
  NULLIF("evtID", '')::INTEGER,
  "evtTyp"
FROM tmp_events;
SQL
done