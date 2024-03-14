
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import logging

from data_replication_script import replicate_and_transform_customer_data, replicate_and_transform_product_data, \
    replicate_and_transform_order_data
from generate_random_orders import generate_random_order
from db.clickhouse_database import clickhouse_engine
from db.database import engine

app = FastAPI(
    title="Product database",
)
origins = [
    "http://localhost",
    "http://localhost:3000",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.info("Application started!")

@app.get("/healthcheck")
def healthcheck():
    return "OK"


@app.get("/generate_order")
def generate_order():
    generate_random_order()
    return "finished adding the data"


@app.get("/move_the_data")
def move_the_data():
    replicate_and_transform_customer_data(pg_engine=engine, ch_engine=clickhouse_engine)
    replicate_and_transform_product_data(pg_engine=engine, ch_engine=clickhouse_engine)
    replicate_and_transform_order_data(pg_engine=engine, ch_engine=clickhouse_engine)
    return "finished moving the data"

