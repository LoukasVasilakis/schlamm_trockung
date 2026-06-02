import sqlite3
from pathlib import Path

import dash
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import callback, dcc, html
from dash.dependencies import Input, Output


def load_data():
    db_path = (
        Path(__file__).resolve().parent.parent.parent.parent / "db" / "sqlite" / "events.sqlite"
    )
    conn = sqlite3.connect(db_path)
    df = pd.read_sql(
        'SELECT "Datum", "Meldung", "evtTyp", "Prio", "Benutzer", "Ort", "Objekt", "Msr",'
        ' "Zustand" FROM events',
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

    categorical_cols = ["evtTyp", "Prio", "Zustand", "Ort", "Benutzer", "Objekt", "Msr"]
    for col in ["Meldung"] + categorical_cols:
        df[col] = df[col].fillna("NaN").astype(str)
        df.loc[df[col].str.strip() == "", col] = "NaN"

    for col in categorical_cols:
        df[col] = df[col].astype("category")

    dates = pd.to_datetime(df["Datum"].dropna().sort_values().dt.normalize().unique())

    return df, dates


df, dates = load_data()


def build_simple_options(series):
    if hasattr(series, "cat"):
        # Faster unique() for categorical data
        unique_vals = sorted(series.unique().dropna().astype(str))
    else:
        unique_vals = sorted(series.dropna().astype(str).unique())
    return [{"label": v, "value": v} for v in unique_vals]


if not __name__.startswith("test"):
    dash.register_page(__name__, path="/", name="Störmeldungen")


layout = html.Div(
    [
        # ---- Filter-Bereich ----
        html.Div(
            [
                # Zeile 1: Dropdowns
                html.Div(
                    [
                        html.Div(
                            [
                                html.Label(
                                    "evtTyp",
                                    style={
                                        "fontFamily": "Arial",
                                        "fontWeight": "bold",
                                        "marginBottom": "4px",
                                        "display": "block",
                                    },
                                ),
                                dcc.Dropdown(
                                    id="stoer-evttyp-dropdown",
                                    options=build_simple_options(df["evtTyp"]),
                                    value=["Störmeldungen"],
                                    multi=True,
                                    placeholder="Alle",
                                    style={"width": "200px", "fontFamily": "Arial"},
                                ),
                            ],
                            style={"marginRight": "20px"},
                        ),
                        html.Div(
                            [
                                html.Label(
                                    "Objekt",
                                    style={
                                        "fontFamily": "Arial",
                                        "fontWeight": "bold",
                                        "marginBottom": "4px",
                                        "display": "block",
                                    },
                                ),
                                dcc.Dropdown(
                                    id="stoer-objekt-dropdown",
                                    options=[],
                                    value=[],
                                    multi=True,
                                    placeholder="Alle",
                                    style={"width": "200px", "fontFamily": "Arial"},
                                ),
                            ],
                            style={"marginRight": "20px"},
                        ),
                        html.Div(
                            [
                                html.Label(
                                    "Msr",
                                    style={
                                        "fontFamily": "Arial",
                                        "fontWeight": "bold",
                                        "marginBottom": "4px",
                                        "display": "block",
                                    },
                                ),
                                dcc.Dropdown(
                                    id="stoer-msr-dropdown",
                                    options=[],
                                    value=[],
                                    multi=True,
                                    placeholder="Alle",
                                    style={"width": "200px", "fontFamily": "Arial"},
                                ),
                            ],
                            style={"marginRight": "20px"},
                        ),
                        html.Div(
                            [
                                html.Label(
                                    "Meldung",
                                    style={
                                        "fontFamily": "Arial",
                                        "fontWeight": "bold",
                                        "marginBottom": "4px",
                                        "display": "block",
                                    },
                                ),
                                dcc.Dropdown(
                                    id="stoer-meldung-dropdown",
                                    options=[],
                                    value=[],
                                    multi=True,
                                    placeholder="Alle",
                                    style={"width": "200px", "fontFamily": "Arial"},
                                ),
                            ],
                            style={"marginRight": "20px"},
                        ),
                        html.Div(
                            [
                                html.Label(
                                    "Prio",
                                    style={
                                        "fontFamily": "Arial",
                                        "fontWeight": "bold",
                                        "marginBottom": "4px",
                                        "display": "block",
                                    },
                                ),
                                dcc.Dropdown(
                                    id="stoer-prio-dropdown",
                                    options=[],
                                    value=[],
                                    multi=True,
                                    placeholder="Alle",
                                    style={"width": "140px", "fontFamily": "Arial"},
                                ),
                            ],
                            style={"marginRight": "20px"},
                        ),
                        html.Div(
                            [
                                html.Label(
                                    "Ort",
                                    style={
                                        "fontFamily": "Arial",
                                        "fontWeight": "bold",
                                        "marginBottom": "4px",
                                        "display": "block",
                                    },
                                ),
                                dcc.Dropdown(
                                    id="stoer-ort-dropdown",
                                    options=[],
                                    value=[],
                                    multi=True,
                                    placeholder="Alle",
                                    style={"width": "200px", "fontFamily": "Arial"},
                                ),
                            ],
                            style={"marginRight": "20px"},
                        ),
                        html.Div(
                            [
                                html.Label(
                                    "Zustand",
                                    style={
                                        "fontFamily": "Arial",
                                        "fontWeight": "bold",
                                        "marginBottom": "4px",
                                        "display": "block",
                                    },
                                ),
                                dcc.Dropdown(
                                    id="stoer-zustand-dropdown",
                                    options=[],
                                    value=[],
                                    multi=True,
                                    placeholder="Alle",
                                    style={"width": "200px", "fontFamily": "Arial"},
                                ),
                            ],
                            style={"marginRight": "20px"},
                        ),
                        html.Div(
                            [
                                html.Label(
                                    "Benutzer",
                                    style={
                                        "fontFamily": "Arial",
                                        "fontWeight": "bold",
                                        "marginBottom": "4px",
                                        "display": "block",
                                    },
                                ),
                                dcc.Dropdown(
                                    id="stoer-benutzer-dropdown",
                                    options=[],
                                    value=[],
                                    multi=True,
                                    placeholder="Alle",
                                    style={"width": "200px", "fontFamily": "Arial"},
                                ),
                            ],
                        ),
                    ],
                    style={
                        "display": "flex",
                        "flexWrap": "wrap",
                        "alignItems": "flex-start",
                        "marginBottom": "16px",
                    },
                ),
                # Zeile 2: Steuerung
                html.Div(
                    [
                        html.Div(
                            [
                                html.Label(
                                    "Top N",
                                    style={
                                        "fontFamily": "Arial",
                                        "fontWeight": "bold",
                                        "marginBottom": "4px",
                                        "display": "block",
                                    },
                                ),
                                dcc.Dropdown(
                                    id="stoer-topn-dropdown",
                                    options=[
                                        {"label": "Alle", "value": "ALL"},
                                        {"label": "5", "value": 5},
                                        {"label": "10", "value": 10},
                                        {"label": "15", "value": 15},
                                        {"label": "20", "value": 20},
                                    ],
                                    value=10,
                                    clearable=False,
                                    style={"width": "100px", "fontFamily": "Arial"},
                                ),
                            ],
                            style={"marginRight": "30px"},
                        ),
                        html.Div(
                            [
                                html.Label(
                                    "Y-Achse",
                                    style={
                                        "fontFamily": "Arial",
                                        "fontWeight": "bold",
                                        "marginBottom": "4px",
                                        "display": "block",
                                    },
                                ),
                                dcc.RadioItems(
                                    id="stoer-yaxis-toggle",
                                    options=[
                                        {"label": " evtTyp", "value": "evtTyp"},
                                        {"label": " Objekt", "value": "Objekt"},
                                        {"label": " Msr", "value": "Msr"},
                                        {"label": " Meldung", "value": "Meldung"},
                                        {"label": " Prio", "value": "Prio"},
                                        {"label": " Ort", "value": "Ort"},
                                        {"label": " Zustand", "value": "Zustand"},
                                        {"label": " Benutzer", "value": "Benutzer"},
                                    ],
                                    value="Meldung",
                                    inline=True,
                                    style={"fontFamily": "Arial"},
                                ),
                            ],
                            style={"marginRight": "30px"},
                        ),
                        html.Div(
                            [
                                html.Label(
                                    "Ansicht",
                                    style={
                                        "fontFamily": "Arial",
                                        "fontWeight": "bold",
                                        "marginBottom": "4px",
                                        "display": "block",
                                    },
                                ),
                                dcc.RadioItems(
                                    id="stoer-view-toggle",
                                    options=[
                                        {"label": " Absolut", "value": "absolut"},
                                        {"label": " Prozentual", "value": "prozentual"},
                                    ],
                                    value="absolut",
                                    inline=True,
                                    style={"fontFamily": "Arial"},
                                ),
                            ],
                            style={"marginRight": "30px"},
                        ),
                        html.Div(
                            [
                                html.Button(
                                    "Reset Filter",
                                    id="stoer-reset-button",
                                    n_clicks=0,
                                    style={
                                        "fontFamily": "Arial",
                                        "fontWeight": "bold",
                                        "padding": "8px 18px",
                                        "cursor": "pointer",
                                        "backgroundColor": "#e89090",
                                        "border": "1px solid #c97070",
                                        "borderRadius": "4px",
                                        "color": "#4a0000",
                                        "marginTop": "22px",
                                    },
                                ),
                            ],
                        ),
                    ],
                    style={"display": "flex", "alignItems": "flex-start"},
                ),
            ],
            style={"marginBottom": "20px"},
        ),
        # ---- Mini-Plot Zeitverlauf (einklappbar) ----
        html.Details(
            [
                html.Summary(
                    "Zeitverlauf (Events pro Tag)",
                    style={
                        "fontFamily": "Arial",
                        "fontWeight": "bold",
                        "cursor": "pointer",
                        "fontSize": "16px",
                        "marginBottom": "5px",
                    },
                ),
                dcc.Graph(id="stoer-timeline-mini", config={"displayModeBar": False}),
            ],
        ),
        # ---- Extremwert-Entfernung (einklappbar) ----
        html.Details(
            [
                html.Summary(
                    "Extremwerte entfernen",
                    style={
                        "fontFamily": "Arial",
                        "fontWeight": "bold",
                        "cursor": "pointer",
                        "fontSize": "16px",
                    },
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Label(
                                    "Threshold (Events/Tag)",
                                    style={"fontFamily": "Arial"},
                                ),
                                dcc.Input(
                                    id="stoer-threshold-input",
                                    type="number",
                                    value=None,
                                    min=0,
                                    step=1,
                                    placeholder="z.B. 5000",
                                    style={
                                        "width": "120px",
                                        "fontFamily": "Arial",
                                        "padding": "5px",
                                    },
                                ),
                                html.Span(
                                    " (Tage mit mehr Events werden entfernt, leer = aus)",
                                    style={
                                        "fontFamily": "Arial",
                                        "fontSize": "12px",
                                        "marginLeft": "5px",
                                    },
                                ),
                            ],
                            style={
                                "display": "inline-block",
                                "marginRight": "20px",
                                "verticalAlign": "top",
                            },
                        ),
                        html.Div(
                            [
                                html.Label(
                                    "Outlier entfernen (Standardabweichungen vom Mittelwert)",
                                    style={"fontFamily": "Arial"},
                                ),
                                dcc.Dropdown(
                                    id="stoer-outlier-sigma",
                                    options=[
                                        {"label": "Aus", "value": "off"},
                                        {"label": "1σ", "value": 1},
                                        {"label": "2σ", "value": 2},
                                        {"label": "3σ", "value": 3},
                                    ],
                                    value="off",
                                    clearable=False,
                                    style={"width": "220px", "fontFamily": "Arial"},
                                ),
                            ],
                            style={
                                "display": "inline-block",
                                "marginRight": "20px",
                                "verticalAlign": "top",
                            },
                        ),
                        html.Div(
                            [
                                html.Label(
                                    "Manuelle Tage ausschliessen", style={"fontFamily": "Arial"}
                                ),
                                dcc.Dropdown(
                                    id="stoer-manual-exclude",
                                    options=[],
                                    value=[],
                                    multi=True,
                                    placeholder="Keine",
                                    style={"width": "400px", "fontFamily": "Arial"},
                                ),
                            ],
                            style={"display": "inline-block", "verticalAlign": "top"},
                        ),
                    ],
                    style={"marginTop": "10px"},
                ),
                html.Div(
                    id="stoer-exclude-stats",
                    style={
                        "marginTop": "15px",
                        "fontFamily": "Arial",
                        "fontSize": "13px",
                        "padding": "8px",
                        "backgroundColor": "#FFFFFF",
                        "borderRadius": "3px",
                    },
                ),
                html.Div(
                    [
                        html.Label(
                            "Y-Achse Skala:", style={"fontFamily": "Arial", "marginRight": "10px"}
                        ),
                        dcc.RadioItems(
                            id="stoer-dist-scale",
                            options=[
                                {"label": " Linear", "value": "linear"},
                                {"label": " Logarithmisch", "value": "log"},
                            ],
                            value="log",
                            inline=True,
                            style={"fontFamily": "Arial", "display": "inline-block"},
                        ),
                    ],
                    style={"marginTop": "10px"},
                ),
                dcc.Graph(id="stoer-distribution-plot", config={"displayModeBar": False}),
            ],
            style={
                "marginTop": "10px",
                "marginBottom": "20px",
                "padding": "10px",
                "backgroundColor": "#E0F0E0",
                "borderRadius": "5px",
            },
        ),
        # ---- Hauptplot ----
        dcc.Graph(
            id="stoermeldungen-bar-chart",
            config={
                "displayModeBar": True,
                "displaylogo": False,
                "toImageButtonOptions": {
                    "format": "png",
                    "filename": "top_meldungen",
                    "scale": 2,
                },
            },
        ),
    ]
)


