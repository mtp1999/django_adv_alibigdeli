FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt /app/
RUN pip3 install --upgrade pip
RUN pip install --upgrade pip setuptools wheel
RUN pip3 install -r requirements.txt
COPY ./backend /app/
