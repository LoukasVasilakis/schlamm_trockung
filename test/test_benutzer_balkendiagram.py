def test_update_user_overview_returns_empty_figure_when_no_data_for_filter(
    fake_dashboard_data, pages_dir, monkeypatch
):
    df, dates = fake_dashboard_data

    module = __import__(
        "test.conftest", fromlist=["load_module_with_fake_data"]
    ).load_module_with_fake_data(
        pages_dir / "benutzer_balkendiagram.py",
        "benutzer_test_module_empty",
        df,
        dates,
        monkeypatch,
    )

    # Last date only has evtTyp "Warnungen", so filtering to "Störmeldungen" should yield empty
    slider_value = [3, 3]
    fig = module.update_user_overview(slider_value, "Störmeldungen")

    assert "Keine Benutzerdaten" in fig.layout.title.text
    assert fig.layout.font.family == "Arial"
    assert fig.layout.plot_bgcolor == "#F0FFF0"


def test_update_user_overview_returns_four_traces(fake_dashboard_data, pages_dir, monkeypatch):
    df, dates = fake_dashboard_data

    module = __import__(
        "test.conftest", fromlist=["load_module_with_fake_data"]
    ).load_module_with_fake_data(
        pages_dir / "benutzer_balkendiagram.py",
        "benutzer_test_module_traces",
        df,
        dates,
        monkeypatch,
    )

    slider_value = [0, len(dates) - 1]
    fig = module.update_user_overview(slider_value, "ALL")

    # 2x2 subplot setup -> 4 bar traces
    assert len(fig.data) == 4
    assert fig.layout.font.family == "Arial"
    assert fig.layout.paper_bgcolor == "#F0FFF0"


def test_update_user_overview_excludes_auto_and_nan_in_second_row(
    fake_dashboard_data, pages_dir, monkeypatch
):
    df, dates = fake_dashboard_data

    module = __import__(
        "test.conftest", fromlist=["load_module_with_fake_data"]
    ).load_module_with_fake_data(
        pages_dir / "benutzer_balkendiagram.py",
        "benutzer_test_module_filtering",
        df,
        dates,
        monkeypatch,
    )

    slider_value = [0, len(dates) - 1]
    fig = module.update_user_overview(slider_value, "ALL")

    # Trace order:
    # 0 = all users absolute
    # 1 = all users percent
    # 2 = no NaN / AUTO absolute
    # 3 = no NaN / AUTO percent

    second_row_absolute = fig.data[2]
    second_row_percent = fig.data[3]

    abs_users = list(second_row_absolute.y)
    pct_users = list(second_row_percent.y)

    assert "AUTO" not in abs_users
    assert "AUTO" not in pct_users
    assert "NaN" not in abs_users
    assert "NaN" not in pct_users

    # remaining expected users
    assert set(abs_users) == {"Alice", "Bob", "Charlie"}


def test_update_user_overview_evttyp_filter_changes_title(
    fake_dashboard_data, pages_dir, monkeypatch
):
    df, dates = fake_dashboard_data

    module = __import__(
        "test.conftest", fromlist=["load_module_with_fake_data"]
    ).load_module_with_fake_data(
        pages_dir / "benutzer_balkendiagram.py",
        "benutzer_test_module_title",
        df,
        dates,
        monkeypatch,
    )

    slider_value = [0, len(dates) - 1]
    fig = module.update_user_overview(slider_value, "Störmeldungen")

    assert "evtTyp: Störmeldungen" in fig.layout.title.text
