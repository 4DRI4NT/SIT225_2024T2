#include <DHT.h>

#define DHTPIN 2
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

float temp, hum;

void setup() {
  Serial.begin(9600);

  dht.begin();
}

void loop() {
  temp = dht.readTemperature();
  hum = dht.readHumidity();

  Serial.println(String(temp) + "," + String(hum));
  
  delay(10*1000);
}