from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey
)

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Category(Base):

    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)

    name = Column(String(100))

    products = relationship(

        "Product",

        backref="category"

    )


class Supplier(Base):

    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True)

    supplier_name = Column(String(100))

    phone = Column(String(20))

    email = Column(String(100))

    products = relationship(

        "Product",

        backref="supplier"

    )


class Product(Base):

    __tablename__ = "products"

    id = Column(Integer, primary_key=True)

    name = Column(String(100))

    price = Column(Float)

    quantity = Column(Integer)

    category_id = Column(
        Integer,
        ForeignKey("categories.id")
    )

    supplier_id = Column(
        Integer,
        ForeignKey("suppliers.id")
    )