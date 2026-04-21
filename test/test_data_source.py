import os
from collections.abc import Generator

import pandas as pd
import psycopg2
import pytest
from psycopg2.extensions import connection

from utils.db_interaction import EventDataSource


@pytest.fixture
def connection() -> Generator[connection, None, None]:
    host = "db" if os.getenv("GITLAB_CI") else "localhost"

    conn = psycopg2.connect(
        dbname="pro2d_db", user="postgres", password="postgres", host=host, port="5432"
    )

    yield conn
    conn.close()


@pytest.fixture
def data_source(connection) -> EventDataSource:
    return EventDataSource(connection)


def test_data_source(data_source: EventDataSource) -> None:
    events = data_source.get_all_events()

    assert events is not None


def test_get_cleaned_events(data_source: EventDataSource) -> None:
    all_events = data_source.get_all_events()
    assert all_events is not None
    assert "Vinzenzo Signorelli" in all_events["Benutzer"].values
    assert "Vincenzo Signorelli" in all_events["Benutzer"].values

    cleaned_events = data_source.get_cleaned_events()
    assert cleaned_events is not None
    assert "Vinzenzo Signorelli" not in cleaned_events["Benutzer"].values
    assert "Vincenzo Signorelli" in cleaned_events["Benutzer"].values


def test_get_person_events(data_source: EventDataSource) -> None:
    person_events = data_source.get_person_events()
    assert person_events is not None
    assert all(
        user not in ["AUTO", "Gast", "cag"] and pd.notna(user)
        for user in person_events["Benutzer"].unique()
    )
    assert all(evt != "Login/Logout" for evt in person_events["evtTyp"].unique())

    person_events_with_login = data_source.get_person_events(include_login_logout=True)
    assert person_events_with_login is not None
    assert all(
        user not in ["AUTO", "Gast", "cag"] and pd.notna(user)
        for user in person_events_with_login["Benutzer"].unique()
    )
    assert "Login/Logout" in person_events_with_login["evtTyp"].unique()


def test_get_events_by_type(data_source: EventDataSource) -> None:
    event_types = ["Sollwert-Vorgaben", "Aggregate-Vorwahlen"]
    events_by_type = data_source.get_events_by_type(event_types)
    assert events_by_type is not None
    assert all(evt in event_types for evt in events_by_type["evtTyp"].unique())


def test_get_high_prio_events(data_source: EventDataSource) -> None:
    high_prio_events = data_source.get_high_prio_events()
    assert high_prio_events is not None
    assert all(prio in [1.0, 2.0] for prio in high_prio_events["Prio"].unique())


def test_get_efficiency_metrics(data_source: EventDataSource) -> None:
    efficiency_metrics = data_source.get_efficiency_metrics()
    assert efficiency_metrics is not None
    assert "Events_pro_Login" in efficiency_metrics.columns
    assert efficiency_metrics["Events_pro_Login"].dtype == float
    assert all(efficiency_metrics["Events_pro_Login"] >= 0)


def test_get_time_analysis_data(data_source: EventDataSource) -> None:
    limited_df = data_source.get_events_in_time_range("2020-01-03", "2020-01-04")
    time_analysis_data = data_source.get_time_analysis_data(df=limited_df)
    assert time_analysis_data is not None
    assert "Stunde" in time_analysis_data.columns
    assert all(time_analysis_data["Stunde"].between(5, 14))
    assert "Wochentag" in time_analysis_data.columns
    assert all(time_analysis_data["Wochentag"] == "Friday")
    assert "Ist_Nacht" in time_analysis_data.columns
    assert "Ist_Wochenende" in time_analysis_data.columns
    assert not any(time_analysis_data["Ist_Wochenende"])


def test_get_events_from_user(data_source: EventDataSource) -> None:
    user_events_empty = data_source.get_events_from_user(["Vinzenzo Signorelli"])
    assert len(user_events_empty) == 0

    user_events = data_source.get_events_from_user(["Roland Reinle"])
    assert user_events is not None

    timed_user_events = data_source.get_events_in_time_range(
        "2020-01-01", "2020-01-07", df=user_events
    )
    assert len(timed_user_events) == 143


def test_get_top_meldungen_per_user(data_source: EventDataSource) -> None:
    top_meldungen = data_source.get_top_meldungen_per_user(n=3)
    assert top_meldungen is not None
    for _user, meldungen in top_meldungen.items():
        assert len(meldungen) <= 3


def test_get_events_in_time_range(data_source: EventDataSource) -> None:
    start_date = "2024-01-01"
    end_date = "2024-01-31"
    events_in_range = data_source.get_events_in_time_range(start_date, end_date)
    assert events_in_range is not None
    assert all(
        pd.to_datetime(start_date) <= pd.to_datetime(d) < pd.to_datetime(end_date)
        for d in events_in_range["Datum"]
    )
