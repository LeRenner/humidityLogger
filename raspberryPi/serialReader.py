import serial
import paho.mqtt.client as mqtt


# Serial configuration
ARDUINO_SERIAL_PORT = '/dev/ttyACM0'  # Adjust this to match your Arduino's serial port
BAUD_RATE = 9600

# MQTT configuration
BROKER_ADDRESS = '192.168.15.120'  # Replace with your local broker's address
MQTT_HUMIDITY = 'dht22/humidity'
MQTT_TEMPERATURE = 'dht22/temperature'


#check for -v flag
import sys
if len(sys.argv) > 1:
    if sys.argv[1] == "-v":
        print("Verbose mode enabled")
        verbose = True
else:
    verbose = False


# Function to read float value from Arduino via serial
def readArduinoData():
    with serial.Serial(ARDUINO_SERIAL_PORT, BAUD_RATE) as ser:
        data = []
        try:
            line = ser.readline().decode().strip().split("@")
            data.append(float(line[0]))
            data.append(float(line[1]))
            return data
        except ValueError:
            return None


# Function to send float value as an MQTT packet
def sendMqttPacket(values):
    client = mqtt.Client()
    client.connect(BROKER_ADDRESS)
    client.publish(MQTT_HUMIDITY, str(values[0]))
    client.disconnect()
    client.connect(BROKER_ADDRESS)
    client.publish(MQTT_TEMPERATURE, str(values[1]))
    client.disconnect()


if __name__ == '__main__':
    while True:
        float_value = readArduinoData()
        if float_value is not None:
            if verbose: print(float_value)
            sendMqttPacket(float_value)