#ifndef ENGINE_H
#define ENGINE_H

#include "config.h"

// Pin para buzzer/alarma en GPIO4
#define PIN_BUZZER 4

void stop() {
  digitalWrite(PIN_WH1, LOW); digitalWrite(PIN_WH2, LOW);   // Motor izq parado
  digitalWrite(PIN_WH3, LOW); digitalWrite(PIN_WH4, LOW);   // Motor der parado
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

// ==========================================
// L298N: IN1,IN2 = Motor Derecho (visto desde el frente)
//        IN3,IN4 = Motor Izquierdo (visto desde el frente)
// Cabina invertida: adelante = LOW,HIGH | atrás = HIGH,LOW
// ==========================================

void forward() {
  digitalWrite(PIN_WH1, LOW);  digitalWrite(PIN_WH2, HIGH);  // Der adelante
  digitalWrite(PIN_WH3, LOW);  digitalWrite(PIN_WH4, HIGH);  // Izq adelante
  Serial.println("Vehículo Avanzando... (FORWARD)");
}

void backward() {
  digitalWrite(PIN_WH1, HIGH); digitalWrite(PIN_WH2, LOW);   // Der atrás
  digitalWrite(PIN_WH3, HIGH); digitalWrite(PIN_WH4, LOW);   // Izq atrás
  Serial.println("Vehículo Retrocediendo... (BACKWARD)");
}

// Giro a la IZQUIERDA: rueda derecha avanza, izquierda para
void turnLeft() {
  digitalWrite(PIN_WH1, LOW);  digitalWrite(PIN_WH2, HIGH);  // Der adelante
  digitalWrite(PIN_WH3, LOW);  digitalWrite(PIN_WH4, LOW);   // Izq parado
  Serial.println("Girando a la IZQUIERDA... (LEFT)");
}

// Giro a la DERECHA: rueda izquierda avanza, derecha para
void turnRight() {
  digitalWrite(PIN_WH1, LOW);  digitalWrite(PIN_WH2, LOW);   // Der parado
  digitalWrite(PIN_WH3, LOW);  digitalWrite(PIN_WH4, HIGH);  // Izq adelante
  Serial.println("Girando a la DERECHA... (RIGHT)");
}

void slow() {
  forward();
  Serial.println("Velocidad reducida... (SLOW)");
}

void alarm() {
  stop();
  // Activar buzzer desde GPIO4
  for (int i = 0; i < 3; i++) {
    digitalWrite(PIN_BUZZER, HIGH);
    delay(400);
    digitalWrite(PIN_BUZZER, LOW);
    delay(200);
  }
  Serial.println("🚨 ALARMA ACTIVADA! (GPIO4)");
}

#endif