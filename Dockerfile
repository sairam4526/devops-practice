FROM python:3.11.2

WORKDIR /app

RUN pip install flask

COPY . .

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/')"

CMD ["python", "app.py"]