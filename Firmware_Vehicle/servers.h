#ifndef SERVER_H
#define SERVER_H

#include <WiFi.h>
#include "esp_http_server.h"
#include <ArduinoJson.h>
#include "config.h"
#include "engine.h"
#include "esp_camera.h"

httpd_handle_t camera_httpd = NULL;
httpd_handle_t control_httpd = NULL;

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
}


