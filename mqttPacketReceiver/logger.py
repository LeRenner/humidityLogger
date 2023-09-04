#!/usr/bin/python3

#check for -v flag
import sys
sys.stdout = sys.stderr

if len(sys.argv) > 1:
    if sys.argv[1] == "-v":
        # print to stderror
        print("Verbose mode enabled")
        verbose = True
else:
    verbose = False


import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


# InfluxDB credentials
INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_TOKEN = open("/secrets/token", "r").read().strip()
INFLUXDB_ORG = open("/secrets/org", "r").read().strip()
INFLUXDB_BUCKET = open("/secrets/bucket", "r").read().strip()

# MQTT credentials
config = open("/config/main.txt", "r").readlines()
MQTT_BROKER = config[0].strip()
MQTT_PORT = int(config[1].strip())

# MQTT topics
# topics look like this: "sensor/kind"
topicList = config[2].strip().split(",")

# InfluxDB client
influxdb_client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)

if verbose:
    # print all read information
    print("InfluxDB URL: ", INFLUXDB_URL)
    print("InfluxDB token: ", INFLUXDB_TOKEN)
    print("InfluxDB org: ", INFLUXDB_ORG)
    print("InfluxDB bucket: ", INFLUXDB_BUCKET)
    print("MQTT broker: ", MQTT_BROKER)
    print("MQTT port: ", MQTT_PORT)
    print("MQTT topics: ", topicList)


def on_connect(client, userdata, flags, rc):
    if verbose: print("Connected to MQTT broker with result code " + str(rc))
    for topic in topicList:
        client.subscribe(topic)
        if verbose: print("Subscribed to topic: " + topic)


def on_message(client, userdata, msg):
    if verbose: print("Received message on topic: " + msg.topic + " with payload: " + msg.payload.decode())
    try:
        # Parse the value from the message payload
        value = float(msg.payload)

        # Parse the value type from the topic
        value_type = msg.topic.split("/")[1]

        # Create a new InfluxDB point
        point = Point(value_type).field("value", value)
        write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)

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
