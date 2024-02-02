FROM python:3.10-slim-bullseye

#ffmpeg dependency for moviepy module
RUN apt-get update \
  && apt-get install -y --no-install-recommends --no-install-suggests \
  build-essential ffmpeg \
  && pip install --no-cache-dir --upgrade pip

WORKDIR /app
COPY ./requirements.txt /app
RUN pip install --no-cache-dir --requirement /app/requirements.txt
COPY . /app

#Since it is a consumer we do not expose port
#It is not a service making request
#This service is going to consume message from queue

CMD ["python3", "consumer.py"]
