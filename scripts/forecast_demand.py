import numpy as np
import pandas as pd
import sqlite3

conn=sqlite3.connect('../database/inventory.db')
daily_volume=pd.read_sql('SELECT timestamp,product_id,SUM(units_sold) as daily_volume FROM sales GROUP BY timestamp, product_id',conn)
conn.close()

#converting to time-series data

daily_volume['timestamp']=pd.to_datetime(daily_volume['timestamp'])
daily_volume.set_index('timestamp',inplace=True)

if daily_volume.isnull().sum() > 0:
    daily_volume.dropna()