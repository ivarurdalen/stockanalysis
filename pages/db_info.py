from dash import dcc, callback, html, Input, Output
import dash
import dash_bootstrap_components as dbc
import pandas as pd
import sqlite3


dash.register_page(__name__, path="/db_info", title="Database", name="Database")


def make_summary_table(db_info):
    """Make html table to show cagr and  best and worst periods"""

    table_class = "text-body text-nowrap"
    nr_tickers = html.Span(["Number of tickers: "], className=table_class)
    nr_rows_prices = html.Span(
        ["Number of rows in prices table: "], className=table_class
    )
    first_date_prices = html.Span(
        ["First date in prices table:"], className=table_class
    )
    last_date_prices = html.Span(["Last date in prices table:"], className=table_class)
    nr_rows_single_ticker = html.Span(
        ["Number of rows for single ticker: "], className=table_class
    )

    df_table = pd.DataFrame(
        {
            "Parameter": [
                nr_tickers,
                nr_rows_prices,
                first_date_prices,
                last_date_prices,
                nr_rows_single_ticker,
            ],
            "Value": [
                db_info["nr_tickers"],
                db_info["nr_rows_prices"],
                db_info["first_date_prices"],
                db_info["last_date_prices"],
                db_info["nr_rows_single_ticker"],
            ],
        }
    )
    return dbc.Table.from_dataframe(df_table, bordered=True, hover=True)


layout = dbc.Col(
    children=[
        dbc.Row(
            [
                dbc.Button(
                    "Get database info",
                    id="btn-update",
                    color="primary",
                    className="me-1",
                    n_clicks=0,
                )
            ],
            className="d-grid col-6 ps-3",
        ),
        dbc.Row(html.Div(id="summary_table"), className="pt-4"),
    ],
    width=6,
    lg=3,
    className="pt-4",
)


@callback(Output("summary_table", "children"), Input("btn-update", "n_clicks"))
def update_db_info(n_clicks):
    con = sqlite3.connect("pages/data/stockanalysis.db")
    cursor = con.cursor()

    ticker = "EQNR.OL"
    ticker_prices = pd.read_sql_query(
        f"SELECT * FROM prices WHERE ticker='{ticker}'",
        con,
        index_col="Date",
        parse_dates=["Date"],
    )
    ticker_prices.index.rename("Date", inplace=True)
    nr_tickers = cursor.execute("SELECT COUNT(*) FROM tickers").fetchone()[0]
    nr_rows_tickers = cursor.execute("SELECT COUNT(*) FROM prices").fetchone()[0]

    db_info = {
        "nr_tickers": nr_tickers,
        "nr_rows_prices": nr_rows_tickers,
        "first_date_prices": ticker_prices.first("1D").index[0].strftime("%Y-%m-%d"),
        "last_date_prices": ticker_prices.last("1D").index[0].strftime("%Y-%m-%d"),
        "nr_rows_single_ticker": len(ticker_prices.index),
    }

    return make_summary_table(db_info)
