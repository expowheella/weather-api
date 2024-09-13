from sqlalchemy.orm import Session
import models
import schemas


"""Cities"""


def get_cities(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.City).offset(skip).limit(limit).all()

async def get_city_name_by_id(db: Session, city_id: int):
    return db.query(models.City).filter(models.City.city_id == city_id).first().name

async def get_history(db: Session):
    success = 200
    data = db.query(models.Logs).filter(models.Logs.status_code == success).order_by(models.Logs.timestamp.desc()).limit(5).all()
    return data
