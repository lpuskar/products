# !/usr/bin/env python3
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '')))

from data_replication_script import replicate_and_transform_customer_data, replicate_and_transform_product_data, \
    replicate_and_transform_order_data
from db.clickhouse_database import clickhouse_engine
from db.database import engine


if __name__ == "__main__":
    print("Starting to replicate and transform data from Postgres to Clickhouse database")
    replicate_and_transform_customer_data(pg_engine=engine, ch_engine=clickhouse_engine)
    replicate_and_transform_product_data(pg_engine=engine, ch_engine=clickhouse_engine)
    replicate_and_transform_order_data(pg_engine=engine, ch_engine=clickhouse_engine)
    print("Data transfer finished")
