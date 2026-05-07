import dash
import pandas as pd
import psycopg2
from dash import Input, Output, callback


def load_data():
    conn = psycopg2.connect(
        dbname="pro2d_db",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432",
    )

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

    df = df.dropna(subset=["Datum"]).copy()
    df["Meldung"] = df["Meldung"].fillna("").astype(str)

    dates = pd.to_datetime(
        df["Datum"]
        .dropna()
        .sort_values()
        .dt.normalize()
        .unique()
    )

    return df, dates


df, dates = load_data()


@callback(
    Output("date-range-slider", "value"),
    Output("date-picker-range", "start_date"),
    Output("date-picker-range", "end_date"),
    Input("date-picker-range", "start_date"),
    Input("date-picker-range", "end_date"),
    Input("date-range-slider", "value"),
)
def sync_date_controls(start_date, end_date, slider_value):
    trigger = dash.callback_context.triggered_id

    if trigger == "date-picker-range":
        if start_date is None or end_date is None:
            return dash.no_update, dash.no_update, dash.no_update

        selected_start = pd.to_datetime(start_date)
        selected_end = pd.to_datetime(end_date)

        start_idx = dates.searchsorted(selected_start)
        end_idx = dates.searchsorted(selected_end)

        start_idx = max(0, min(start_idx, len(dates) - 1))
        end_idx = max(0, min(end_idx, len(dates) - 1))

        return [start_idx, end_idx], dash.no_update, dash.no_update

    if trigger == "date-range-slider":
        start_idx, end_idx = slider_value

        return (
            dash.no_update,
            dates[start_idx].date(),
            dates[end_idx].date(),
        )

    return slider_value, start_date, end_date


@callback(
    Output("output-date", "children"),
    Input("date-range-slider", "value"),
)
def show_selected_dates(slider_value):
    start_idx, end_idx = slider_value

    return (
        f"Selected range: "
        f"{dates[start_idx].strftime('%Y-%m-%d')} "
        f"to {dates[end_idx].strftime('%Y-%m-%d')}"
    )