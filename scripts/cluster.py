import pandas as pd
import sqlite3
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

conn=sqlite3.connect('../data/inevntory.db')
forecasted_demand=pd.read_sql('SELECT * FROM forecasts',conn)
conn.close()

forecasted_demand_pivot=pd.pivot_table(
    forecasted_demand,
    index=['product_id','ds'],
)

print(forecasted_demand.head())