@callback(
    Output("stoer-evttyp-dropdown", "value"),
    Output("stoer-objekt-dropdown", "value"),
    Output("stoer-msr-dropdown", "value"),
    Output("stoer-meldung-dropdown", "value"),
    Output("stoer-prio-dropdown", "value"),
    Output("stoer-ort-dropdown", "value"),
    Output("stoer-zustand-dropdown", "value"),
    Output("stoer-benutzer-dropdown", "value"),
    Output("stoer-view-toggle", "value"),
    Output("stoer-topn-dropdown", "value"),
    Output("stoer-yaxis-toggle", "value"),
    Output("stoer-threshold-input", "value"),
    Output("stoer-outlier-sigma", "value"),
    Output("stoer-manual-exclude", "value"),
    Output("stoer-dist-scale", "value"),
    Input("stoer-reset-button", "n_clicks"),
    prevent_initial_call=True,
)
def reset_filters(n_clicks):
    return (
        ["Störmeldungen"],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        "absolut",
        10,
        "Meldung",
        None,
        "off",
        [],
        "log",
    )


def _apply_filters(
    df, evttyp, objekt, msr, meldung, prio=None, ort=None, zustand=None, benutzer=None
):
    mask = pd.Series(True, index=df.index)
    if evttyp:
        mask &= df["evtTyp"].isin(evttyp)
    if objekt:
        mask &= df["Objekt"].isin(objekt)
    if msr:
        mask &= df["Msr"].isin(msr)
    if meldung:
        mask &= df["Meldung"].isin(meldung)
    if prio:
        mask &= df["Prio"].isin(prio)
    if ort:
        mask &= df["Ort"].isin(ort)
    if zustand:
        mask &= df["Zustand"].isin(zustand)
    if benutzer:
        mask &= df["Benutzer"].isin(benutzer)
    return df[mask]


