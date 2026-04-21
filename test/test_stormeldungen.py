import pandas as pd


def test_update_bar_chart_returns_empty_figure_when_no_stoermeldungen(
    fake_dashboard_data, pages_dir, monkeypatch
):
    df, dates = fake_dashboard_data

    module = __import__(
        "test.conftest", fromlist=["load_module_with_fake_data"]
    ).load_module_with_fake_data(
        pages_dir / "stormeldungen.py", "stormeldungen_test_module_empty", df, dates, monkeypatch
    )

    # Choose only the last day (2024-01-04), which has no evtTyp == "Störmeldungen"
    slider_value = [3, 3]
    fig = module.update_bar_chart(slider_value)

    assert "Keine Störmeldungen" in fig.layout.title.text
    assert fig.layout.font.family == "Arial"
    assert fig.layout.plot_bgcolor == "#F0FFF0"


def test_update_bar_chart_counts_top_messages_correctly(
    fake_dashboard_data, pages_dir, monkeypatch
):
    df, dates = fake_dashboard_data

    module = __import__(
        "test.conftest", fromlist=["load_module_with_fake_data"]
    ).load_module_with_fake_data(
        pages_dir / "stormeldungen.py", "stormeldungen_test_module_counts", df, dates, monkeypatch
    )

    # Full range
    slider_value = [0, len(dates) - 1]
    fig = module.update_bar_chart(slider_value)

    assert len(fig.data) == 1
    trace = fig.data[0]

    # We expect only non-empty Meldung rows where evtTyp == "Störmeldungen"
    # Counts:
    # "Pumpe Fehler" -> 2
    # "Sensor Alarm" -> 1
    # "Motor Störung" -> 1
    x_values = list(trace.x)
    y_values = list(trace.y)

    assert set(y_values) == {"Pumpe Fehler", "Sensor Alarm", "Motor Störung"}
    assert sorted(x_values) == [1, 1, 2]


def test_update_bar_chart_filters_by_date_range(fake_dashboard_data, pages_dir, monkeypatch):
    df, dates = fake_dashboard_data

    module = __import__(
        "test.conftest", fromlist=["load_module_with_fake_data"]
    ).load_module_with_fake_data(
        pages_dir / "stormeldungen.py",
        "stormeldungen_test_module_datefilter",
        df,
        dates,
        monkeypatch,
    )

    # Only first date: 2024-01-01
    slider_value = [0, 0]
    fig = module.update_bar_chart(slider_value)

    assert len(fig.data) == 1
    trace = fig.data[0]

    assert list(trace.y) == ["Pumpe Fehler"]
    assert list(trace.x) == [2]
