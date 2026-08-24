FROM python:3.11.2

WORKDIR /app

RUN pip install flask

COPY . .

CMD ["python", "app.py"]