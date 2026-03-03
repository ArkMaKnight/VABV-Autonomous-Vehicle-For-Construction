#ifndef ENGINE_H
#define ENGINE_H

#include "config.h"

// Pin para buzzer/alarma (ajusta según tu conexión)
#define PIN_BUZZER 2

void stop() {
  digitalWrite(PIN_WH1, LOW); digitalWrite(PIN_WH2, LOW);
  digitalWrite(PIN_WH3, LOW); digitalWrite(PIN_WH4, LOW);
  Serial.println("Vehículo detenido. (STOP)");
}

void configEngines() {
  pinMode(PIN_WH1, OUTPUT); pinMode(PIN_WH2, OUTPUT);
  pinMode(PIN_WH3, OUTPUT); pinMode(PIN_WH4, OUTPUT);
  pinMode(PIN_BUZZER, OUTPUT);
  digitalWrite(PIN_BUZZER, LOW);
  stop();
  Serial.println("Motores Listos.");
}

void EngineOn() {
  // Para PWM si lo necesitas después
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
  Serial.println("Vehículo Retrocediendo... (BACKWARD)");
}

void slow() {
  // Velocidad reducida - usa PWM o simplemente pulsos
  // Por ahora avanza normal (puedes implementar PWM después)
  forward();
  Serial.println("Velocidad reducida... (SLOW)");
}

void alarm() {
  stop();
  // Activar buzzer por 2 segundos
  digitalWrite(PIN_BUZZER, HIGH);
  delay(500);
  digitalWrite(PIN_BUZZER, LOW);
  delay(200);
  digitalWrite(PIN_BUZZER, HIGH);
  delay(500);
  digitalWrite(PIN_BUZZER, LOW);
  Serial.println("ALARMA ACTIVADA!");
}

#endif