FROM tiangolo/uwsgi-nginx-flask:python3.8

COPY ./app /app

WORKDIR /app

COPY requirements.txt ./

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

ENV STATIC_PATH /app/app/static
ENV SQLALCHEMY_DATABASE_URI sqlite:///db.sqlite
#RUN python init_model.py
#ENTRYPOINT [ "python" ]