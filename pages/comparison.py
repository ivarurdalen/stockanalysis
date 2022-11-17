import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__)

ticker_label = html.H5("Stock ticker:", className="mt-4")
ticker = dcc.Dropdown(
    id="ticker",
    options=["EQNR.OL", "SCATC.OL"],
    value="EQNR.OL",
    clearable=False,
)

index_label = html.H5("Index:", className="mt-4")
index = dcc.Dropdown(
    id="index",
    options=["OBX", "NDX", "SP500"],
    value="OBX",
    clearable=False,
)


input_groups = dbc.Row(
    [
        dbc.Col([ticker_label, ticker]),
        dbc.Col([index_label, index]),
    ],
    className="p-4",
)

layout = dbc.Row(
    [
        dbc.Row(input_groups),
        dbc.Row(dbc.Alert("This Dash page is a work in progress", color="warning")),
    ],
    className="ms-4",
)
