import pandas as pd


class EventDataSource:
    def __init__(self, connection):
        self.db = connection

    def get_all_events(self) -> pd.DataFrame:
        """Gibt alle Events aus der Datenbank zurück."""
        return pd.read_sql("SELECT * FROM events", self.db)

    def get_cleaned_events(self) -> pd.DataFrame:
        """Gibt alle Events mit bereinigten Benutzernamen zurück."""
        df = self.get_all_events()
        df["Benutzer"] = df["Benutzer"].replace("Vinzenzo Signorelli", "Vincenzo Signorelli")
        return df

    def get_person_events(self, include_login_logout=False) -> pd.DataFrame:
        """Gibt nur Events von echten Personen zurück (ohne AUTO, NaN, Gast, cag)."""
        df = self.get_cleaned_events()

        exclude_users = ["AUTO", "Gast", "cag"]
        df_persons = df[(df["Benutzer"].notna()) & (~df["Benutzer"].isin(exclude_users))]

        if not include_login_logout:
            df_persons = df_persons[df_persons["evtTyp"] != "Login/Logout"]

        return df_persons

    def get_events_by_type(self, event_types: list) -> pd.DataFrame:
        """Gibt Events bestimmter Typen zurück (z.B. 'Sollwert-Vorgaben')."""
        df = self.get_cleaned_events()
        return df[df["evtTyp"].isin(event_types)]

    def get_high_prio_events(self) -> pd.DataFrame:
        """Gibt Events mit hoher Priorität (1.0, 2.0) zurück."""
        df = self.get_cleaned_events()
        return df[df["Prio"].isin([1.0, 2.0])]

    def get_efficiency_metrics(self) -> pd.DataFrame:
        """Berechnet die Effizienz (Events pro Login-Session) pro Benutzer."""
        df = self.get_cleaned_events()

        # Logins zählen
        ll = df[df["evtTyp"] == "Login/Logout"]
        logins = ll[ll["Meldung"].str.startswith("Login", na=False)]
        login_counts = logins.groupby("Benutzer").size()

        # Relevante Eingriffe (Grenzwertsetzungen etc.)
        eingriff_types = ["Sollwert-Vorgaben", "Aggregate-Vorwahlen", "Programm-Vorwahlen"]
        eingriffe = df[df["evtTyp"].isin(eingriff_types)]
        eing_counts = eingriffe.groupby("Benutzer").size()

        # Metriken kombinieren
        eff = (eing_counts / login_counts).dropna().round(2)
        return eff.to_frame(name="Events_pro_Login")

    def get_time_analysis_data(self) -> pd.DataFrame:
        """Gibt Daten mit erweiterten Zeitfeldern für die Analyse zurück."""
        df = self.get_cleaned_events()
        df["Datum"] = pd.to_datetime(df["Datum"])
        df["Stunde"] = df["Datum"].dt.hour
        df["Wochentag"] = df["Datum"].dt.day_name()
        df["Ist_Wochenende"] = df["Datum"].dt.dayofweek >= 5
        df["Ist_Nacht"] = (df["Stunde"] >= 22) | (df["Stunde"] < 6)
        return df

    def get_top_meldungen_per_user(self, n=5) -> dict:
        """Gibt die Top N Meldungen für jeden Benutzer zurück."""
        df = self.get_person_events()
        result = {}
        for user in df["Benutzer"].unique():
            user_data = df[df["Benutzer"] == user]
            top_n = user_data["Meldung"].value_counts().head(n)
            result[user] = top_n
        return result
