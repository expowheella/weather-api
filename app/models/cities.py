from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd
import openpyxl

# from settings import db_config
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship

import dotenv

dotenv.load_dotenv()

from settings import Base, DATABASE_URI

"""Database connection configuration. """


# Define the City model
class City(Base):
    __tablename__ = "cities2"

    city_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    longitude = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    country = Column(String, nullable=False)

    logs = relationship("Logs", back_populates="city", cascade="all, delete-orphan")


def create_cities(session):
    """List of cities to insert."""

    cities = pd.read_excel("app/models/cities.xlsx")
    cities.columns = ["name", "longitude", "latitude", "country"]

    for _, city in cities.iterrows():
        city_instance = City(
            name=city[0], longitude=city[1], latitude=city[2], country=city[3]
        )
        session.add(city_instance)

    session.commit()
    session.close()

    print("City data inserted successfully.")
