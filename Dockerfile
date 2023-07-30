FROM python:3.9
ENV LANG C.UTF-8

ENV PYTHONUNBUFFERED 1
ARG USERNAME=user
RUN adduser --system --no-create-home $USERNAME
WORKDIR /app
RUN pip3 install virtualenv
RUN virtualenv venv
COPY requirements.txt .

RUN apt-get update && apt-get install -y --no-install-recommends \
    nginx \
    postgresql-client

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install Pillow

COPY . .
EXPOSE 8000

