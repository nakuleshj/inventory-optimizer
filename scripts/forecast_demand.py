import numpy as np
import pandas as pd
import sqlite3
from prophet import Prophet
import matplotlib.pyplot as plt
import logging
from tqdm import tqdm

logger = logging.getLogger('cmdstanpy')
logger.setLevel(logging.ERROR)
logger.addHandler(logging.NullHandler())

def forecaster(df):
    prophet_model=Prophet()
    prophet_model.fit(df)
    predictions_ds=prophet_model.make_future_dataframe(periods=60)
    forecast = prophet_model.predict(predictions_ds)
    forecast=forecast[forecast['ds'].isin(df['ds'].values)==False]
    print(forecast.shape[0])
    forecast['yhat']=forecast['yhat'].astype(int)
    forecast_dict={'y':forecast['yhat'].values,'ds':forecast['ds'].values}
    return forecast_dict

conn=sqlite3.connect('../database/inventory.db')
sales_data=pd.read_sql('SELECT timestamp as ds,product_id,SUM(units_sold) as y FROM sales GROUP BY timestamp, product_id',conn)
conn.close()

#converting to time-series data

sales_data['ds']=pd.to_datetime(sales_data['ds'])
sales_data.dropna(inplace=True)
product_ids=sales_data['product_id'].unique()

for pid in product_ids:
    if len(sales_data[sales_data['product_id']==pid]) >=2:
        forecasted_values=pd.DataFrame(forecaster(sales_data[sales_data['product_id']==pid]))
        forecasted_values['product_id']=pid