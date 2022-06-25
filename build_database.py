import pandas as pd
import sqlalchemy
import secret
import pyarrow.parquet as pq

# loading secrets
username = secret.USER
pwd = secret.PASSWORD
url = secret.URL
db = secret.DB_NAME

months = ["1", "2", "3"]

engine = sqlalchemy.create_engine(f"postgresql://{username}:{pwd}@{url}:5432/{db}")

for month in months:
    data_path = f"./raw_data/yellow_tripdata_2022-0{month}.parquet"
    table = pq.read_table(data_path)
    df = table.to_pandas()
    df.columns = [c.lower() for c in df.columns] # PostgreSQL deprecates upper-case column names
    
    if month=="1":
        df.to_sql("Jan_2022", engine, index=False)
    elif month=="2":
        df.to_sql("Fab_2022", engine, index=False)
    elif month=="3":
        df.to_sql("Mar_2022", engine, index=False)
    else:
        pass
