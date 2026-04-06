import pandas as pd
import psycopg2
import dash
from dash import html
from dash import dcc
from dash import callback
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go


# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(
    dbname="pro2d_db",  # dbname: name of the database
    user="postgres",    # user/password: login credentials
    password="postgres",
    host="localhost",   # host: where the database server is running (localhost = this machine)
    port="5432" # port: default PostgreSQL port
)

df = pd.read_sql('SELECT "Datum", "Meldung", "evtTyp", "Prio", "Benutzer" FROM events', conn) # Dataframe erstellen

conn.close()  # Close the database connection, avoid open connections (resource leaks)

# Prepare dates
df["Datum"] = pd.to_datetime(df["Datum"], errors="coerce")  # Feature Datum in panda datatime konvertieren
df = df.sort_values("Datum")  # korrekte Reihenfolge sichern

df["Benutzer"] = df["Benutzer"].replace("Vinzenzo Signorelli", "Vincenzo Signorelli")  # Schreibfehler im Namen korrigieren

# Clean data for dashboard
df = df.dropna(subset=["Datum"]).copy()  # Alle Zeilen ohne gültiges Datum entfernen
df["Meldung"] = df["Meldung"].fillna("").astype(str)  # Leere Meldungen mit leerem String füllen und sicher als Text speichern

dates = pd.to_datetime(df["Datum"].dropna().sort_values().dt.normalize().unique())  # Eindeutige Datumswerte ohne Uhrzeit für Slider und Kalender

app = dash.Dash(__name__)  # Dash-App erstellen

app.layout = html.Div([
    html.H1("STRAG AG", style={"textAlign": "center"}), # Obertitel

    html.H3("Select Date"), # Untertitel

    html.Div(
        dcc.DatePickerRange(
            id="date-picker-range",  # Eindeutige ID für Callback-Verknüpfung
            min_date_allowed=dates[0].date(), # Erste Zeile in dates ist das früste auswählbar Datum
            max_date_allowed=dates[-1].date(), # Letzte Zeile in dates ist das letzte auswählbar Datum
            start_date=dates[0].date(), # Gleich hier
            end_date=dates[-1].date(), # Gleich hier
            display_format="YYYY-MM-DD",
            updatemode="bothdates" # Ermöglicht im Kalender ein Start und End Datum zu wählen
        ),
        style={
            "display": "inline-block",  # Kalenderfeld nur so breit wie nötig darstellen
            "marginBottom": "10px"  # Abstand nach unten zum Slider
        }
    ),

    html.Div(
        dcc.RangeSlider(
            min=0,  # Kleinster Sliderwert entspricht dem ersten Datum in dates
            max=len(dates) - 1,  # Grösster Sliderwert entspricht dem letzten Datum in dates
            step=1,  # Slider springt immer genau ein Datum weiter
            value=[0, len(dates) - 1],  # Standardmässig ist der ganze Zeitraum ausgewählt
            marks={
                0: dates[0].strftime("%Y-%m-%d"),
                len(dates) - 1: dates[-1].strftime("%Y-%m-%d")
            },
            id="date-range-slider"  # Eindeutige ID für Callback-Verknüpfung
        ),
        className="slider-wrapper"  # CSS-Klasse für zusätzliche Formatierung des Sliders
    ),

    html.Div(id="output-date", style={"marginTop": "10px", "marginBottom": "20px"}),  # Textausgabe des aktuell gewählten Zeitraums

    html.Div([
        html.Div(
            dcc.Graph(id="stoermeldungen-bar-chart", config={"displayModeBar": False}),  # Balkendiagramm ohne Plotly-Menüleiste
            style={"width": "60%", "display": "inline-block", "verticalAlign": "top"}  # Linkes Diagramm nimmt 60% Breite ein
        ),
        html.Div(
            dcc.Graph(id="benutzer-heatmap", config={"displayModeBar": False}),  # Heatmap ohne Plotly-Menüleiste
            style={"width": "38%", "display": "inline-block", "verticalAlign": "top", "marginLeft": "2%"}  # Rechtes Diagramm nimmt 38% Breite ein
        )
    ])
],
style={  # ästhetische Einstellungen
    "backgroundColor": "#F0FFF0",   # page background color
    "fontFamily": "Arial",          # default font
    "color": "black",               # default text color
    "padding": "20px"               # spacing around content
})


@callback(
    Output("date-range-slider", "value"),
    Input("date-picker-range", "start_date"),
    Input("date-picker-range", "end_date")
)
def update_slider_from_picker(start_date, end_date):
    start_date = pd.to_datetime(start_date)  # Startdatum aus dem Kalender in pandas-Datum umwandeln
    end_date = pd.to_datetime(end_date)  # Enddatum aus dem Kalender in pandas-Datum umwandeln

    start_idx = dates.searchsorted(start_date)  # Position des Startdatums in der dates-Liste finden
    end_idx = dates.searchsorted(end_date)  # Position des Enddatums in der dates-Liste finden

    start_idx = min(start_idx, len(dates) - 1)  # Verhindert, dass der Index ausserhalb des gültigen Bereichs liegt
    end_idx = min(end_idx, len(dates) - 1)  # Verhindert, dass der Index ausserhalb des gültigen Bereichs liegt

    return [start_idx, end_idx]  # Slider auf die gewählten Datumspositionen setzen


@callback(
    Output("output-date", "children"),
    Input("date-range-slider", "value")
)
def show_selected_dates(slider_value):
    start_idx, end_idx = slider_value  # Die beiden Slider-Positionen entpacken
    return f"Selected range: {dates[start_idx].strftime('%Y-%m-%d')} to {dates[end_idx].strftime('%Y-%m-%d')}"  # Gewählten Zeitraum als Text anzeigen


