#ifndef ENGINE_H
#define ENGINE_H

#include "config.h"
  
    void stop() {
    digitalWrite(PIN_WH1, LOW); digitalWrite(PIN_WH2, LOW);
    digitalWrite(PIN_WH3, LOW); digitalWrite(PIN_WH4, LOW);
    Serial.println("Vehículo detenido. (STOP)");
  }

  void configEngines() {
     // pinMode(PIN_FRT, OUTPUT); 
     // pinMode(PIN_BCK, OUTPUT);
     pinMode(PIN_WH1, OUTPUT); pinMode(PIN_WH2, OUTPUT);
     pinMode(PIN_WH3, OUTPUT); pinMode(PIN_WH4, OUTPUT);
     stop();
    Serial.println("Motores Listos.");
  }

  void EngineOn() {
    // analogWrite(PIN_FRT, INIT_SPEED);
    // analogWrite(PIN_BCK, INIT_SPEED);
  }

  void forward() {
    EngineOn();
    digitalWrite(PIN_WH1, HIGH); digitalWrite(PIN_WH2, HIGH);
    digitalWrite(PIN_WH3, LOW); digitalWrite(PIN_WH4, LOW);
    Serial.println("Vehículo Avanzando... (FORWARD)");
  }

  void backward() {
    EngineOn();
    digitalWrite(PIN_WH1, LOW); digitalWrite(PIN_WH2, LOW);
    digitalWrite(PIN_WH3, HIGH); digitalWrite(PIN_WH4, HIGH);
  }

#endif