def _get_excluded_days(dff, threshold_abs, sigma_choice, manual_excludes):
    if dff.empty:
        return set()

    # Pre-calculate normalized dates to avoid repeated .dt.normalize() calls
    normalized_dates = dff["Datum"].dt.normalize()
    daily_counts = normalized_dates.value_counts()
    excluded = set()

    if threshold_abs is not None and threshold_abs > 0:
        excluded.update(daily_counts[daily_counts > threshold_abs].index)

    if sigma_choice != "off" and len(daily_counts) > 1:
        try:
            n_sigma = int(sigma_choice)
            mean = daily_counts.mean()
            std = daily_counts.std()
            if std > 0:
                outlier_mask = (daily_counts - mean).abs() > n_sigma * std
                excluded.update(daily_counts[outlier_mask].index)
        except (ValueError, TypeError):
            pass

    for d_str in manual_excludes or []:
        excluded.add(pd.Timestamp(d_str))

    return excluded


@callback(
    Output("stoer-objekt-dropdown", "options"),
    Input("stoer-evttyp-dropdown", "value"),
)
def update_objekt_options(evttyp):
    dff = df if not evttyp else df[df["evtTyp"].isin(evttyp)]
    return build_simple_options(dff["Objekt"])


@callback(
    Output("stoer-msr-dropdown", "options"),
    Input("stoer-evttyp-dropdown", "value"),
    Input("stoer-objekt-dropdown", "value"),
)
def update_msr_options(evttyp, objekt):
    dff = _apply_filters(df, evttyp, objekt, [], [])
    return build_simple_options(dff["Msr"])


