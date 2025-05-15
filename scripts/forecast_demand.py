import numpy as np
import pandas as pd
import sqlite3
from prophet import Prophet
import matplotlib.pyplot as plt

conn=sqlite3.connect('../database/inventory.db')
daily_volume=pd.read_sql('SELECT timestamp as ds,product_id,SUM(units_sold) as y FROM sales GROUP BY timestamp, product_id',conn)
conn.close()

#converting to time-series data

daily_volume['ds']=pd.to_datetime(daily_volume['ds'])
#daily_volume.set_index('ds',inplace=True)

prophet_model=Prophet()
prophet_model.fit(daily_volume)

predictions=prophet_model.make_future_dataframe(periods=30)

forecast = prophet_model.predict(predictions)

prophet_model.plot(forecast)
plt.show()