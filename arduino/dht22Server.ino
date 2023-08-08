// print temperature and humidity to serial monitor with '@' separator
// uses arduino leonardo and dht22 sensor

#include <DHT.h>

#define DHTPIN 9
#define DHTTYPE DHT22

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  Serial.println("DHT22 test");
  dht.begin();
}

void loop() {
  delay(2000);
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  Serial.print(h);
  Serial.print("@");
  Serial.println(t);
}
