# Database-Final-Project
Implementing applications with PostgreSQL DBMS and Python3.

## Prerequisites
You shall download some necessary packages before you run these code. Packages needed can be download using:

```shell
$ pip3 install -r requirements.txt
```

## Download datasets
The data used for this project is from [TLC Trip Record Data](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page).

The dataset I chose includes Yellow Taxi Trip Records from January, 2022 to March, 2022.
You can download the datasets with the link below and save them to the directory "[raw_data](https://github.com/Lucas-Kuo/Database-Final-Project/tree/main/raw_data)":
| Month    | download link (.parquet file)   |
|----------|------------------------|
| Jan | [link](https://nyc-tlc.s3.amazonaws.com/trip+data/yellow_tripdata_2022-01.parquet)                    |
| Fab | [link](https://nyc-tlc.s3.amazonaws.com/trip+data/yellow_tripdata_2022-02.parquet)                    |
| Mar | [link](https://nyc-tlc.s3.amazonaws.com/trip+data/yellow_tripdata_2022-03.parquet)                    |


Alternatively, if you are running on Linux-based, the following shell script can do the same thing automatically when bash interpreter is available:
```shell
$ cd ./raw_data
$ bash ./download_data.sh
$ cd ~
```

Either way, make sure you have the following file structure in the repository before going on:
```
.
├── raw_data
│   ├── yellow_tripdata_2022-01.parquet
│   ├── yellow_tripdata_2022-02.parquet
│   └── yellow_tripdata_2022-03.parquet
├── requirements.txt
├── README.md
└── other python files
```

## Parquet File Conversion & Creating Tables
Since we're dealing with parquet files, we need to convert them into files that SQL databases support. In Python, I decided to read in parquet files with [pyarrow](https://arrow.apache.org/docs/python/index.html) package and convert them into [Pandas Dataframes](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html). With the dataframes, it can be written into any SQL database with built-in function.

To do so, just run the following command:
```
python3 build_database.py
```

