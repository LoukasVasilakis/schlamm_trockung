import pandas as pd
import dash
from dash import Input, Output, callback
from data_loader import dates


@callback(
    Output("date-range-slider", "value"),
    Output("date-picker-range", "start_date"),
    Output("date-picker-range", "end_date"),
    Input("date-picker-range", "start_date"),
    Input("date-picker-range", "end_date"),
    Input("date-range-slider", "value")
)
def sync_date_controls(start_date, end_date, slider_value):
    trigger = dash.callback_context.triggered_id

    if trigger == "date-picker-range":
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        start_idx = dates.searchsorted(start_date)
        end_idx = dates.searchsorted(end_date)

        start_idx = min(start_idx, len(dates) - 1)
        end_idx = min(end_idx, len(dates) - 1)

        return [start_idx, end_idx], dash.no_update, dash.no_update

    if trigger == "date-range-slider":
        start_idx, end_idx = slider_value
        return dash.no_update, dates[start_idx].date(), dates[end_idx].date()

    return slider_value, start_date, end_date


@callback(
    Output("output-date", "children"),
    Input("date-range-slider", "value")
)
def show_selected_dates(slider_value):
    start_idx, end_idx = slider_value
    return (
        f"Selected range: "
        f"{dates[start_idx].strftime('%Y-%m-%d')} "
        f"to {dates[end_idx].strftime('%Y-%m-%d')}"
    )