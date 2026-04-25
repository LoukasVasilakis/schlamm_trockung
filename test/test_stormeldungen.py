import pandas as pd

from dashboard.dashboard_scripts.charts.stormeldungen_chart import update_bar_chart


def test_update_bar_chart_returns_figure():
    test_df = pd.DataFrame(
        {
            "datum": ["2024-01-01", "2024-01-02"],
            "anzahl_stoermeldungen": [3, 5],
        }
    )

    fig = update_bar_chart([0, 1], test_df)

    assert fig is not None
    assert hasattr(fig, "data")
    assert hasattr(fig, "layout")