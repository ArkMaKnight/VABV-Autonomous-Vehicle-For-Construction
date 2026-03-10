#ifndef SERVIDORES_H
#define SERVIDORES_H

#include <WiFi.h>
#include "esp_http_server.h"
#include "config.h"
#include "engine.h"
#include "ESP32_Stream_Driver.h"


// ==========================================
// 3. INICIADOR MAESTRO
// ==========================================
void iniciarTodoRed() {
  // A) CONECTAR WIFI (Automático)
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_ID, WIFI_PASS);
  
  Serial.print("Conectando WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500); Serial.print(".");
  }
  Serial.println("\n✅ CONECTADO!");
  Serial.print("📡 VIDEO: http://"); Serial.print(WiFi.localIP()); Serial.println(":81/stream");
  Serial.print("🎮 CONTROL: http://"); Serial.print(WiFi.localIP()); Serial.println("/control");

  // B) INICIAR VIDEO (Puerto 81)
  httpd_config_t config = HTTPD_DEFAULT_CONFIG();
  config.server_port = 81;
  config.ctrl_port = 32768; // Puerto interno A
  
  httpd_uri_t stream_uri = { .uri = "/stream", .method = HTTP_GET, .handler = stream_handler, .user_ctx = NULL };
  
  if (httpd_start(&stream_httpd, &config) == ESP_OK) {
    httpd_register_uri_handler(stream_httpd, &stream_uri);
    Serial.println("✅ Video OK");
  }

  // C) INICIAR CONTROL (Puerto 80)
  server.on("/control", HTTP_POST, handleControl);
  server.on("/control", HTTP_OPTIONS, handleControlOptions);
  server.on("/status", HTTP_GET, handleStatus);
  server.begin();
  Serial.println("✅ Control OK");
}

  

#endif