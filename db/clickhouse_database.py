from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from clickhouse_sqlalchemy import make_session, get_declarative_base, types, engines
from sqlalchemy.types import UUID
import uuid

Base = declarative_base()

def generate_uuid():
    return uuid.uuid4()


class FactSales(Base):
    __tablename__ = 'FactSales'
    id = Column(UUID, primary_key=True, default=generate_uuid)
    order_date = Column(DateTime)
    customer_id = Column(Integer)
    product_id = Column(Integer)
    quantity = Column(Integer)
    amount = Column(Float)
    __table_args__ = (
        engines.MergeTree(order_by=(id,)),
    )

class DimCustomer(Base):
    __tablename__ = 'DimCustomer'
    id = Column(UUID, primary_key=True, default=generate_uuid)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    __table_args__ = (
        engines.MergeTree(order_by=(id,)),
    )

class DimProduct(Base):
    __tablename__ = 'DimProduct'
    id = Column(UUID, primary_key=True, default=generate_uuid)
    name = Column(String)
    price = Column(Float)
    __table_args__ = (
        engines.MergeTree(order_by=(id,)),
    )

db_url = "clickhouse://default:@clickhouse:8123/default"
clickhouse_engine = create_engine(db_url)

Base.metadata.create_all(clickhouse_engine)
