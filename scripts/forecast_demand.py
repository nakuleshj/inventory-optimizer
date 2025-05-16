import numpy as np
import pandas as pd
import sqlite3
from prophet import Prophet
from prophet.serialize import model_to_json, model_from_json
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
    forecast['yhat']=forecast['yhat'].astype(int)
    forecast_dict={'y':forecast['yhat'].values,'ds':forecast['ds'].values}
    return forecast_dict

conn=sqlite3.connect('../database/inventory.db')
sales_data=pd.read_sql('SELECT timestamp as ds,product_id,SUM(units_sold) as y FROM sales GROUP BY timestamp, product_id',conn)
conn.close()

sales_data['ds']=pd.to_datetime(sales_data['ds'])
sales_data.dropna(inplace=True)
product_ids=sales_data['product_id'].unique()
print(len(product_ids))
forecasted_demand=pd.DataFrame()
print('OG Count ',len(sales_data))
count=0
for pid in tqdm(product_ids):
    if len(sales_data[sales_data['product_id']==pid]) >=2:
        count=count+1
        forecasted_values=pd.DataFrame(forecaster(sales_data[sales_data['product_id']==pid]))
        forecasted_values['product_id']=pid
        forecasted_demand=pd.concat([forecasted_demand,forecasted_values])

print(count)
print("Count should be: ",count*60)
print('New Count ',len(forecasted_demand))

def store_forecasts(forecasts):
    conn=sqlite3.connect('../database/inventory.db')
    forecasts.to_sql(
        'forecasts',conn,if_exists='replace',index=False
    )
    conn.close()

