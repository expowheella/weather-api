FROM python:3.9

WORKDIR /code/app

COPY app/. /code/app
COPY requirements.txt /code/app

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