@callback(
    Output("stoer-meldung-dropdown", "options"),
    Input("stoer-evttyp-dropdown", "value"),
    Input("stoer-objekt-dropdown", "value"),
    Input("stoer-msr-dropdown", "value"),
)
def update_meldung_options(evttyp, objekt, msr):
    dff = _apply_filters(df, evttyp, objekt, msr, [])
    return build_simple_options(dff["Meldung"])


@callback(
    Output("stoer-prio-dropdown", "options"),
    Input("stoer-evttyp-dropdown", "value"),
    Input("stoer-objekt-dropdown", "value"),
    Input("stoer-msr-dropdown", "value"),
    Input("stoer-meldung-dropdown", "value"),
)
def update_prio_options(evttyp, objekt, msr, meldung):
    dff = _apply_filters(df, evttyp, objekt, msr, meldung)
    return build_simple_options(dff["Prio"])


@callback(
    Output("stoer-ort-dropdown", "options"),
    Input("stoer-evttyp-dropdown", "value"),
    Input("stoer-objekt-dropdown", "value"),
    Input("stoer-msr-dropdown", "value"),
    Input("stoer-meldung-dropdown", "value"),
    Input("stoer-prio-dropdown", "value"),
)
def update_ort_options(evttyp, objekt, msr, meldung, prio):
    dff = _apply_filters(df, evttyp, objekt, msr, meldung, prio)
    return build_simple_options(dff["Ort"])


