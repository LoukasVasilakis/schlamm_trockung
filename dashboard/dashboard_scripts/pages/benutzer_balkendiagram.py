import dash
import pandas as pd
import plotly.graph_objects as go
from dash import callback, dcc, html
from dash.dependencies import Input, Output
from data_loader import dates, df
from plotly.colors import qualitative
from plotly.subplots import make_subplots

dash.register_page(__name__, path="/benutzer-balkendiagram", name="Benutzer-Übersicht")


def get_event_type_options(source_df):
    event_types = sorted(source_df["evtTyp"].dropna().astype(str).unique())

    return [{"label": "All", "value": "ALL"}] + [
        {"label": evt_type, "value": evt_type} for evt_type in event_types
    ]


def build_user_color_map(source_df):
    users = source_df["Benutzer"].fillna("NaN").astype(str).unique().tolist()
    users = sorted(users)

    palette = (
        qualitative.Plotly
        + qualitative.Safe
        + qualitative.Set3
        + qualitative.Dark24
        + qualitative.Light24
    )

    color_map = {}
    for i, user in enumerate(users):
        color_map[user] = palette[i % len(palette)]

    return color_map


def add_bar_trace(fig, series, row, col, color_map, is_percent=False):
    axis_number = (row - 1) * 2 + col
    xref = "x domain" if axis_number == 1 else f"x{axis_number} domain"
    yref = "y domain" if axis_number == 1 else f"y{axis_number} domain"

    if series.empty:
        fig.add_annotation(
            x=0.5,
            y=0.5,
            xref=xref,
            yref=yref,
            text="Keine Daten",
            showarrow=False,
            font=dict(family="Arial", size=12, color="black"),
        )
        return

    plot_df = pd.DataFrame(
        {"Benutzer": series.index.astype(str), "Wert": series.values}
    ).sort_values("Wert", ascending=True)

    text_values = (
        [f"{val:.1f}%" for val in plot_df["Wert"]]
        if is_percent
        else [str(int(val)) for val in plot_df["Wert"]]
    )

    fig.add_trace(
        go.Bar(
            x=plot_df["Wert"],
            y=plot_df["Benutzer"],
            orientation="h",
            marker_color=[color_map.get(user, "#636EFA") for user in plot_df["Benutzer"]],
            text=text_values,
            textposition="outside",
            cliponaxis=False,
            hovertemplate=(
                "Benutzer: %{y}<br>Anteil: %{x:.1f}%<extra></extra>"
                if is_percent
                else "Benutzer: %{y}<br>Anzahl Events: %{x}<extra></extra>"
            ),
            showlegend=False,
        ),
        row=row,
        col=col,
    )


layout = html.Div(
    [
        html.H2(
            "Benutzer-Übersicht",
            style={"fontFamily": "Arial", "textAlign": "center"},
        ),
        html.Div(
            [
                html.Label(
                    "Filter evtTyp",
                    style={
                        "fontFamily": "Arial",
                        "display": "block",
                        "marginBottom": "5px",
                    },
                ),
                dcc.Dropdown(
                    id="balkendiagram-evttyp-dropdown",
                    options=get_event_type_options(df),
                    value="ALL",
                    clearable=False,
                    style={"fontFamily": "Arial", "width": "300px"},
                ),
            ],
            style={"marginBottom": "15px"},
        ),
        dcc.Graph(id="benutzer-balkendiagram", config={"displayModeBar": False}),
    ]
)


