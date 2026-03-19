import pandas as pd
import plotly.express as px
import psycopg2
from dash import Dash, Input, Output, callback, dcc, html

conn = psycopg2.connect(
    dbname="pro2d_db", user="postgres", password="postgres", host="localhost", port="5432"
)

cur = conn.cursor()

cur.execute("SELECT * FROM events LIMIT 150")
events = cur.fetchall()

cur.close()
conn.close()

df = pd.DataFrame(
    events,
    columns=[
        "Datum",
        "Prio",
        "MSR",
        "Ort",
        "Objekt",
        "Meldung",
        "Zustand",
        "Benutzer",
        "evtID",
        "evtTyp",
    ],
)

app = Dash()

app.layout = [
    html.H1(children="Title of Dash App", style={"textAlign": "center"}),
    dcc.Dropdown(df.evtTyp.unique(), "Login/Logout", id="dropdown-selection"),
    dcc.Graph(id="graph-content"),
]


@callback(Output("graph-content", "figure"), Input("dropdown-selection", "value"))
def update_graph(value):
    dff = df[df.evtTyp == value]
    dff["Date_only"] = dff["Datum"].dt.date
    return px.histogram(dff, x="Date_only")


if __name__ == "__main__":
    app.run(debug=True)