@callback(
    Output("stoer-zustand-dropdown", "options"),
    Input("stoer-evttyp-dropdown", "value"),
    Input("stoer-objekt-dropdown", "value"),
    Input("stoer-msr-dropdown", "value"),
    Input("stoer-meldung-dropdown", "value"),
    Input("stoer-prio-dropdown", "value"),
    Input("stoer-ort-dropdown", "value"),
)
def update_zustand_options(evttyp, objekt, msr, meldung, prio, ort):
    dff = _apply_filters(df, evttyp, objekt, msr, meldung, prio, ort)
    return build_simple_options(dff["Zustand"])


@callback(
    Output("stoer-benutzer-dropdown", "options"),
    Input("stoer-evttyp-dropdown", "value"),
    Input("stoer-objekt-dropdown", "value"),
    Input("stoer-msr-dropdown", "value"),
    Input("stoer-meldung-dropdown", "value"),
    Input("stoer-prio-dropdown", "value"),
    Input("stoer-ort-dropdown", "value"),
    Input("stoer-zustand-dropdown", "value"),
)
def update_benutzer_options(evttyp, objekt, msr, meldung, prio, ort, zustand):
    dff = _apply_filters(df, evttyp, objekt, msr, meldung, prio, ort, zustand)
    return build_simple_options(dff["Benutzer"])


@callback(
    Output("stoer-manual-exclude", "options"),
    Input("date-range-slider", "value"),
    Input("stoer-evttyp-dropdown", "value"),
    Input("stoer-objekt-dropdown", "value"),
    Input("stoer-msr-dropdown", "value"),
    Input("stoer-meldung-dropdown", "value"),
    Input("stoer-prio-dropdown", "value"),
    Input("stoer-ort-dropdown", "value"),
    Input("stoer-zustand-dropdown", "value"),
    Input("stoer-benutzer-dropdown", "value"),
)
def update_manual_exclude_options(
    slider_value, evttyp, objekt, msr, meldung, prio, ort, zustand, benutzer
):
    start_idx, end_idx = slider_value
    start_date = dates[start_idx]
    end_date = dates[end_idx] + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)

    dff = df[(df["Datum"] >= start_date) & (df["Datum"] <= end_date)]
    dff = _apply_filters(dff, evttyp, objekt, msr, meldung, prio, ort, zustand, benutzer)

    available_days = sorted(dff["Datum"].dt.normalize().unique())
    return [
        {
            "label": pd.Timestamp(d).strftime("%Y-%m-%d"),
            "value": pd.Timestamp(d).strftime("%Y-%m-%d"),
        }
        for d in available_days
    ]