@callback(
    Output("benutzer-balkendiagram", "figure"),
    Input("date-range-slider", "value"),
    Input("balkendiagram-evttyp-dropdown", "value"),
)
def update_user_overview(slider_value, selected_evttyp):
    start_idx, end_idx = slider_value

    start_date = dates[start_idx]
    end_date = dates[end_idx] + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)

    dff = df[(df["Datum"] >= start_date) & (df["Datum"] <= end_date)].copy()

    if selected_evttyp not in [None, "ALL"]:
        dff = dff[dff["evtTyp"] == selected_evttyp].copy()

    if dff.empty:
        fig = go.Figure()
        fig.update_layout(
            title="Keine Benutzerdaten im gewählten Zeitraum",
            plot_bgcolor="#F0FFF0",
            paper_bgcolor="#F0FFF0",
            font=dict(family="Arial", color="black"),
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
        )
        fig.add_annotation(
            text="Keine Benutzerdaten im gewählten Zeitraum",
            x=0.5,
            y=0.5,
            xref="paper",
            yref="paper",
            showarrow=False,
            font=dict(family="Arial", size=14, color="black"),
        )
        return fig

    color_map = build_user_color_map(df)

    user_counts_all = dff["Benutzer"].fillna("NaN").astype(str).value_counts()
    user_pct_all = (
        (user_counts_all / user_counts_all.sum() * 100).round(1)
        if not user_counts_all.empty
        else pd.Series(dtype=float)
    )

    dff_no_nan_auto = dff[(dff["Benutzer"].notna()) & (~dff["Benutzer"].isin(["AUTO"]))].copy()

    user_counts_no_nan_auto = dff_no_nan_auto["Benutzer"].astype(str).value_counts()
    user_pct_no_nan_auto = (
        (user_counts_no_nan_auto / user_counts_no_nan_auto.sum() * 100).round(1)
        if not user_counts_no_nan_auto.empty
        else pd.Series(dtype=float)
    )

    fig = make_subplots(
        rows=2,
        cols=2,
        horizontal_spacing=0.18,
        vertical_spacing=0.22,
    )

    add_bar_trace(fig, user_counts_all, 1, 1, color_map, is_percent=False)
    add_bar_trace(fig, user_pct_all, 1, 2, color_map, is_percent=True)
    add_bar_trace(fig, user_counts_no_nan_auto, 2, 1, color_map, is_percent=False)
    add_bar_trace(fig, user_pct_no_nan_auto, 2, 2, color_map, is_percent=True)

    fig.add_annotation(
        x=0.24,
        y=1.10,
        xref="paper",
        yref="paper",
        text="<b>absolut</b>",
        showarrow=False,
        font=dict(family="Arial", size=16, color="black"),
    )

    fig.add_annotation(
        x=0.76,
        y=1.10,
        xref="paper",
        yref="paper",
        text="<b>prozentual</b>",
        showarrow=False,
        font=dict(family="Arial", size=16, color="black"),
    )

    fig.add_annotation(
        x=0.5,
        y=0.43,
        xref="paper",
        yref="paper",
        text="<b>Benutzer (Ohne NaN, AUTO)</b>",
        showarrow=False,
        font=dict(family="Arial", size=14, color="black"),
    )

    fig.update_xaxes(title_text="Anzahl Events", row=1, col=1)
    fig.update_xaxes(title_text="Anteil (%)", row=1, col=2)
    fig.update_xaxes(title_text="Anzahl Events", row=2, col=1)
    fig.update_xaxes(title_text="Anteil (%)", row=2, col=2)

    fig.update_yaxes(title_text="Benutzer", row=1, col=1)
    fig.update_yaxes(title_text="Benutzer", row=2, col=1)

    fig.update_yaxes(title_text="", row=1, col=2)
    fig.update_yaxes(title_text="", row=2, col=2)

    title_suffix = f" – evtTyp: {selected_evttyp}" if selected_evttyp not in [None, "ALL"] else ""

    fig.update_layout(
        title=f"Benutzer-Übersicht – Anzahl Events pro Benutzer{title_suffix}",
        height=850,
        plot_bgcolor="#F0FFF0",
        paper_bgcolor="#F0FFF0",
        font=dict(family="Arial", color="black"),
        margin=dict(l=170, r=80, t=170, b=50),
        bargap=0.2,
    )

    return fig
