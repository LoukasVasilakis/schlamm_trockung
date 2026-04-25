# PRO2D - Ausfälle in Schlammtrocknungsanlage verhindern

Dieses Repository beinhaltet alle Dateien bezüglich des Projekts PRO2D.

## Projektinformation
### Projektrollen
PO: Florin
Deputy PO: Janis
Aufgabe: Issues anschauen und verwalten, bei Unklarheiten eine Überarbeitung in Auftrag geben, Priorisierung für die Sprints gestalten.

Scrum-Master: Melanie
Deputy Scrum-Muster: Harman
Aufgabe: Leitung der Meetings, Time-Management, "ordentliche" Meetings (alle können sprechen, Core-Values werden eingehalten)

Developers: Alessandro Gregori, Loukas Vasilakis

Kunde: STRAG (**S**chlamm**Tr**ocknungs**AG**)
Vertreter: Daniel Wymann

### Kontakt 
Daniel daniel.wymann@stragara.ch:
- Grundsätzlich während der Ganzen Woche erreichbar
Reto reto.balz@stragara.ch:
- Vorzugsweise Mittwochs verfügbar
- Besser per Teams als per Telefon erreichbar.

### Daten
- "PLS (Prozessleitsystem)".
- Täglich werden CSVs generiert
- Events wie z.B:
	- wer hat sich eingeloggt
	- ... bis zu
	- schlimmste Störung jemals
    
| Attribut   | Typ    | Wichtigkeit | Beschreibung                                 |
| ---------- | ------ | ----------- | -------------------------------------------- |
| Datum/Zeit | `Date` | 5           |                                              |
| Priorität  |        | 5           | Null, 0,1,2,3                                |
| MSR Nr.    |        | 3           | Sensor Nummer / Exception aus einem Programm |
| Ort        |        | 2           |                                              |
| Objekt     |        | 4           |                                              |
| Meldung    |        | 5           |                                              |
| Zustand    |        | 3           |                                              |
| Benutzer   |        | 5           | Login-Events können nachverfolgt werden      |
| evtID      |        | 0           | Id                                           |
| evtTyp     |        | 5           | "Login","Logout","Störung"                   |

---

## Praxiswissen

### Trocknungsprozess
*Trockensubstanz (TS)* = Anteil an Wasser/Getrocknetem Schlamm

0% *TS* = Nur Wasser
100% *TS* = Staubtrocken

- Getrocknet kann der Schlamm als Brennstoff verwendet werden. (Wird anschliessend an Holcim geliefert.)
- Läuft fast 365 Tage im Jahr (2-3 Wochen deaktiviert für Improvements)
- Läuft seit mehr als 10 Jahren (für uns relevante Daten sind 2024 - 2025)
- Zum Teil **3-6 Monate** (!) stillgestanden (aufgrund von Teilen)
- Ein Trocknungsdurchgang dauert ungefähr 2h
- Es werden ungefähr 60 Tonnen Granulat (Pulver) pro Woche gewonnen

#### Ablauf der Trocknung
1. Startet beim Schlammbunker (30% TS)
2. Schlamm nach oben pumpen
3. Schlamm in vordefinierte Form (genannt "Matrize") eingefüllt
4. Schlamm wird durch die Matrize als "Spaghetti" auf ein Förderband verschoben
5. "Spaghettis" werden getrocknet (Wärme kommt von Holcim?)
6. Getrocknete Spaghettis werden zu Granulat gemacht
7. Granulatbunker
8. LKW wird mit Granulatpulver beladen

#### Teilsysteme:
##### Luftfilterung:
Ein Teil der Luft, die beim Trocknen benutzt wurde ist sehr Ammoniaklastig (verschmutzt). Luft wird in einem 3-Stufigen verfahren gewaschen.
Anschliessend in den Biofilter

##### Kühlung:
- "Recyceltes Wasser" Im Trockner entsteht heisse, feuchte Luft. Diese wird dann zum kondensieren gebracht
- Brauchwasser (13°) von Holcim

Die Anlage kann auch Nassschlamm (5% TS) annehmen. Damit aus der 5% - 30% TS-Schlamm wird, wird er mit Flockungsmitteln versehen und anschliessend gepresst.
Übrig bleibt der Schlamm und Trübwasser. Das Trübwasser kommt zurück zur ARA.

---

## Infrastruktur 

Meeting-Protokolle, Code-Dateien und andere Projekt-bezogene Dateien werden
alle in diesem Repository hinterlegt.

Für TODOs werden Issues erfasst. Jeder darf Issues erfassen, sich selbst Issues
zuweisen und andere Issues kommentieren.

