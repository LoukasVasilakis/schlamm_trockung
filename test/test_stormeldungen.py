import pandas as pd
import plotly.express as px


def update_bar_chart(slider_value, df, dates):
    start_idx, end_idx = slider_value

    start_date = dates[start_idx]
    end_date = dates[end_idx] + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)

    dff = df[
        (df["Datum"] >= start_date) & (df["Datum"] <= end_date) & (df["evtTyp"] == "Störmeldungen")
    ].copy()

    dff = dff[dff["Meldung"].str.strip() != ""].copy()

    if dff.empty:
        fig = px.bar(x=[], y=[], orientation="h", title="Keine Störmeldungen im gewählten Zeitraum")
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

    fig.update_traces(textposition="outside")

    fig.update_layout(
        xaxis_title="Anzahl",
        yaxis_title="Störmeldung",
        plot_bgcolor="#F0FFF0",
        paper_bgcolor="#F0FFF0",
        font=dict(family="Arial", color="black"),
        margin=dict(l=220, r=40, t=60, b=40),
    )

    return fig


def test_update_bar_chart_returns_figure():
    dates = pd.to_datetime(["2024-01-01", "2024-01-02"])

    df = pd.DataFrame(
        {
            "Datum": pd.to_datetime(
                [
                    "2024-01-01 10:00:00",
                    "2024-01-01 11:00:00",
                    "2024-01-02 12:00:00",
                    "2024-01-02 13:00:00",
                ]
            ),
            "evtTyp": [
                "Störmeldungen",
                "Störmeldungen",
                "Störmeldungen",
                "Andere Meldung",
            ],
            "Meldung": [
                "Fehler A",
                "Fehler A",
                "Fehler B",
                "Fehler C",
            ],
        }
    )

    fig = update_bar_chart([0, 1], df, dates)

    assert fig is not None
    assert hasattr(fig, "data")
    assert hasattr(fig, "layout")
    assert fig.layout.title.text == "Top 10 Störmeldungen im gewählten Zeitraum"
