FROM python:3.9-slim

RUN apt-get update && apt-get install -y bash \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir Flask==2.2.3 gunicorn==20.1.0

RUN pip install --upgrade Flask Gunicorn Werkzeug

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
