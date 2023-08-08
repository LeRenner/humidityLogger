FROM python:latest

WORKDIR /usr/app/src
COPY logger.py ./
RUN mkdir -p /usr/app/src/mess
RUN python3 -m pip install paho-mqtt influxdb-client

CMD [ "python", "./logger.py"]
