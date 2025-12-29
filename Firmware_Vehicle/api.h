#ifndef SERVER_H
#define SERVER_H
#define PORT 30

#include <Wifi.h>
#include <WebSever.h>
#include <ArduinoJson.h>
#include "config.h"
#include "motores.h"

WebServer server(PORT);

void WiFiConnection() {
  IPAddress local_ip(ROBOT_IP);
  IPAddress gateway(GATEWAY);
  IPAddress subnet(SUBNET);

 Serial.print("Conectando a WiFi...");
  if (!WiFi.config(local_ip, gateway, subnet)) {
    Serial.println("Error de configuración de RED. Verificar.")
  } else {
  Serial.print("WiFi Conectado.");
  WiFi.begin(WIFI_ID, WIFI_PASS);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\n WIFi Conectado.")
  Serial.print("IP del ROBOT: ");
  Serial.println(WiFi.localIP());
  }

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
