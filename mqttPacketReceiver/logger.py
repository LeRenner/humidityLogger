#!/usr/bin/python3

#check for -v flag
import sys
if len(sys.argv) > 1:
    if sys.argv[1] == "-v":
        print("Verbose mode enabled")
        verbose = True
else:
    verbose = False


import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


# InfluxDB credentials
INFLUXDB_URL = "http://influxdb:8086"
INFLUXDB_TOKEN = "TOKEN"
INFLUXDB_ORG = "ORG"
INFLUXDB_BUCKET = "BUCKET"

# MQTT credentials
MQTT_BROKER = "mosquitto"
MQTT_PORT = 1883

# MQTT topics
TEMPERATURE_TOPIC = "dht22/temperature"
HUMIDITY_TOPIC = "dht22/humidity"

# InfluxDB client
influxdb_client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)


def on_connect(client, userdata, flags, rc):
    if verbose: print("Connected to MQTT broker with result code " + str(rc))
    client.subscribe([(TEMPERATURE_TOPIC, 0), (HUMIDITY_TOPIC, 0)])


def on_message(client, userdata, msg):
    if verbose: print("Received message on topic: " + msg.topic + " with payload: " + msg.payload.decode())
    try:
        if msg.topic == TEMPERATURE_TOPIC:
            value_type = "temperature"
        elif msg.topic == HUMIDITY_TOPIC:
            value_type = "humidity"
        else:
            return

        # Parse the value from the message payload
        value = float(msg.payload)

        # Write the data to InfluxDB
        write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
        point = Point("dht22").tag("sensor", "dht22").field(value_type, value)
        write_api.write(bucket=INFLUXDB_BUCKET, record=point)

        if verbose: print("Data logged to InfluxDB: ", value_type, value)
    except Exception as e:
        print("Error logging data to InfluxDB: ", e)


def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    # Start the MQTT loop
    client.loop_forever()


if __name__ == "__main__":
    main()