@callback(
    Output("stoermeldungen-bar-chart", "figure"),
    Input("date-range-slider", "value")
)
def update_bar_chart(slider_value):
    start_idx, end_idx = slider_value  # Aktuelle Start- und Endposition des Sliders übernehmen

    start_date = dates[start_idx]  # Startindex in echtes Datum umwandeln
    end_date = dates[end_idx] + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)  # Enddatum bis 23:59:59 des gewählten Tages erweitern

    dff = df[
        (df["Datum"] >= start_date) &
        (df["Datum"] <= end_date) &
        (df["evtTyp"] == "Störmeldungen")
    ].copy()  # Datensatz auf Zeitraum und evtTyp = Störmeldungen filtern

    dff = dff[dff["Meldung"].str.strip() != ""].copy()  # Leere oder nur aus Leerzeichen bestehende Meldungen entfernen

    if dff.empty:
        fig = px.bar(
            x=[],
            y=[],
            orientation="h",
            title="Keine Störmeldungen im gewählten Zeitraum"
        )  # Leeres Diagramm erzeugen, falls keine Daten vorhanden sind
        fig.update_layout(
            plot_bgcolor="#F0FFF0",
            paper_bgcolor="#F0FFF0",
            font=dict(family="Arial", color="black")
        )  # Layout des leeren Diagramms an das Dashboard anpassen
        return fig

    error_counts = dff["Meldung"].value_counts().head(10).sort_values()  # Top 10 häufigste Meldungen zählen und aufsteigend sortieren

    plot_df = error_counts.reset_index()  # Series in DataFrame umwandeln
    plot_df.columns = ["Meldung", "Anzahl"]  # Spalten sinnvoll benennen

    fig = px.bar(
        plot_df,
        x="Anzahl",
        y="Meldung",
        orientation="h",
        title="Top 10 Störmeldungen im gewählten Zeitraum",
    )  # Horizontales Balkendiagramm erstellen

    fig.update_traces(textposition="outside")  # Textposition ausserhalb der Balken festlegen

    fig.update_layout(
        xaxis_title="Anzahl",
        yaxis_title="Störmeldung",
        plot_bgcolor="#F0FFF0",
        paper_bgcolor="#F0FFF0",
        font=dict(family="Arial", color="black"),
        margin=dict(l=220, r=40, t=60, b=40)
    )  # Beschriftungen, Farben und Ränder des Diagramms definieren

    return fig


@callback(
    Output("benutzer-heatmap", "figure"),
    Input("date-range-slider", "value")
)
def update_user_heatmap(slider_value):
    start_idx, end_idx = slider_value  # Aktuelle Start- und Endposition des Sliders übernehmen

    start_date = dates[start_idx]  # Startindex in echtes Datum umwandeln
    end_date = dates[end_idx] + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)  # Enddatum bis 23:59:59 des gewählten Tages erweitern

    dff = df[
        (df["Datum"] >= start_date) &
        (df["Datum"] <= end_date)
    ].copy()  # Datensatz auf den gewählten Zeitraum filtern

    dff = dff[dff["evtTyp"] != "Login/Logout"].copy()  # Login/Logout-Ereignisse ausschliessen
    dff = dff[dff["Benutzer"].notna()].copy()  # Zeilen ohne Benutzer entfernen
    dff = dff[~dff["Benutzer"].isin(["AUTO"])].copy()  # Automatische Systemeinträge ausschliessen

    if dff.empty:
        fig = go.Figure()  # Leere Plotly-Figur erstellen, falls keine Benutzerdaten vorhanden sind
        fig.update_layout(
            title="Keine Benutzerdaten im gewählten Zeitraum",
            plot_bgcolor="#F0FFF0",
            paper_bgcolor="#F0FFF0",
            font=dict(family="Arial", color="black")
        )  # Layout des leeren Diagramms an das Dashboard anpassen
        return fig

    user_counts = dff["Benutzer"].value_counts().sort_values(ascending=False)  # Benutzer nach Anzahl Ereignissen absteigend zählen

    heatmap_df = pd.DataFrame({
        "Benutzer": user_counts.index,
        "Anzahl": user_counts.values
    }).sort_values("Anzahl", ascending=True)  # DataFrame für die Heatmap erstellen und für die Darstellung sortieren

    fig = go.Figure(
        data=go.Heatmap(
            z=heatmap_df[["Anzahl"]].values,
            x=["Anzahl"],
            y=heatmap_df["Benutzer"],  # Benutzer als Zeilenbeschriftung
            colorscale="Reds",  # Farbschema von hellrot bis dunkelrot
            showscale=True,  # Farbskala rechts anzeigen
            text=heatmap_df["Anzahl"],  # Anzahl zusätzlich als Text in den Feldern anzeigen
            texttemplate="%{text}",
            textfont={"color": "black", "size": 12},  # Schriftfarbe und Schriftgrösse in den Feldern
            hovertemplate="Benutzer: %{y}<br>Anzahl: %{z}<extra></extra>",
            ygap=3,  # Trennlinien zwischen Benützerzeilen
            xgap=1
        ) # Beschriftungen, Farben und Ränder des Diagramms definieren
    )

    fig.update_layout(
        title="Benutzer-Aktivität im gewählten Zeitraum",
        xaxis_title="",
        yaxis_title="Benutzer",
        plot_bgcolor="white",
        paper_bgcolor="#F0FFF0",
        font=dict(family="Arial", color="black"),
        margin=dict(l=160, r=40, t=60, b=40)
    )  # Layout der Heatmap definieren

    return fig


if __name__ == "__main__":
    app.run(debug=True)  # App im Debug-Modus starten