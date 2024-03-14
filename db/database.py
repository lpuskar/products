import logging
import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Numeric, DateTime, text
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, declarative_base
load_dotenv()

db_url = URL.create(
    "postgresql",
    username=os.getenv('POSTGRES_USERNAME'),
    password=os.getenv('POSTGRES_PASSWORD'),
    host=os.getenv('POSTGRES_HOST'),
    database=os.getenv('POSTGRES_DB'),
)


engine = create_engine(db_url, connect_args={"options": "-c timezone=utc"})
Base = declarative_base()


class Customer(Base):
    __tablename__ = "customer"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(100))
    row_inserted_at = Column(DateTime(timezone=True), server_default=text("timezone('utc', now())"), index=True)

    def __repr__(self):
        return (f"<Customer(id={self.id}, first_name='{self.first_name}', last_name='{self.last_name}',"
                f" email='{self.email}', row_inserted_at='{self.row_inserted_at}')>")


class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200))
    price = Column(Numeric)
    row_inserted_at = Column(DateTime(timezone=True), server_default=text("timezone('utc', now())"), index=True)

    def __repr__(self):
        return (f"<Product(id={self.id}, name='{self.name}', price={self.price},"
                f" row_inserted_at='{self.row_inserted_at}')>")


class Order(Base):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer)
    order_date = Column(DateTime(timezone=True))
    total_amount = Column(Numeric)
    row_inserted_at = Column(DateTime(timezone=True), server_default=text("timezone('utc', now())"), index=True)

    def __repr__(self):
        return (f"<Order(id={self.id}, customer_id={self.customer_id}, order_date='{self.order_date}',"
                f" total_amount={self.total_amount}, row_inserted_at='{self.row_inserted_at}')>")


class OrderDetail(Base):
    __tablename__ = "orderdetail"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer)
    product_id = Column(Integer)
    quantity = Column(Integer)
    amount = Column(Numeric)
    row_inserted_at = Column(DateTime(timezone=True), server_default=text("timezone('utc', now())"), index=True)

    def __repr__(self):
        return (f"<OrderDetail(id={self.id}, order_id={self.order_id}, product_id={self.product_id},"
                f" quantity={self.quantity}, row_inserted_at='{self.row_inserted_at}')>")


Base.metadata.create_all(engine)


def add_new_order_to_db(customer_id, order_date, total_amount):
    Session = sessionmaker(bind=engine)
    session = Session()

    new_order = Order(customer_id=customer_id, order_date=order_date, total_amount=total_amount)

    session.add(new_order)
    try:
        session.commit()
        print("New order added successfully.")
        return new_order.id
    except Exception as e:
        session.rollback()
        print(f"Failed to add new order. Error: {e}")
    finally:
        session.close()


def add_new_order_detail_to_db(order_id, product_id, quantity, amount):
    Session = sessionmaker(bind=engine)
    session = Session()

    new_order_detail = OrderDetail(order_id=order_id, product_id=product_id, quantity=quantity, amount=amount)

    session.add(new_order_detail)
    try:
        session.commit()
        print("New order detail added successfully.")
    except Exception as e:
        session.rollback()
        print(f"Failed to add new order detail. Error: {e}")
    finally:
        session.close()


def add_initial_data_to_db():
    Session = sessionmaker(bind=engine)
    session = Session()

    session.add(Product(name='Socks', price=5))
    session.add(Product(name='Shirt', price=10))
    session.add(Product(name='Pants', price=20))

    session.add(Customer(first_name='Mari', last_name='Maasikas', email='mari.maasikas@gmail.com'))
    session.add(Customer(first_name='John', last_name='Doe', email='john.doe@gmail.com'))
    session.add(Customer(first_name='Jane', last_name='Doe', email='jane.doe@gmail.com'))

    session.add(
        Order(customer_id=1,
              order_date=datetime(2024, 3, 9, 8, 30, tzinfo=timezone.utc),
              total_amount=25))
    session.add(
        Order(customer_id=2,
              order_date=datetime(2024, 3, 10, 11, 45, tzinfo=timezone.utc),
              total_amount=20))

    session.add(OrderDetail(order_id=1, product_id=1, quantity=3, amount=15))
    session.add(OrderDetail(order_id=1, product_id=2, quantity=1, amount=10))
    session.add(OrderDetail(order_id=2, product_id=3, quantity=1, amount=20))

    try:
        session.commit()
        print("Initial data added successfully.")
    except Exception as e:
        session.rollback()
        print(f"Failed to add initial data. Error: {e}")
    finally:
        session.close()


def is_order_table_empty(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        first_product = session.query(Product).first()
        return first_product is None
    except Exception as e:
        logging.info(f"Failed to check if the product table is empty. Error: {e}")
        return False
    finally:
        session.close()


if is_order_table_empty(engine):
    add_initial_data_to_db()



