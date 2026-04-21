import sys
import types
import importlib.util
from pathlib import Path

import pandas as pd
import pytest
import dash

"""
Skript, um Fake-Daten zu erstellen und diese für Unit-Tests bereitzustellen.

Nutzt, um:
- ein kleines, kontrolliertes Test-Dataset (df, dates) zu erzeugen
- reproduzierbare und schnelle Tests zu ermöglichen

Zusätzlich Hilfsfunktion, die:
- Dashboard-Module dynamisch lädt
- dabei das data_loader-Modul durch Fake-Daten ersetzt (Monkeypatching)
- dash.register_page deaktiviert, damit Tests ohne laufende Dash-App funktionieren
"""


@pytest.fixture
def fake_dashboard_data():
    df = pd.DataFrame(
        {
            "Datum": pd.to_datetime(
                [
                    "2024-01-01 08:00:00",
                    "2024-01-01 09:00:00",
                    "2024-01-02 10:00:00",
                    "2024-01-03 11:00:00",
                    "2024-01-03 12:00:00",
                    "2024-01-04 13:00:00",
                ]
            ),
            "Meldung": [
                "Pumpe Fehler",
                "Pumpe Fehler",
                "Sensor Alarm",
                "",
                "Motor Störung",
                "Pumpe Fehler",
            ],
            "evtTyp": [
                "Störmeldungen",
                "Störmeldungen",
                "Störmeldungen",
                "Warnungen",
                "Störmeldungen",
                "Warnungen",
            ],
            "Prio": [1, 1, 2, 2, 1, 3],
            "Benutzer": [
                "Alice",
                "Bob",
                "AUTO",
                None,
                "Alice",
                "Charlie",
            ],
        }
    )

    dates = pd.to_datetime(df["Datum"].dt.normalize().sort_values().unique())

    return df, dates


def load_module_with_fake_data(module_file_path, module_name, df, dates, monkeypatch):
    """
    Load a dashboard page/callback module from file path while mocking:
    - dash.register_page
    - data_loader.df
    - data_loader.dates
    """
    fake_data_loader = types.ModuleType("data_loader")
    fake_data_loader.df = df
    fake_data_loader.dates = dates

    monkeypatch.setitem(sys.modules, "data_loader", fake_data_loader)
    monkeypatch.setattr(dash, "register_page", lambda *args, **kwargs: None)

    spec = importlib.util.spec_from_file_location(module_name, module_file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


@pytest.fixture
def project_root():
    return Path(__file__).resolve().parents[1]


@pytest.fixture
def pages_dir(project_root):
    return project_root / "dashboard" / "dashboard_scripts" / "pages"


@pytest.fixture
def dashboard_scripts_dir(project_root):
    return project_root / "dashboard" / "dashboard_scripts"
