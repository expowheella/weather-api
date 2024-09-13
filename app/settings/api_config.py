import os
import dotenv

dotenv.load_dotenv()


API_KEY = os.getenv("API_KEY")
API_URL = (
    "https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}"
)
