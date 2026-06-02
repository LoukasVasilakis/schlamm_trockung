import sqlite3
from pathlib import Path

import dash
import pandas as pd
from dash import Input, Output, callback


def load_data():
    db_path = Path(__file__).resolve().parent.parent.parent / "db" / "sqlite" / "events.sqlite"
    conn = sqlite3.connect(db_path)

    df = pd.read_sql(
        'SELECT "Datum", "Meldung", "evtTyp", "Prio", "Benutzer" FROM events',
        conn,
    )

    conn.close()

    df["Datum"] = pd.to_datetime(df["Datum"], errors="coerce")
    df = df.sort_values("Datum")

    df["Benutzer"] = df["Benutzer"].replace(
        "Vinzenzo Signorelli",
        "Vincenzo Signorelli",
    )

    df = df.dropna(subset=["Datum"])
    df["Meldung"] = df["Meldung"].fillna("").astype(str)

    categorical_cols = ["evtTyp", "Prio", "Benutzer"]
    for col in categorical_cols:
        df[col] = df[col].astype("category")

    dates = pd.to_datetime(df["Datum"].dropna().sort_values().dt.normalize().unique())

    return df, dates


df, dates = load_data()


@callback(
    Output("date-range-slider", "value"),
    Output("date-picker-range", "start_date"),
    Output("date-picker-range", "end_date"),
    Input("date-picker-range", "start_date"),
    Input("date-picker-range", "end_date"),
    Input("date-range-slider", "value"),
    prevent_initial_call=False,
)
def sync_date_controls(start_date, end_date, slider_value):
    """Synchronize date picker and range slider in both directions."""
    trigger_id = dash.callback_context.triggered_id

    # If date picker changed, update slider
    if trigger_id in ["date-picker-range.start_date", "date-picker-range.end_date"]:
        if start_date is None or end_date is None:
            return dash.no_update, dash.no_update, dash.no_update

        selected_start = pd.to_datetime(start_date)
        selected_end = pd.to_datetime(end_date)

        start_idx = dates.searchsorted(selected_start)
        end_idx = dates.searchsorted(selected_end)

        # Clamp to valid range
        start_idx = max(0, min(start_idx, len(dates) - 1))
        end_idx = max(0, min(end_idx, len(dates) - 1))

        return [start_idx, end_idx], dash.no_update, dash.no_update

    # If slider changed, update date picker
    if trigger_id == "date-range-slider":
        if slider_value is None or len(slider_value) < 2:
            return dash.no_update, dash.no_update, dash.no_update

        start_idx, end_idx = slider_value
        return dash.no_update, dates[start_idx].date(), dates[end_idx].date()

    # Initial call or state preservation
    return dash.no_update, dash.no_update, dash.no_update


@callback(
    Output("output-date", "children"),
    Input("date-picker-range", "start_date"),
    Input("date-picker-range", "end_date"),
    Input("date-range-slider", "value"),
    prevent_initial_call=False,
)
def show_selected_dates(start_date, end_date, slider_value):
    """Display the selected date range from either the picker or slider."""
    # Prefer date picker values if available
    if start_date and end_date:
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
    elif slider_value and len(slider_value) >= 2:
        start_idx, end_idx = slider_value
        start = dates[start_idx]
        end = dates[end_idx]
    else:
        return ""

    return f"Ausgewählter Zeitraum: {start.strftime('%Y-%m-%d')} bis {end.strftime('%Y-%m-%d')}"
