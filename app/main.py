"""Application's entrypoint"""

from fastapi import FastAPI
import api.history
import models
import settings
import api
from settings import get_db


# Create all tables in the database if they don't exist
settings.Base.metadata.create_all(bind=settings.engine)


async def lifespan(app: FastAPI):
    # Run startup code to create cities table
    db_generator = get_db()
    db_session = next(db_generator)

    try:
        models.create_cities(session=db_session)
        yield  # Yield control to start the application
    finally:
        # Make sure to close the session once the app shuts down
        next(db_generator, None)


app = FastAPI(lifespan=lifespan)

app.include_router(api.weather_router)
app.include_router(api.history_router)
app.include_router(api.cities_router)


# DEBUG MODE
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