@callback(
    Output("stoer-exclude-stats", "children"),
    Input("date-range-slider", "value"),
    Input("stoer-evttyp-dropdown", "value"),
    Input("stoer-objekt-dropdown", "value"),
    Input("stoer-msr-dropdown", "value"),
    Input("stoer-meldung-dropdown", "value"),
    Input("stoer-prio-dropdown", "value"),
    Input("stoer-ort-dropdown", "value"),
    Input("stoer-zustand-dropdown", "value"),
    Input("stoer-benutzer-dropdown", "value"),
    Input("stoer-threshold-input", "value"),
    Input("stoer-outlier-sigma", "value"),
    Input("stoer-manual-exclude", "value"),
)
def update_exclude_stats(
    slider_value,
    evttyp,
    objekt,
    msr,
    meldung,
    prio,
    ort,
    zustand,
    benutzer,
    threshold_abs,
    sigma_choice,
    manual_excludes,
):
    start_idx, end_idx = slider_value
    start_date = dates[start_idx]
    end_date = dates[end_idx] + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)

    dff = df[(df["Datum"] >= start_date) & (df["Datum"] <= end_date)]
    dff = _apply_filters(dff, evttyp, objekt, msr, meldung, prio, ort, zustand, benutzer)

    if dff.empty:
        return "Keine Daten im gewählten Zeitraum."

    total_days = dff["Datum"].dt.normalize().nunique()
    total_events = len(dff)

    excluded = _get_excluded_days(dff, threshold_abs, sigma_choice, manual_excludes)

    if not excluded:
        return (
            f"Keine Tage entfernt. Daten: {total_events:,} Events an {total_days} Tagen.".replace(
                ",", "'"
            )
        )

    excluded_events = len(dff[dff["Datum"].dt.normalize().isin(excluded)])
    pct_days = len(excluded) / total_days * 100 if total_days > 0 else 0
    pct_events = excluded_events / total_events * 100 if total_events > 0 else 0

    return html.Div(
        [
            html.B("Entfernt: "),
            f"{len(excluded)} von {total_days} Tagen ({pct_days:.1f}%) – "
            f"{excluded_events:,} von {total_events:,} Events ({pct_events:.1f}%)".replace(
                ",", "'"
            ),
        ]
    )


@callback(
    Output("stoer-distribution-plot", "figure"),
    Input("date-range-slider", "value"),
    Input("stoer-evttyp-dropdown", "value"),
    Input("stoer-objekt-dropdown", "value"),
    Input("stoer-msr-dropdown", "value"),
    Input("stoer-meldung-dropdown", "value"),
    Input("stoer-prio-dropdown", "value"),
    Input("stoer-ort-dropdown", "value"),
    Input("stoer-zustand-dropdown", "value"),
    Input("stoer-benutzer-dropdown", "value"),
    Input("stoer-outlier-sigma", "value"),
    Input("stoer-threshold-input", "value"),
    Input("stoer-dist-scale", "value"),
)
def update_distribution_plot(
    slider_value,
    evttyp,
    objekt,
    msr,
    meldung,
    prio,
    ort,
    zustand,
    benutzer,
    sigma_choice,
    threshold_abs,
    scale_mode,
):
    import numpy as np

    start_idx, end_idx = slider_value
    start_date = dates[start_idx]
    end_date = dates[end_idx] + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)

    dff = df[(df["Datum"] >= start_date) & (df["Datum"] <= end_date)]
    dff = _apply_filters(dff, evttyp, objekt, msr, meldung, prio, ort, zustand, benutzer)

    if dff.empty or dff["Datum"].dt.normalize().nunique() < 2:
        fig = go.Figure()
        fig.update_layout(
            height=250,
            plot_bgcolor="#F0FFF0",
            paper_bgcolor="#F0FFF0",
            margin=dict(l=40, r=20, t=30, b=30),
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
        )
        fig.add_annotation(
            text="Zu wenig Daten für Verteilung",
            x=0.5,
            y=0.5,
            xref="paper",
            yref="paper",
            showarrow=False,
        )
        return fig

    daily_counts = dff.groupby(dff["Datum"].dt.normalize()).size()
    mean = daily_counts.mean()
    std = daily_counts.std()

    cutoff = None
    if sigma_choice != "off" and std > 0:
        try:
            n_sigma = int(sigma_choice)
            cutoff = mean + n_sigma * std
        except (ValueError, TypeError):
            pass

    if threshold_abs is not None and threshold_abs > 0:
        cutoff = min(cutoff, threshold_abs) if cutoff is not None else threshold_abs

    values = daily_counts.values
    counts_hist, bin_edges = np.histogram(values, bins=30, density=True)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    bin_width = bin_edges[1] - bin_edges[0]

    if cutoff is not None:
        colors = ["red" if c > cutoff else "#2ca02c" for c in bin_centers]
    else:
        colors = ["#2ca02c"] * len(bin_centers)

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=bin_centers,
            y=counts_hist,
            width=bin_width,
            marker=dict(color=colors, line=dict(color="black", width=0.5)),
            hovertemplate="Events/Tag: %{x:.0f}<br>Dichte: %{y:.6f}<extra></extra>",
            showlegend=False,
        )
    )

    fig.add_vline(
        x=mean,
        line=dict(color="blue", width=2, dash="solid"),
        annotation_text=f"Ø {mean:.0f}",
        annotation_position="top",
    )

    if sigma_choice != "off" and std > 0:
        try:
            n_sigma = int(sigma_choice)
            upper = mean + n_sigma * std
            fig.add_vline(
                x=upper,
                line=dict(color="red", width=2, dash="dash"),
                annotation_text=f"+{n_sigma}σ",
                annotation_position="top",
            )
        except (ValueError, TypeError):
            pass

    if threshold_abs is not None and threshold_abs > 0:
        fig.add_vline(
            x=threshold_abs,
            line=dict(color="orange", width=2, dash="dot"),
            annotation_text=f"Threshold {int(threshold_abs)}",
            annotation_position="top",
        )

    yaxis_type = "log" if scale_mode == "log" else "linear"

    fig.update_layout(
        title="Verteilung der Events pro Tag (Dichte)",
        xaxis_title="Events pro Tag",
        yaxis_title="Dichte" + (" (log)" if scale_mode == "log" else ""),
        yaxis_type=yaxis_type,
        height=320,
        plot_bgcolor="#F0FFF0",
        paper_bgcolor="#F0FFF0",
        font=dict(family="Arial", color="black", size=11),
        margin=dict(l=40, r=20, t=50, b=40),
        showlegend=False,
        bargap=0,
    )
    return fig


