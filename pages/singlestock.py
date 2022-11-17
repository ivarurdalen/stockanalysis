import dash
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import talib as ta
import pandas as pd
import sqlite3
import numpy as np

# from .database import con

dash.register_page(__name__, path="/", name="Single Stock")

# Figures
def make_chart(dff):
    # fig = go.Figure()
    # add subplot properties when initializing fig variable ***don't forget to import plotly!!!***
    fig = make_subplots(
        rows=3,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.01,
        row_heights=[0.6, 0.2, 0.2],
        # row_width=[0.5, 0.1, 0.2, 0.2],
    )

    fig.add_trace(
        go.Candlestick(
            x=dff.index,
            open=dff["Open"],
            high=dff["High"],
            low=dff["Low"],
            close=dff["Close"],
            name="Stock price",
            # marker_color="blue",
            # line=dict(width=6, dash="dot"),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=dff.index,
            y=dff["20SMA"],
            opacity=0.7,
            line=dict(color="blue", width=2),
            name="20 SMA",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=dff.index,
            y=dff["50SMA"],
            opacity=0.7,
            line=dict(color="orange", width=2),
            name="50 SMA",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=dff.index,
            y=dff["100SMA"],
            opacity=0.7,
            line=dict(color="red", width=2),
            name="100 SMA",
        )
    )

    # Plot volume trace on 2nd row in our figure
    colors = [
        "green" if row["Open"] - row["Close"] >= 0 else "red"
        for index, row in dff.iterrows()
    ]
    fig.add_trace(
        go.Bar(x=dff.index, y=dff["Volume"], marker_color=colors, name="Volume"),
        row=2,
        col=1,
    )

    # RSI
    fig.add_trace(
        go.Scatter(
            x=dff.index,
            y=dff["RSI"],
            opacity=0.7,
            line=dict(color="blue", width=2),
            name="RSI",
        ),
        row=3,
        col=1,
    )
    fig.add_hline(
        y=20, line_width=1, line_dash="dash", line_color="black", row=3, col=1
    )
    fig.add_hline(
        y=80, line_width=1, line_dash="dash", line_color="black", row=3, col=1
    )
    fig.add_hline(y=50, line_width=1, line_dash="dash", line_color="grey", row=3, col=1)
    fig.add_hrect(
        y0=80, y1=100, line_width=0, fillcolor="red", opacity=0.2, row=3, col=1
    )
    fig.add_hrect(
        y0=0, y1=20, line_width=0, fillcolor="green", opacity=0.2, row=3, col=1
    )

    fig.update_layout(
        title="Stock price",
        template="none",
        showlegend=True,
        legend=dict(x=0.01, y=0.99),
        height=800,
        margin=dict(l=40, r=10, t=60, b=55),
        # yaxis=dict(tickprefix="NOK", fixedrange=True),
        # yaxis_title="Stock Price",
        # yaxis=dict(tickprefix="NOK"),
        yaxis=dict(autorange=True, fixedrange=False),
        # xaxis=dict(title="Date", fixedrange=True),
        xaxis=dict(
            rangeselector=dict(
                buttons=list(
                    [
                        dict(count=7, label="7d", step="day", stepmode="backward"),
                        dict(count=1, label="1m", step="month", stepmode="backward"),
                        dict(count=1, label="MTD", step="month", stepmode="todate"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(count=1, label="YTD", step="year", stepmode="todate"),
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(step="all"),
                    ]
                )
            ),
            rangeslider=dict(visible=True),
            type="date",
        ),
        xaxis_rangeslider_visible=False,
        xaxis3_rangeslider_visible=True,
        xaxis3_rangeslider_thickness=0.1,
    )

    fig.update_xaxes(
        rangebreaks=[
            dict(bounds=["sat", "mon"]),  # hide weekends
            # dict(values=["2015-12-25", "2016-01-01"])  # hide Christmas and New Year's
        ]
    )
    fig.update_yaxes(range=[0, 100], row=3, col=1)

    return fig


def make_return_distribution(dff):
    fig = go.Figure()
    fig.add_trace(
        go.Histogram(
            x=dff["log_returns"],
            name="Log returns",
            marker_line=dict(width=1, color="black"),
        )
    )
    # fig.add_trace(
    #     go.Histogram(
    #         x=dff["returns"],
    #         name="Returns",
    #         marker_line=dict(width=1, color="black"),
    #     )
    # )

    fig.update_layout(
        title="Log return distribution",
        template="none",
        showlegend=True,
        legend=dict(x=0.01, y=0.99),
        height=400,
        margin=dict(l=40, r=10, t=60, b=55),
        bargap=0.2,
        barmode="overlay",
    )

    fig.update_traces(opacity=0.5, xbins_size=0.01)
    fig.update_xaxes(tickangle=45, dtick=0.01)

    return fig


tickers = pd.read_csv(
    "pages/data/tickers/oslo_tickers.csv", header=None, names=["ticker"]
)
tickers = tickers["ticker"].tolist()
ticker_label = html.H5("Stock ticker:", className="mt-4")
ticker = dcc.Dropdown(
    id="ticker",
    options=tickers,
    value="EQNR.OL",
    clearable=False,
)

range_label = html.H5("Range in days:", className="mt-4")
range = dcc.Dropdown(
    id="range",
    options=[365, 180, 30, 7],
    value=365,
    clearable=False,
)


input_groups = dbc.Row(
    [
        dbc.Col([ticker_label, ticker]),
        dbc.Col([range_label, range]),
    ],
    className="p-4",
)

layout = dbc.Row(
    [
        dbc.Row(input_groups),
        dbc.Row(
            [
                dbc.Col(
                    [dcc.Graph(id="return_distribution", className="pb-4")],
                    width=12,
                    lg=5,
                    className="mt-4 border",
                ),
                dbc.Col(
                    [dcc.Graph(id="stock_price_chart", className="pb-4")],
                    width=12,
                    lg=7,
                    className="pt-4",
                ),
            ]
        ),
    ],
    className="ms-4",
)

# Callbacks
@callback(
    Output("stock_price_chart", "figure"),
    Output("return_distribution", "figure"),
    Input("ticker", "value"),
    Input("range", "value"),
)
def update_chart(ticker, range):
    # Set defaults for invalid inputs
    ticker = "EQNR.OL" if ticker is None else ticker

    con = sqlite3.connect("pages/data/stockanalysis.db")

    df = pd.read_sql_query(
        f"SELECT * from prices WHERE ticker='{ticker}'",
        con,
        index_col="Date",
        parse_dates=["Date"],
    )

    # con.close()

    # Filter on ticker and remove ticker column
    dff = df.iloc[:, 1:]
    dff["20SMA"] = ta.SMA(dff["Close"], 20)
    dff["50SMA"] = ta.SMA(dff["Close"], 50)
    dff["100SMA"] = ta.SMA(dff["Close"], 100)

    dff["RSI"] = ta.RSI(dff["Close"], 14)

    dff = dff.iloc[-range:, :]
    # Creat stock price chart
    fig = make_chart(dff)

    dff["log_returns"] = np.log(dff["Close"]) - np.log(dff["Close"].shift(1))
    dff["returns"] = dff["Close"].pct_change()
    fig_ret = make_return_distribution(dff)

    return fig, fig_ret
