import dash
import pandas as pd
import plotly.io as pio
import psycopg2
from dash import dcc, html


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

    dates = pd.to_datetime(df["Datum"].dropna().sort_values().dt.normalize().unique())

    return df, dates


df, dates = load_data()


# Dashboard Guidelines
pio.templates["custom"] = pio.templates["plotly_white"]
pio.templates["custom"].layout.font.family = "Arial"
pio.templates.default = "custom"


# App
app = dash.Dash(__name__, use_pages=True)
server = app.server


app.layout = html.Div(
    [
        html.H1(
            "STRAG AG",
            style={"textAlign": "center", "fontFamily": "Arial", "marginBottom": "10px"},
        ),
        html.H3("Datum auswählen", style={"fontFamily": "Arial"}),
        html.Div(
            dcc.DatePickerRange(
                id="date-picker-range",
                min_date_allowed=dates[0].date(),
                max_date_allowed=dates[-1].date(),
                start_date=dates[0].date(),
                end_date=dates[-1].date(),
                display_format="YYYY-MM-DD",
                updatemode="bothdates",
            ),
            style={"display": "inline-block", "marginBottom": "10px"},
        ),
        html.Div(
            dcc.RangeSlider(
                min=0,
                max=len(dates) - 1,
                step=1,
                value=[0, len(dates) - 1],
                marks={
                    0: dates[0].strftime("%Y-%m-%d"),
                    len(dates) - 1: dates[-1].strftime("%Y-%m-%d"),
                },
                id="date-range-slider",
            ),
            className="slider-wrapper",
        ),
        html.Div(
            id="output-date",
            style={"marginTop": "10px", "marginBottom": "20px", "fontFamily": "Arial"},
        ),
        dash.page_container,
    ],
    style={
        "backgroundColor": "#F0FFF0",
        "fontFamily": "Arial",
        "color": "black",
        "padding": "20px",
        "minHeight": "100vh",
    },
)


if __name__ == "__main__":
    app.run(debug=True)