Wichtige Projektfragen wurden im [Miro-Board](https://miro.com/app/board/uXjVG7--mE4=/?share_link_id=526173358274) notiert und geklärt.$

---

## AI Governance
### Ground-Rules
- Keine projektspezifischen und sensible Daten der KI füttern
- Test-Driven-Development für Qualitätssicherung (Unit Test wird geschrieben vor Coding, dann wird Code gezielt so erstellt solange bis der Test grün ist)
- evtl. "datenschutzfreundlichere" KI Anbieter nutzen (z.B. Claude)
- Neutrale Prompts, welche nicht auf das konkrete Projekt bzw. Domäne schliessen lassen
- **Qualitätssicherung**: Jeder KI-generierte Code muss reviewed werden.
- **Kennzeichnungspflicht**: Grössere KI Nutzung (Generierung von gesamten Funktionen oder Funktionalitäten) kennzeichnen
---
## Projektstruktur

    pro2db_ausfaelle_in_schlammtrocknungsanlage/
    │
    ├── meetings/                   # Notizen und Protokolle von Meetings
    │   ├── deepdive_09-03-2026.md
    │   ├── kickoff_24-02-26.md
    │   ├── kundenmeeting_02-03-26.md
    │   ├── retro.md
    │   ├── weekly.md
    │   └── planning_03-03-26.md
    │
    ├── db/
    │   ├── docker/
    │   │   └── docker-compose.yml
    │   └── init/
    │       ├── 01_init.sql
    │       └── 02_import_csv.sh
    │ 
    ├── notebooks/
    │
    ├── src/
    │
    ├── test/                       # Automatisierte Code-Überprüfung
    │   ├── test_db_connection.py
    │   └── test_example.py
    │
    ├── praesentationen/            # Präsentationsmaterial (Slides etc.)
    │
    ├── eda/                        # Explorative Datenanalyse
    │   ├── eda_documents/          # EDA Dokumentation
    │   │   └── Bericht_EDA_Schlammtrocknungsanlage_Sprint_1.pdf
    │   │
    │   └── eda_scripts/            # Package für alle eda scripts
    │       ├── __init__.py
    │       ├── error_analysis.py
    │       └── user_analysis.ipynb
    │
    │
    ├── dashboard/
    │   ├── dashboard_documents/     # Dashboard Dokumentation
    │   └── dashboard_scripts/       # Package für alle Dashboard scripts
    │       └── __init__.py
    │
    ├── Readme.md                    # Projektbeschreibung und Nutzung
    ├── .gitignore                   # Dateien die Git ignorieren soll
    ├── pyproject.toml               # Projekt- und Abhängkigkeitskonfiguration
    ├── requirements.txt             # Python-Abhängigkeitenliste
    ├── .gitlab-ci.yml               # CI/CD Pipeline Konfiguration
    ├── goal-driven-roadmap-and-releases.md
    ├── pre-commit-config.yaml       # Pre-Commit Prüfregeln
    └── uv.lock                      # Abhängigkeitsversionen sperren

## Branching Workflow
### Ground-Rules

- `main`: An `main` wird, nur überträgt (push) nach einem `Sprint-Review`
- `dev`: `issues`, die ihr `Review` bestanden haben werden auf `dev`übertragen
- `feature/<issue-thema>`: `issues` werden in ihrem eigenen `Branch` verarbeitet und dürfen nur nach `Review` an `dev` übertragen werden

### Hilfreiche git commands

1. Aktuellen Stand  in lokalen workspace holen.
   ```bash
   git checkout dev
   git pull origin dev
   ```
2. Feature-Branch erstellen.
   ```bash
   git checkout -b feature/<issue-thema>
   # z.B. git checkout -b feature/histogramm
   ```
3. Auf Stand halten.
   Wenn `dev` sich ändert:
   ```bash
   git checkout dev && git pull
   git checkout feature/<issue-thema>
   git merge dev    # oder: git rebase dev
   ```
4. Push & Merge Request öffnen.
   ```bash
   git push -u origin feature/<issue-thema>
   ```

5. Aufräumen:
   ```bash
   git branch -d feature/<issue-thema>
   git push origin --delete feature/<issue-thema>
   ```
6. Versionieren:
   ```bash
   git checkout main
   git pull origin main
   git tag <version-name> # z.B. v1.0
   git push origin <version-name>
   ```


7. Explorer:
Eine IDE wie PyCharm kann die Nutzung von Git stark vereinfachen und viele Befehle durch einfache Klicks ersetzen

---

## Development Standards
### Review & Merge Regel

- Wer das Review durchführt, soll anschliessend auch den Merge durchführen 
- Als Reviewer dürfen auch Kollegen, die am gleichen Issue arbeiten, zugewiesen werden
- Commit Message soll erklären was wurde gemacht / verändert und warum
- Wie in GitLab automatisch vorgesehen, soll der Source-Branch nach dem Merge gelöscht werden.
Ausser beim dev-Branch nach einem Merge in den main-Branch oder in speziellen Ausnahmefällen

### Best-Practice-Anweisungen (nicht obligatorisch, aber sehr empfohlen)

- Konstantes Repository-Layout behalten
- Eine revision per commit
- Regelmässige Pulls
- Push keinen fehlerhaften Code, ausser du arbeitest gerade aktiv daran und bittest einen Kollegen um Unterstützung
- Lieber zu viele Code comments als zu wenig
- Code löschen statt auskommentieren
- Niemals Änderungen im .git-Ordner vornehmen

---

## CI/CD pipeline

### uv.lock
Die Datei `uv.lock` wird vom Python-Paketmanager uv automatisch erzeugt und dient dazu, alle Projektabhängigkeiten exakt festzuhalten.

**Zweck**
    
`uv.lock` stellt sicher, dass alle Entwickler:innen sowie die CI/CD-Pipeline dieselben Paketversionen verwenden.
Dadurch werden reproduzierbare und stabile Umgebungen gewährleistet.


**Erstellung/Aktualisierung**

```bash
uv lock # erstellen oder aktualisieren
 ```
**Verwendung in der CI/CD Pipeline**

In der Pipeline wird die Datei verwendet, um exakt die definierten Versionen zu installieren
```bash
  uv sync # installiert alle Abhängigkeiten
  ```
**Hinweise**
  - `uv.lock` sollte im Repository versioniert (committed) werden
  - Die Datei sollte **nicht** manuell bearbeitet werden

### Linter
Für die Codequalität und einheitliche Formatierung werden mehrere Tools verwendet, die über pre-commit und den Python-Linter Ruff integriert sind.

**Verwendete Tools**

- **Ruff**: Schneller Linter und Formatter (PEP8, Imports, Bugs, Naming, etc.)
- **Mypy**: Statische Typüberprüfung
- **Pydoclint**: Prüfung von Docstrings
- **nbqa**: Ermöglicht Linting und Formatting von Jupyter Notebooks

**Zweck**
- Konsistenter Code-Stil im gesamten Projekt
- Frühes Erkennen von Fehlern
- Bessere Lesbarkeit und Wartbarkeit

**Installation**
```bash
uv sync --extra dev
 ```

**Verwendung**

Manuel ausführen
```bash
uv run ruff check .
uv run mypy .
 ```

**Automatische Korrekturen**
```bash
uv run ruff check . --fix # behebt automatisch viele Linting-Probleme
uv run ruff format . # sorgt für ein konsistentes Code-Layout
```

**Für Notebooks**
```bash
uv run nbqa ruff .
uv run nbqa mypy .
```
Mit automatischen Fixes:
```bash
uv run nbqa ruff . --fix
```

### Data Import (Postgres)

Die CSV-Daten werden automatisch beim Start des Datenbank-Containers importiert.

**Funktionsweise**
- **OneDrive Link** Damit der Datenimport stattfinden kann, müssen die CSVs lokal verfügbar sein.
 Das können wir erreichen, indem wir im Sharepoint im `STRAG` Ordner klicken "Verknüpfung zu Onedrive hinzufügen"
- **Import** Sobald die OneDrive-Verknüpfung existiert muss nur noch der Container gestartet werden (`docker compose up`) im Ordner `db/docker`


**Datenquelle (Docker)**

In der `db/docker/.env` Datei kann der lokale Pfad zu den CSV-Daten konfiguriert werden. Dies ist notwendig, da der OneDrive-Pfad je nach Benutzer variiert.

Beispiel in `.env`:
```env
IMPORT_DATA_PATH=C:/Pfad/zu/deinen/Daten
```

In der `docker-compose.yml` wird diese Variable dann verwendet:
```yaml
volumes:
  - "${IMPORT_DATA_PATH}:/import_data"
```
Stelle sicher, dass `IMPORT_DATA_PATH` in deiner lokalen `.env` auf den korrekten Ordner mit den CSV-Dateien zeigt.
Wichtig ist dabei, dass der `IMPORT_DATA_PATH` auf den ordner `Logger` zeigt, da ansonsten auch die (vorerst unnötigen Prozess-Events) importiert werden (und der import fehlschlägt).

 **Manueller Re-Import**

Der Import kann auch von Hand gestartet werden:
```bash
docker exec -it postgres_db /docker-entrypoint-initdb.d/02_import_csv.sh
```
