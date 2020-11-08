FROM python:3.7

COPY . /app

WORKDIR /app

RUN apt-get update -y 
RUN apt-get install build-essential python3-dev -y
RUN pip3 install -r requirements.txt

CMD python3 app.py