@callback(
    Output("stoer-timeline-mini", "figure"),
    Input("date-range-slider", "value"),
    Input("stoer-evttyp-dropdown", "value"),
    Input("stoer-objekt-dropdown", "value"),
    Input("stoer-msr-dropdown", "value"),
    Input("stoer-meldung-dropdown", "value"),
    Input("stoer-prio-dropdown", "value"),
    Input("stoer-ort-dropdown", "value"),
    Input("stoer-zustand-dropdown", "value"),
    Input("stoer-benutzer-dropdown", "value"),
    Input("stoer-threshold-input", "value"),
    Input("stoer-outlier-sigma", "value"),
    Input("stoer-manual-exclude", "value"),
)
def update_timeline(
    slider_value,
    evttyp,
    objekt,
    msr,
    meldung,
    prio,
    ort,
    zustand,
    benutzer,
    threshold_abs,
    sigma_choice,
    manual_excludes,
):
    start_idx, end_idx = slider_value
    start_date = dates[start_idx]
    end_date = dates[end_idx] + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)

    dff = df[(df["Datum"] >= start_date) & (df["Datum"] <= end_date)]
    dff = _apply_filters(dff, evttyp, objekt, msr, meldung, prio, ort, zustand, benutzer)

    if dff.empty:
        fig = go.Figure()
        fig.update_layout(
            height=150,
            plot_bgcolor="#F0FFF0",
            paper_bgcolor="#F0FFF0",
            margin=dict(l=40, r=20, t=20, b=30),
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
        )
        fig.add_annotation(
            text="Keine Daten", x=0.5, y=0.5, xref="paper", yref="paper", showarrow=False
        )
        return fig

    # Pre-calculate normalized dates to avoid repeated .dt.normalize() calls
    normalized_dates = dff["Datum"].dt.normalize()
    daily = normalized_dates.value_counts().reset_index()
    daily.columns = ["Tag", "Anzahl"]
    daily = daily.sort_values("Tag")

    excluded = _get_excluded_days(dff, threshold_abs, sigma_choice, manual_excludes)
    daily["status"] = daily["Tag"].apply(lambda d: "entfernt" if d in excluded else "behalten")

    fig = go.Figure()
    fig.add_trace(
        go.Scattergl(
            x=daily["Tag"],
            y=daily["Anzahl"],
            mode="lines",
            line=dict(color="lightgray", width=1),
            hoverinfo="skip",
            showlegend=False,
        )
    )
    keep = daily[daily["status"] == "behalten"]
    fig.add_trace(
        go.Scattergl(
            x=keep["Tag"],
            y=keep["Anzahl"],
            mode="markers",
            marker=dict(color="#2ca02c", size=6),
            name="behalten",
            hovertemplate="%{x|%Y-%m-%d}<br>Anzahl: %{y}<extra></extra>",
        )
    )
    rem = daily[daily["status"] == "entfernt"]
    if not rem.empty:
        fig.add_trace(
            go.Scattergl(
                x=rem["Tag"],
                y=rem["Anzahl"],
                mode="markers",
                marker=dict(color="red", size=8, symbol="x"),
                name="entfernt",
                hovertemplate="%{x|%Y-%m-%d}<br>Anzahl: %{y}<br>ENTFERNT<extra></extra>",
            )
        )

    fig.update_layout(
        height=180,
        plot_bgcolor="#F0FFF0",
        paper_bgcolor="#F0FFF0",
        font=dict(family="Arial", color="black", size=10),
        margin=dict(l=40, r=20, t=10, b=30),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.0, xanchor="right", x=1.0),
        xaxis=dict(title=""),
        yaxis=dict(title="Events/Tag"),
    )
    return fig


