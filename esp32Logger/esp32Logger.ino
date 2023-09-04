#include <OneWire.h>
#include <DallasTemperature.h>
#include <WiFi.h>
#include <PubSubClient.h>

#define ONE_WIRE_BUS 14

// WiFi credentials
const char* ssid = "LeRouter";
const char* password = "PASSWORD";
const char* mqtt_server = "192.168.15.120";
const int 	mqtt_port = 32032;
const char* mqtt_topic = "fridge/temperature";

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);
WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
	Serial.begin(115200);

	// Start wifi
	Serial.println("Connecting to WiFi.");
	WiFi.begin(ssid, password);
	while (WiFi.status() != WL_CONNECTED) {
		delay(1000);
		Serial.print(".");
	}
	Serial.println("\nConnected to WiFi!");

	// MQTT Setup
	client.setServer(mqtt_server, mqtt_port);

	// Initialize DS18B20
	sensors.begin();

	// select 12-bit resolution
	sensors.setResolution(12);

	// wait for mqtt to connect
	while (!client.connected()) {
		Serial.println("Connecting to MQTT...");
		if (client.connect("ESP32Client")) {
			Serial.println("connected!");
		} else {
			Serial.print("failed with state ");
			Serial.print(client.state());
			delay(2000);
		}
	}
}

void loop() {
	client.loop();

	// Get temperature
	sensors.requestTemperatures();
	float temperature = sensors.getTempCByIndex(0);

	Serial.print("Temperature: ");
	Serial.println(temperature);

	// Publish temperature
	if (client.connected()) {
		String tempString = String(temperature, 2);
		client.publish(mqtt_topic, tempString.c_str());
		Serial.print("Published temperature: ");
		Serial.println(tempString);
	}

	Serial.println("Waiting 5 seconds...");
	// Wait 1 second
	delay(1000);
}