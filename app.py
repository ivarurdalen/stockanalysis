from dash import Dash, dcc, html, dash_table, Input, Output, State, callback_context
import dash
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd
import sqlite3
import talib as ta

app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.ZEPHYR, dbc.icons.FONT_AWESOME],
)

# Markdown text
footer = html.Footer(
    dcc.Markdown(
        """
        App developed with Dash framework (Plotly + Flask + React) by [Ivar Soares Urdalen](https://ivarurdalen.github.io). ![](assets/github.svg)
        """
    ),
    className="p-2 mt-auto bg-light text-center small",
)


# ticker = dbc.InputGroup(
#     [
#         dbc.InputGroupText("Stock Ticker"),
#         dcc.Dropdown(
#             id="ticker",
#             options=["EQNR.OL", "SCATC.OL"],
#             value="EQNR.OL",
#             clearable=False,
#         ),
#     ],
#     className="mb-3",
# )


navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink(page["name"], href=page["path"]))
        for page in dash.page_registry.values()
        # dbc.DropdownMenu(
        #     [
        #         dbc.DropdownMenuItem(page["name"], href=page["path"])
        #         for page in dash.page_registry.values()
        #     ],
        #     nav=True,
        #     label="More Pages",
        # ),
    ],
    brand="Stock Analysis Dashboard",
    color="primary",
    dark=True,
    links_left=True,
    className="mb-2",
)

# Main layout
app.layout = dbc.Container(
    [
        # dbc.Row(
        #     dbc.Col(
        #         html.H2(
        #             "Stock Analysis Dashboard",
        #             className="text-center bg-primary text-white p-2",
        #         ),
        #     )
        # ),
        navbar,
        # dbc.Row(
        #     [
        #         dbc.Col(
        #             [
        #                 input_groups,
        #             ],
        #             width=12,
        #             lg=5,
        #             className="mt-4 border",
        #         ),
        #         dbc.Col(
        #             [dcc.Graph(id="stock_price_chart", className="pb-4")],
        #             width=12,
        #             lg=7,
        #             className="pt-4",
        #         ),
        #     ],
        #     className="ms-4",
        # ),
        dash.page_container,
        dbc.Row(dbc.Col(footer), className="mt-auto"),
    ],
    fluid=True,
    className="d-flex flex-column min-vh-100",
)

if __name__ == "__main__":
    app.run_server(debug=True)