@callback(
    Output("stoermeldungen-bar-chart", "figure"),
    Input("date-range-slider", "value"),
    Input("stoer-evttyp-dropdown", "value"),
    Input("stoer-objekt-dropdown", "value"),
    Input("stoer-msr-dropdown", "value"),
    Input("stoer-meldung-dropdown", "value"),
    Input("stoer-prio-dropdown", "value"),
    Input("stoer-ort-dropdown", "value"),
    Input("stoer-zustand-dropdown", "value"),
    Input("stoer-benutzer-dropdown", "value"),
    Input("stoer-topn-dropdown", "value"),
    Input("stoer-view-toggle", "value"),
    Input("stoer-yaxis-toggle", "value"),
    Input("stoer-threshold-input", "value"),
    Input("stoer-outlier-sigma", "value"),
    Input("stoer-manual-exclude", "value"),
)
def update_bar_chart(
    slider_value,
    evttyp,
    objekt,
    msr,
    meldung,
    prio,
    ort,
    zustand,
    benutzer,
    top_n,
    view_mode,
    y_col,
    threshold_abs,
    sigma_choice,
    manual_excludes,
):
    start_idx, end_idx = slider_value
    start_date = dates[start_idx]
    end_date = dates[end_idx] + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)

    dff = df[(df["Datum"] >= start_date) & (df["Datum"] <= end_date)]
    dff = _apply_filters(dff, evttyp, objekt, msr, meldung, prio, ort, zustand, benutzer)

    excluded = _get_excluded_days(dff, threshold_abs, sigma_choice, manual_excludes)
    if excluded:
        # Use boolean indexing on the original dff instead of
        # .dt.normalize() in the mask if possible
        # but excluded contains Timestamps, so this is already quite efficient.
        dff = dff[~dff["Datum"].dt.normalize().isin(excluded)]

    if dff.empty:
        fig = px.bar(
            pd.DataFrame({y_col: [], "Wert": []}),
            x="Wert",
            y=y_col,
            orientation="h",
            title="Keine Daten im gewählten Zeitraum/Filter",
        )
        fig.update_layout(
            plot_bgcolor="#F0FFF0",
            paper_bgcolor="#F0FFF0",
            font=dict(family="Arial", color="black"),
            showlegend=False,
        )
        return fig

    counts = dff[y_col].value_counts()
    if top_n != "ALL":
        counts = counts.head(int(top_n))
    counts = counts.sort_values(ascending=True)

    plot_df = pd.DataFrame(
        {
            y_col: counts.index.astype(str).tolist(),
            "Anzahl": counts.values.tolist(),
        }
    )

    total = len(dff)
    if view_mode == "prozentual":
        plot_df["Wert"] = (plot_df["Anzahl"] / total * 100).round(2)
        text_values = [f"{v:.2f}%" for v in plot_df["Wert"]]
        x_title = "Anteil (%)"
    else:
        plot_df["Wert"] = plot_df["Anzahl"]
        text_values = [str(int(v)) for v in plot_df["Wert"]]
        x_title = "Anzahl"

    plot_df["text"] = text_values

    n_label = "Alle" if top_n == "ALL" else top_n
    excl_suffix = f" ({len(excluded)} Tage entfernt)" if excluded else ""
    fig = px.bar(
        plot_df,
        x="Wert",
        y=y_col,
        orientation="h",
        color=y_col,
        text="text",
        color_discrete_sequence=px.colors.qualitative.Plotly,
        title=f"Top {n_label} {y_col} im gewählten Zeitraum{excl_suffix}",
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(
        xaxis_title=x_title,
        yaxis_title=y_col,
        plot_bgcolor="#F0FFF0",
        paper_bgcolor="#F0FFF0",
        font=dict(family="Arial", color="black"),
        margin=dict(l=220, r=40, t=60, b=40),
        showlegend=False,
    )

    return fig
