import sqlite3
import pandas as pd

# Load data
con = sqlite3.connect("pages/data/stockanalysis.db")
# df = pd.read_sql_query(
#     "SELECT * from prices", con, index_col="Date", parse_dates=["Date"]
# )
