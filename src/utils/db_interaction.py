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

    def get_person_events(self, include_login_logout: bool = False) -> pd.DataFrame:
        """Gibt nur Events von echten Personen zurück (ohne AUTO, NaN, Gast, cag)."""
        df = self.get_cleaned_events()

        exclude_users = ["AUTO", "Gast", "cag"]
        df_persons = df[(df["Benutzer"].notna()) & (~df["Benutzer"].isin(exclude_users))]

        if not include_login_logout:
            df_persons = df_persons[df_persons["evtTyp"] != "Login/Logout"]

        return df_persons

    def get_events_by_type(self, event_types: list[str]) -> pd.DataFrame:
        """Gibt Events bestimmter Typen zurück (z.B. 'Sollwert-Vorgaben')."""
        df = self.get_cleaned_events()
        return df[df["evtTyp"].isin(event_types)]

    def get_high_prio_events(self) -> pd.DataFrame:
        """Gibt Events mit hoher Priorität (1.0, 2.0) zurück."""
        df = self.get_cleaned_events()
        return df[df["Prio"].isin([1.0, 2.0])]

    def get_efficiency_metrics(self) -> pd.DataFrame:
        """Berechnet die Effizienz (Events pro Login-Session) pro Benutzer."""

        # Logins zählen
        ll = self.get_events_by_type(["Login/Logout"])
        logins = ll[ll["Meldung"].str.startswith("Login", na=False)]
        login_counts = logins.groupby("Benutzer").size()

        # Relevante Eingriffe (Grenzwertsetzungen etc.)
        eingriff_types = ["Sollwert-Vorgaben", "Aggregate-Vorwahlen", "Programm-Vorwahlen"]
        eingriffe = self.get_events_by_type(eingriff_types)
        eing_counts = eingriffe.groupby("Benutzer").size()

        # Metriken kombinieren
        eff = (eing_counts / login_counts).dropna().round(2)
        return eff.to_frame(name="Events_pro_Login")

    def get_time_analysis_data(self, df: pd.DataFrame | None = None) -> pd.DataFrame:
        """Gibt Daten mit erweiterten Zeitfeldern für die Analyse zurück."""
        df = self.get_cleaned_events() if df is None else df
        df["Datum"] = pd.to_datetime(df["Datum"])
        df["Stunde"] = df["Datum"].dt.hour
        df["Wochentag"] = df["Datum"].dt.day_name()
        df["Ist_Wochenende"] = df["Datum"].dt.dayofweek >= 5
        df["Ist_Nacht"] = (df["Stunde"] >= 22) | (df["Stunde"] < 6)
        return df

    def get_top_meldungen_per_user(
        self, n: int = 5, df: pd.DataFrame | None = None
    ) -> dict[str, pd.Series]:
        """Gibt die Top N Meldungen für jeden Benutzer zurück."""
        df = self.get_person_events() if df is None else df
        result = {}
        for user in df["Benutzer"].unique():
            user_data = df[df["Benutzer"] == user]
            top_n = user_data["Meldung"].value_counts().head(n)
            result[user] = top_n
        return result

    def get_events_from_user(
        self, users: list[str], df: pd.DataFrame | None = None
    ) -> pd.DataFrame:
        """Gibt alle Events eines bestimmten Benutzers zurück."""
        df = self.get_cleaned_events() if df is None else df
        return df[df["Benutzer"].isin(users)]

    def get_events_in_time_range(
        self, start: str, end: str, df: pd.DataFrame | None = None
    ) -> pd.DataFrame:
        """Gibt alle Events in einem bestimmten Zeitbereich zurück.(exclude end)"""
        df = self.get_cleaned_events() if df is None else df
        df["Datum"] = pd.to_datetime(df["Datum"])
        start_dt = pd.to_datetime(start)
        end_dt = pd.to_datetime(end)
        return df[(df["Datum"] >= start_dt) & (df["Datum"] < end_dt)]

    def filter_events(
        self, column_to_filter: str, filter_for: list[str], df: pd.DataFrame | None = None
    ) -> pd.DataFrame:
        """Gibt alle Events zurück, die bestimmte Werte in einer Spalte enthalten."""
        df = self.get_cleaned_events() if df is None else df
        return df[df[column_to_filter].isin(filter_for)]
