from dash import Dash, dcc, html, dash_table, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd
import sqlite3
import talib as ta

app = Dash(__name__, external_stylesheets=[dbc.themes.ZEPHYR, dbc.icons.FONT_AWESOME])

# Load data
con = sqlite3.connect("data/stockanalysis.db")
df = pd.read_sql_query(
    "SELECT * from prices", con, index_col="Date", parse_dates=["Date"]
)

# Markdown text
footer = html.Footer(
    dcc.Markdown(
        """
        App developed with Dash framework (Plotly + Flask + React) by Ivar Soares Urdalen.
        """
    ),
    className="p-2 mt-auto bg-light text-center small",
)

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
        for index, row in df.iterrows()
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

ticker_label = html.H5("Stock ticker:", className="mt-4")
ticker = dcc.Dropdown(
    id="ticker",
    options=["EQNR.OL", "SCATC.OL"],
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


input_groups = html.Div(
    [ticker_label, ticker, range_label, range],
    className="p-4",
)

# Main layout
app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H2(
                    "Stock Analysis Dashboard",
                    className="text-center bg-primary text-white p-2",
                ),
            )
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        input_groups,
                    ],
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
            ],
            className="ms-4",
        ),
        dbc.Row(dbc.Col(footer), className="mt-auto"),
    ],
    fluid=True,
    className="d-flex flex-column min-vh-100",
)

# Callbacks
@app.callback(
    Output("stock_price_chart", "figure"),
    Input("ticker", "value"),
    Input("range", "value"),
)
def update_chart(ticker, range):
    # Set defaults for invalid inputs
    ticker = "EQNR.OL" if ticker is None else ticker

    # Filter on ticker and remove ticker column
    dff = df[df["ticker"] == ticker].iloc[:, 1:]
    dff["20SMA"] = ta.SMA(dff["Close"], 20)
    dff["50SMA"] = ta.SMA(dff["Close"], 50)
    dff["100SMA"] = ta.SMA(dff["Close"], 100)

    dff["RSI"] = ta.RSI(dff["Close"], 14)

    dff = dff.iloc[-range:, :]
    # Creat stock price chart
    fig = make_chart(dff)

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
