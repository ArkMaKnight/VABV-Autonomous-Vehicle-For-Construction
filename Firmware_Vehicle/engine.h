#ifndef ENGINE_H
#define ENGINE_H

#include "config.h"

// Pin para buzzer/alarma en GPIO4
#define PIN_BUZZER 4
int current_speed = 255;

void stop() {
  analogWrite(PIN_WH1, 0); analogWrite(PIN_WH2, 0);   // Motor izq parado
  analogWrite(PIN_WH3, 0); analogWrite(PIN_WH4, 0);   // Motor der parado
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

// ==========================================
// L298N: IN1,IN2 = Motor Derecho (visto desde el frente)
//        IN3,IN4 = Motor Izquierdo (visto desde el frente)
// Cabina invertida: adelante = LOW,HIGH | atrás = HIGH,LOW
// ==========================================

void forward() {
  EngineOn();
  analogWrite(PIN_WH1, 0);  analogWrite(PIN_WH2, current_speed);  // Der adelante
  analogWrite(PIN_WH3, 0);  analogWrite(PIN_WH4, current_speed);  // Izq adelante
  Serial.println("Vehículo Avanzando... (FORWARD)");
}

void backward() {
  EngineOn();
  analogWrite(PIN_WH1, current_speed); analogWrite(PIN_WH2, 0);   // Der atrás
  analogWrite(PIN_WH3, current_speed); analogWrite(PIN_WH4, 0);   // Izq atrás
  Serial.println("Vehículo Retrocediendo... (BACKWARD)");
}

// Giro a la IZQUIERDA: rueda derecha avanza, izquierda para
void turnLeft() {
  EngineOn();
  analogWrite(PIN_WH1, 0);  analogWrite(PIN_WH2, current_speed);  // Der adelante
  analogWrite(PIN_WH3, 0);  analogWrite(PIN_WH4, 0);   // Izq parado
  Serial.println("Girando a la IZQUIERDA... (LEFT)");
}

// Giro a la DERECHA: rueda izquierda avanza, derecha para
void turnRight() {
  EngineOn();
  analogWrite(PIN_WH1, 0);  analogWrite(PIN_WH2, 0);   // Der parado
  analogWrite(PIN_WH3, 0);  analogWrite(PIN_WH4, current_speed);  // Izq adelante
  Serial.println("Girando a la DERECHA... (RIGHT)");
}

void acelerate() {
  current_speed = 255;
  Serial.println("Velocidad aumentada al máximo...");
}

void slow() {
  current_speed = 150;
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