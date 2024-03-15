# Data Pipeline from Postgres to Clickhouse

This repository contains a data pipeline solution designed to simulate the data flow between Postgres (OLTP) and Clickhouse (OLAP) databases for a store scenario. The store encompasses entities such as Customers, Products, and Orders. This solution is encapsulated within Docker containers for ease of deployment and testing.

## Overview

Upon initiating the Docker containers, the Postgres database is populated with initial data, including customers, products, and two example orders. A scheduled cron job is configured to generate new orders every minute, simulating real-time data generation. Additionally, an API is available for manually generating orders.

The data transfer from Postgres to Clickhouse occurs every 3 minutes, facilitated by a cron job for simplicity in this demonstration. In a production environment, I would recommend to use Airbyte for raw data transfer between Postgres and Clickhouse, and dbt for transforming the data from raw tables to Facts and Dimensions tables.

## Features

- Initial data setup in Postgres database (Customers, Products, Orders)
- Cron job for automatic order generation every minute
- API endpoint for manual order generation
- Scheduled data transfer from Postgres to Clickhouse every 3 minutes
- Logging of cron job results

## Prerequisites

- Docker is installed on your machine

## Installation and Usage

1. Clone this repository to your local machine.

2. Create a .env file with the following values for testing purposes:

```
POSTGRES_HOST = 'db'
POSTGRES_USERNAME = 'postgres'
POSTGRES_PASSWORD = 'postgres'
POSTGRES_DB = 'products'

```

4. Navigate to the repository directory in your terminal.

5. Build the Docker containers using the following command:

    ```bash
    docker-compose build
    ```

6. Start the Docker containers:

    ```bash
    docker-compose up
    ```

7. The API can be accessed at `http://localhost:8000/docs#/`. Use the `generate_order` endpoint to manually generate orders.

8. Logs can be found under `logs/cron_logs/cron.log`.


## Logs

The results of the cron jobs are logged for monitoring and debugging purposes. Logs are available at:

```
logs/cron_logs/cron.log
```

API logs are available at:

```
logs/logfile.log
```

## Recommendations for Production

For deploying this solution in a production environment, I would make the following changes:

- Utilize Airbyte for data transfer between Postgres and Clickhouse to ensure scalability and reliability.
- Use dbt for data transformation to efficiently manage the data modeling process and ensure data quality.
- A problem might occur, when the database build hasn't finished before the api is setup. Currently I have solved it by making the main service wait 60 seconds. This should be solved better, either in the docker-compose file with dependency conditions or by using netcat to check if the database connection is up and running.
- Currently the setup for Clickhouse table doesn't include an automatically generated UUID as the id of the table and a default id is assigned to all the entries. In a production environment, an ID generator should be added.
