FROM python:3.9.5-slim-buster

WORKDIR /usr/src/app

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

RUN pip install Flask
RUN pip install Jinja2 redis Werkzeug

RUN pip install pandas
RUN pip install lxml

EXPOSE 5000

COPY . /usr/src/app/

CMD ["flask", "run"]
