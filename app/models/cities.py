from sqlalchemy import Column, Integer, String, Float
import pandas as pd
from sqlalchemy.orm import relationship
import dotenv
import queries
from settings import get_db


dotenv.load_dotenv()

from settings import Base

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
    
    # Check if cities are already in db
    if len(queries.get_cities(session)) > 0:
        return   
    
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
