FROM python:3.10-slim

COPY . /app

WORKDIR /app

RUN pip install --no-cache-dir -r /app/requirements.txt

# Install additional dependencies for Dash app
RUN pip install dash pymongo elasticsearch plotly pandas

