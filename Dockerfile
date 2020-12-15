FROM tiangolo/uwsgi-nginx-flask:python3.8

COPY ./app /app

WORKDIR /app

COPY requirements.txt ./

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

ENV STATIC_PATH /app/app/static