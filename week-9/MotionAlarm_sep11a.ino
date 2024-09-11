#include "arduino_secrets.h"
#include "thingProperties.h"

int ledPin = 13;
int sensorPin = 2;
int pirState = LOW;
int val = 0;

void setup() {
  //declare sensor and led
  pinMode(ledPin, OUTPUT);
  pinMode(sensorPin, INPUT);
  
  // Initialize serial and wait for port to open:
  Serial.begin(9600);
  // This delay gives the chance to wait for a Serial Monitor without blocking if none is found
  delay(1500); 

  // Defined in thingProperties.h
  initProperties();

  // Connect to Arduino IoT Cloud
  ArduinoCloud.begin(ArduinoIoTPreferredConnection);
  
  /*
     The following function allows you to obtain more information
     related to the state of network and IoT Cloud connection and errors
     the higher number the more granular information you’ll get.
     The default is 0 (only errors).
     Maximum is 4
 */
  setDebugMessageLevel(2);
  ArduinoCloud.printDebugInfo();
}

void loop() {
  ArduinoCloud.update();

  //get value from sensor
  val = digitalRead(sensorPin);

  //if movement
  if (val == HIGH)
  {
    //led on
    digitalWrite(ledPin, HIGH);

    //if previously no movement
    if (pirState == LOW) 
	  {
      //if untriggered alarm
      if (trigger == false)
      {
        trigger = true;
        Serial.println("Alarm triggered");
      }

      //print result to terminal and set previous state
      Serial.println("Motion detected");
      pirState = HIGH;
    }
  } 
  else 
  {
    //led off
    digitalWrite(ledPin, LOW);
	
    //if previously movement
    if (pirState == HIGH)
    {
      //if untriggered alarm
      if (trigger == false)
      {
        trigger = true;
        Serial.println("Alarm triggered");
      }

      //print result to terminal and set previous state
      Serial.println("Motion ended");
      pirState = LOW;
    }
  } 
}



/*
  Since Trigger is READ_WRITE variable, onTriggerChange() is
  executed every time a new value is received from IoT Cloud.
*/
void onTriggerChange()  {
  Serial.println("--onTriggerChange");
}