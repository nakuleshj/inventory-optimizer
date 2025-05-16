import sqlite3
import pandas as pd

conn=sqlite3.connect('../database/inventory.db')

cursor=conn.cursor()

tables={
    'sales':'../data/sales_stream.csv',
    'inventory':'../data/inventory_levels.csv',
    'products':'../data/product_data.csv',
}

for t_name,data_path in tables.items():
    df=pd.read_csv(data_path)
    df.to_sql(t_name,conn,if_exists='replace',index=False)

conn.close()