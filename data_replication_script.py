import datetime
import logging

import pandas as pd


def replicate_and_transform_customer_data(pg_engine, ch_engine):
    logging.info('Starting replicate_and_transform_customer_data')
    last_processed_timestamp_file = 'logs/last_processed_timestamp_customer_data.txt'

    try:
        with open(last_processed_timestamp_file, 'r') as file:
            last_processed_timestamp_str = file.read().strip()
            last_processed_timestamp = datetime.datetime.fromisoformat(last_processed_timestamp_str)
    except (FileNotFoundError, ValueError) as e:
        logging.error(f'Could not find file {last_processed_timestamp_file}')
        raise e

    last_processed_timestamp_str = str(last_processed_timestamp)
    current_timestamp = datetime.datetime.utcnow()

    query = f"""
        SELECT *
        FROM customer
        WHERE row_inserted_at > '{last_processed_timestamp_str}'
    """

    with pg_engine.connect() as conn, conn.begin():
        df_customers = pd.read_sql(query, conn)

    if 'row_inserted_at' in df_customers.columns:
        df_customers = df_customers.drop(columns=['row_inserted_at'])
    if 'id' in df_customers.columns:
        df_customers = df_customers.drop(columns=['id'])

    if not df_customers.empty:
        with open(last_processed_timestamp_file, 'w') as file:
            file.write(current_timestamp.isoformat())

    df_customers.to_sql('DimCustomer', ch_engine, if_exists='append', index=False)




def replicate_and_transform_product_data(pg_engine, ch_engine):
    logging.info('Starting replicate_and_transform_product_data')
    last_processed_timestamp_file = 'logs/last_processed_timestamp_product_data.txt'

    try:
        with open(last_processed_timestamp_file, 'r') as file:
            last_processed_timestamp_str = file.read().strip()
            last_processed_timestamp = datetime.datetime.fromisoformat(last_processed_timestamp_str)
    except (FileNotFoundError, ValueError) as e:
        logging.error(f'Could not find file {last_processed_timestamp_file}')
        raise e

    last_processed_timestamp_str = str(last_processed_timestamp)
    current_timestamp = datetime.datetime.utcnow()

    query = f"""
        SELECT *
        FROM product
        WHERE row_inserted_at > '{last_processed_timestamp_str}'
    """

    with pg_engine.connect() as conn, conn.begin():
        df_product = pd.read_sql(query, conn)

    if 'row_inserted_at' in df_product.columns:
        df_product = df_product.drop(columns=['row_inserted_at'])
    if 'id' in df_product.columns:
        df_product = df_product.drop(columns=['id'])

    if not df_product.empty:
        with open(last_processed_timestamp_file, 'w') as file:
            file.write(current_timestamp.isoformat())

    df_product.to_sql('DimProduct', ch_engine, if_exists='append', index=False)



def replicate_and_transform_order_data(pg_engine, ch_engine):
    logging.info('Starting replicate_and_transform_order_data')
    last_processed_timestamp_file = 'logs/last_processed_timestamp_order_data.txt'

    try:
        with open(last_processed_timestamp_file, 'r') as file:
            last_processed_timestamp_str = file.read().strip()
            last_processed_timestamp = datetime.datetime.fromisoformat(last_processed_timestamp_str)
    except (FileNotFoundError, ValueError) as e:
        logging.error(f'Could not find file {last_processed_timestamp_file}')
        raise e

    last_processed_timestamp_str = str(last_processed_timestamp)
    current_timestamp = datetime.datetime.utcnow()

    query = f"""
        SELECT order_date, customer_id, product_id, quantity, amount
        FROM public."order" inner join public."orderdetail" on public."order".id = public."orderdetail".order_id 
        WHERE orderdetail.row_inserted_at > '{last_processed_timestamp_str}'
    """

    with pg_engine.connect() as conn, conn.begin():
        df_product = pd.read_sql(query, conn)

    if not df_product.empty:
        with open(last_processed_timestamp_file, 'w') as file:
            file.write(current_timestamp.isoformat())

    df_product.to_sql('FactSales', ch_engine, if_exists='append', index=False)