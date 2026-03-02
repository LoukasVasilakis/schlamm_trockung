## Vorbereitung
### Anwesend
- Loukas
- Harman
- Alessio
- Janis
- Melanie

### Besprochen wurde
- Wie organisieren wir die nächsten Termine mit dem Kunden? -> Termin im Team planen und dann den Kunden anfragen
- Mögliche Projektstruktur: Wöchentliche kleine Meetings, regelmässig grosse Meetings, Teams in Teams
- Wer übernimmt den Lead? -> Wir alle diskutieren, bei Stille greift Alessio ein
- AI Governance -> Siehe Issue

## Kundenmeeting
### Anwesend
Alle aus dem Projektteam, Barabara, Salomon, Kundenseitig: Daniel Wymann, Reto Balz lässt sich entschuldigen

### Besprochen wurde
- Kennenlernen: Alle Stellen sich vor -> Daniel Wymann ist Geschäftsleiter der STRAG AG, kennt die FHNW vom Studium
- Präsentation der STRAG AG:
    - Klärschlammtrocknungsanlage -> Trockener Schlamm (TS) wird als Brennstoff verbrennt (Holcim in Würenlingen)
    - Anlage ist im Dauerbetrieb, 24/7, fast 365 Tage (2-3 Wochen ausgeschaltet für Revisionen) und läuft autonom über Prozessleitsystem (PLS)
    - Es gibt eine ganze Datenbank voller Daten (ca 10 Jahre), welche bis jetzt noch nicht ausgewertet wurden -> Werden auf täglicher Basis als .csv exportiert
    - Erhoffter Output: Auswertung der Meldungen über die Zeit, Strukturierung nach Event Typ, aufbereitete Darstellung zur schnellen Interpretation (Dashboard?)
    - Erste Fragestellungen: 
        - Welche Aggregate / Teilaggregate verursachen am meisten Anlagenstops während "Abwesenheit"? 
        - Welche Sensoren und Aktoren verursachen am meisten Anlagenstopps?
        - In welchem Zeitrahmen werden die meisten Stops verursacht?
    - Grosse Anlage mit diversen Hilfssystemen wie Abluft-Reinigung und Kühlung
    - Datenstruktur, nach Kundenprio sortiert
        - Timestamp
        - eventTyp
        - Priorität (Prio 1 wichtig für uns)
        - Meldung
        - Benutzer
        - Objekt
        - Zustand
        - MSR NR
        - Ort
        - eventID
- Reto und Daniel sind offen für Veränderungen, sowohl an der Prio als auch an anderen Teilen des Systems
- Fehlalarme gibt es eigentlich nicht, Alarm immer wenn Bedingung erfüllt -> Eventuell müsste man die Bedingungen anpassen
- Erstmal Fokus nur auf Meldungen und dann eventuell in einem späteren Schritt Bedingungen überprüfen
- Es gibt auch Prozessdaten, welche wir ebenfalls anschauen könnten, wurden aktuell aber noch nicht präsentiert
- Diverse Fragen zu den Daten und zum Prozess -> Miro-Board zeigt Antworten zu unseren Fragen
- Daniel und Reto sind im Teams eingeladen und werden die Daten da hinterlegen

## Nachbesprechung
### Anwesend
Alle Projektteilnehmer, Salomon und Barbara

### Besprochen wurde
- Was sind die nächsten Schritte? -> EDA und Data Wrangling
- DeepDive nächste Woche überspringen und für EDA nutzen, dafür später mal einen Input zu Analyse-Thematik
- Eventuell Aufteilung der Projektteilnehmer in zwei Teams um die Aufgaben zu erfüllen

### Beschlossen wurde
- Im Meeting morgen diskutieren wir Tasks, Rollenverteilung, Projekt-Vorgehen, etc.
- Im DeepDive montags betreiben wir EDA und Data Wrangling und wenn möglich schon das Sprint-Ziel erfüllen.
- **Sprint-Ziel**: Wir wollen dem Kunden am Ende des Sprints zeigen, welche Fehlermeldung der höchsten Prio(s) am öftesten aufgetreten sind.

