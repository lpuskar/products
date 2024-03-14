# !/usr/bin/env python3
import logging
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '')))

import random
from datetime import datetime, timezone

from dotenv import load_dotenv
load_dotenv()

from db.database import add_new_order_to_db, add_new_order_detail_to_db



def generate_random_order():
    logging.info("Starting to generate a random order")
    customer_ids = [1, 2, 3]
    product_ids = [1, 2, 3]
    quantities = [1, 2, 3, 4, 5]
    prices = [5, 10, 20]

    customer_id = random.choice(customer_ids)
    product_id = random.choice(product_ids)
    quantity = random.choice(quantities)
    order_date = datetime.now(timezone.utc)
    total_amount = quantity * prices[product_id-1]

    order_id = add_new_order_to_db(customer_id, order_date, total_amount)

    if order_id:
        add_new_order_detail_to_db(order_id, product_id, quantity, total_amount)

if __name__ == "__main__":
    print("Generating random orders...")
    generate_random_order()
