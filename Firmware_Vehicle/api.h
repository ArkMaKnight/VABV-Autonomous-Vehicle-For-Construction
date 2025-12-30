#ifndef SERVER_H
#define SERVER_H
#define PORT 30

#include <Wifi.h>
#include <WebSever.h>
#include <ArduinoJson.h>
#include "config.h"
#include "motores.h"

WebServer server(PORT);

  void manageControl() {
      if (server.method() != HTTP_POST) {
        server.send(405, "text/plain", "Solo se permite POST");
        return;
      }

      StaticJsonDocument<200> doc;
      DesearilizationError error = deserializeJson(doc, server.arg("plain"));

      if (error) {
        server.send(400, "application/json", "{\"error\":\"JSON Invalido\"}");
        return;
      }

      const char auth = doc["auth"];
      if (auth != API_KEY) {
        Serial.println("Intento de Acceso no autorizado.");
        Server.send(403, "application/json", "{\"error\":\"Acceso Denegado\"}");
        return;
      }

      const char = doc["action"];
      if (action == "STOP") {
        stop();
        server.send(200, "application/json", "{\"status\":\"ok\", \"msg\":\"Detenido\"}");
      } else if (action == "FORWARD") {
        forward();
        server.send(200, "application/json", "{\"status\":\"ok\", \"msg\":\Adelante\"}");
      } else {
        server.send(400, "application/json", "{\"error\":\"desconocido\"}")
      }
  }

  void configServer() {
    server.on("/control", manageControl());
    server.begin();
    Serial.println("🔹 Servidor HTTP iniciado en puerto: " + PORT)

  }
} 
