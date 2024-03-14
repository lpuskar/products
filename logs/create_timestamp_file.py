import datetime

beginning_timestamp = datetime.datetime(2024, 3, 1, 0, 0, 0)
timestamp_str = beginning_timestamp.strftime('%d.%m.%Y %H:%M:%S')

file_name = "last_processed_timestamp_customer_data.txt"
# file_name = "last_processed_timestamp_product_data.txt"
# file_name = "last_processed_timestamp_order_data.txt"

with open(file_name, 'w') as file:
    file.write(beginning_timestamp.isoformat())

print(f'Timestamp "{timestamp_str}" has been written to "{file_name}".')
