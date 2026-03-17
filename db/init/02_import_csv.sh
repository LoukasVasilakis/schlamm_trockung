#!/bin/bash
set -e

CSV_DIR="/import_data"

[ -d "$CSV_DIR" ] || exit 0

find "$CSV_DIR" -name "*.csv" -print0 | while IFS= read -r -d '' f; do
    echo "Importiere $f..."
    
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
        CREATE TEMP TABLE tmp AS SELECT * FROM events WITH NO DATA;
        ALTER TABLE tmp ALTER COLUMN "Datum" TYPE TEXT, ALTER COLUMN "Prio" TYPE TEXT, ALTER COLUMN "evtID" TYPE TEXT;

        COPY tmp FROM '$f' WITH (FORMAT csv, HEADER true, DELIMITER ';', ENCODING 'LATIN1');

        INSERT INTO events ("Datum", "Prio", "Msr", "Ort", "Objekt", "Meldung", "Zustand", "Benutzer", "evtID", "evtTyp")
        SELECT 
            TO_TIMESTAMP(regexp_replace("Datum", ':(\d{3})$', '.\1'), 'DD.MM.YY HH24:MI:SS.MS'),
            NULLIF("Prio", '')::INTEGER, "Msr", "Ort", "Objekt", "Meldung", "Zustand", "Benutzer", 
            NULLIF("evtID", '')::INTEGER, "evtTyp"
        FROM tmp;
	DROP TABLE tmp;
EOSQL
done
