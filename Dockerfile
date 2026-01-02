FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# We use Gunicorn + Eventlet for production-grade sockets, 
# but for dev, python app.py is fine.
CMD ["python", "app.py"]