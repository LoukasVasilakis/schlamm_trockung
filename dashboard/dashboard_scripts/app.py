import dash
import plotly.io as pio
from dash import dcc, html
from data_loader import dates

# Dashboard Guidelines
pio.templates["custom"] = pio.templates["plotly_white"]  # Plotly template erstellen
pio.templates["custom"].layout.font.family = "Arial"  # Schriftfont immer Arial
pio.templates.default = "custom"  # Jeder Plot verwendet automatisch Arial


# App
app = dash.Dash(__name__, use_pages=True)  # Dash-App erstellen
server = app.server


app.layout = html.Div(
    [
        # --- HEADER ---
        html.H1(
            "STRAG AG",  # Titel
            style={"textAlign": "center", "fontFamily": "Arial", "marginBottom": "10px"},
        ),
        # --- NAVIGATION BUTTONS ---
        html.Div(
            [
                dcc.Link("Störmeldungen", href="/stormeldungen", className="nav-button"),
                dcc.Link(
                    "Benutzer-Balkendiagram", href="/benutzer-balkendiagram", className="nav-button"
                ),
            ],
            style={"textAlign": "center", "marginBottom": "30px", "fontFamily": "Arial"},
        ),
        # --- DATE FILTER ---
        html.H3("Select Date", style={"fontFamily": "Arial"}),
        html.Div(
            dcc.DatePickerRange(
                id="date-picker-range",
                min_date_allowed=dates[
                    0
                ].date(),  # Erste Zeile in dates ist das früste auswählbar Datum
                max_date_allowed=dates[
                    -1
                ].date(),  # Letzte Zeile in dates ist das letzte auswählbar Datum
                start_date=dates[0].date(),
                end_date=dates[-1].date(),
                display_format="YYYY-MM-DD",
                updatemode="bothdates",  # Ermöglicht im Kalender ein Start und End Datum zu wählen
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
        # --- PAGE CONTENT ---
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
