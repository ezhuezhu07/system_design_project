
#baseimage

FROM python:3.10-slim-bullseye

RUN apt-get update \
   && apt-get install -y --no-install-recommends --no-install-suggests \
   build-essential default-libmysqlclient-dev \
   && pip install --no-cache-dir --upgrade pip


WORkDIR /sdapp
COPY ./requirements.txt /sdapp
RUN pip install --no-cache-dir --requirement /sdapp/requirements.txt
COPY . /sdapp

EXPOSE 6000

CMD ["python3", "server.py"]


 
