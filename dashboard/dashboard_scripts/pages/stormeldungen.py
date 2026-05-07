import dash
import pandas as pd
import psycopg2
import plotly.express as px
from dash import callback, dcc, html
from dash.dependencies import Input, Output


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


if not __name__.startswith("test"):
    dash.register_page(__name__, path="/stormeldungen", name="Störmeldungen")


layout = html.Div(
    [
        html.H2(
            "Top 10 Störmeldungen",
            style={"fontFamily": "Arial", "textAlign": "center"},
        ),
        dcc.Graph(id="stoermeldungen-bar-chart", config={"displayModeBar": False}),
    ]
)


@callback(
    Output("stoermeldungen-bar-chart", "figure"),
    Input("date-range-slider", "value"),
)
def update_bar_chart(slider_value):
    start_idx, end_idx = slider_value

    start_date = dates[start_idx]
    end_date = dates[end_idx] + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)

    dff = df[
        (df["Datum"] >= start_date)
        & (df["Datum"] <= end_date)
        & (df["evtTyp"] == "Störmeldungen")
    ].copy()

    dff = dff[dff["Meldung"].str.strip() != ""].copy()

    if dff.empty:
        fig = px.bar(
            x=[],
            y=[],
            orientation="h",
            title="Keine Störmeldungen im gewählten Zeitraum",
        )
        fig.update_layout(
            plot_bgcolor="#F0FFF0",
            paper_bgcolor="#F0FFF0",
            font=dict(family="Arial", color="black"),
        )
        return fig

    error_counts = dff["Meldung"].value_counts().head(10).sort_values()

    plot_df = error_counts.reset_index()
    plot_df.columns = ["Meldung", "Anzahl"]

    fig = px.bar(
        plot_df,
        x="Anzahl",
        y="Meldung",
        orientation="h",
        title="Top 10 Störmeldungen im gewählten Zeitraum",
    )

    fig.update_traces(
        text=plot_df["Anzahl"],
        textposition="outside",
    )

    fig.update_layout(
        xaxis_title="Anzahl",
        yaxis_title="Störmeldung",
        plot_bgcolor="#F0FFF0",
        paper_bgcolor="#F0FFF0",
        font=dict(family="Arial", color="black"),
        margin=dict(l=220, r=40, t=60, b=40),
    )

    return fig