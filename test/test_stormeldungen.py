import pytest
from dashboard.dashboard_scripts.pages.stoermeldungen import update_bar_chart


def test_update_bar_chart_returns_figure():
    # einfacher Dummy-Slider-Wert (Start=0, Ende=1)
    slider_value = [0, 1]

    fig = update_bar_chart(slider_value)

    # Prüfen, ob überhaupt etwas zurückkommt
    assert fig is not None

    # Prüfen, ob es eine Plotly Figure ist
    assert hasattr(fig, "data")
    assert hasattr(fig, "layout")