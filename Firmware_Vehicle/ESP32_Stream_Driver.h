#ifndef STREAM_DRIVER_H
#define STREAM_DRIVER_H

#include <ArduinoJson.h>
#include <WebServer.h>      // Librería fácil para Control

#include "esp_http_server.h"

// --- OBJETOS GLOBALES ---
WebServer server(80);               // Puerto 80 para CONTROL
httpd_handle_t stream_httpd = NULL; // Puerto 81 para VIDEO

// ==========================================
// 1. LÓGICA DE VIDEO (MJPEG) - NO TOCAR
// ==========================================
#define PART_BOUNDARY "123456789000000000000987654321"
static const char* _STREAM_CONTENT_TYPE = "multipart/x-mixed-replace;boundary=" PART_BOUNDARY;
static const char* _STREAM_BOUNDARY = "\r\n--" PART_BOUNDARY "\r\n";
static const char* _STREAM_PART = "Content-Type: image/jpeg\r\nContent-Length: %u\r\n\r\n";

static esp_err_t stream_handler(httpd_req_t *req) {
  camera_fb_t *fb = NULL;
  esp_err_t res = ESP_OK;
  size_t _jpg_buf_len = 0;
  uint8_t *_jpg_buf = NULL;
  char part_buf[64];

  res = httpd_resp_set_type(req, _STREAM_CONTENT_TYPE);
  if (res != ESP_OK) return res;

  while (true) {
    fb = esp_camera_fb_get();
    if (!fb) {
      res = ESP_FAIL;
    } else {
      _jpg_buf_len = fb->len;
      _jpg_buf = fb->buf;
    }
    if (res == ESP_OK) {
      size_t hlen = snprintf(part_buf, 64, _STREAM_PART, _jpg_buf_len);
      res = httpd_resp_send_chunk(req, part_buf, hlen);
    }
    if (res == ESP_OK) {
      res = httpd_resp_send_chunk(req, (const char *)_jpg_buf, _jpg_buf_len);
    }
    if (res == ESP_OK) {
      res = httpd_resp_send_chunk(req, _STREAM_BOUNDARY, strlen(_STREAM_BOUNDARY));
    }
    if (fb) {
      esp_camera_fb_return(fb);
      fb = NULL;
      _jpg_buf = NULL;
    } else if (_jpg_buf) {
      free(_jpg_buf);
      _jpg_buf = NULL;
    }
    if (res != ESP_OK) break;
  }
  return res;
}

// ==========================================
// 2. LÓGICA DE CONTROL (JSON)
// ==========================================

// Maneja CORS preflight (OPTIONS)
void handleControlOptions() {
  server.sendHeader("Access-Control-Allow-Origin", "*");
  server.sendHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  server.sendHeader("Access-Control-Allow-Headers", "Content-Type");
  server.send(204);
}

void handleControl() {
  server.sendHeader("Access-Control-Allow-Origin", "*");
  server.sendHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  server.sendHeader("Access-Control-Allow-Headers", "Content-Type");

  // Manejar preflight
  if (server.method() == HTTP_OPTIONS) {
    server.send(204);
    return;
  }

  if (server.method() != HTTP_POST) {
    server.send(405, "text/plain", "Use metodo POST");
    return;
  }

  String message = server.arg("plain");
  Serial.println("📥 Recibido: " + message);
  
  StaticJsonDocument<200> doc;
  DeserializationError error = deserializeJson(doc, message);

  if (error) {
    Serial.println("❌ Error JSON");
    server.send(400, "application/json", "{\"error\":\"JSON Mal\"}");
    return;
  }

  // Validar API Key
  String auth = doc["auth"];
  if (auth != API_ROBOT) {
    Serial.println("❌ API Key inválida");
    server.send(401, "application/json", "{\"error\":\"No autorizado\"}");
    return;
  }

  String action = doc["action"];
  Serial.println("🎮 Acción: " + action);

  if (action == "FORWARD") {
    forward();
    server.send(200, "application/json", "{\"status\":\"ok\", \"msg\":\"Avanzando\"}");
  } 
  else if (action == "BACKWARD") {
    backward();
    server.send(200, "application/json", "{\"status\":\"ok\", \"msg\":\"Retrocediendo\"}");
  }
  else if (action == "LEFT") {
    turnLeft();
    server.send(200, "application/json", "{\"status\":\"ok\", \"msg\":\"Girando izquierda\"}");
  }
  else if (action == "RIGHT") {
    turnRight();
    server.send(200, "application/json", "{\"status\":\"ok\", \"msg\":\"Girando derecha\"}");
  }
  else if (action == "STOP") {
    stop();
    server.send(200, "application/json", "{\"status\":\"ok\", \"msg\":\"Detenido\"}");
  }
  else if (action == "SLOW") {
    slow();
    server.send(200, "application/json", "{\"status\":\"ok\", \"msg\":\"Velocidad reducida\"}");
  }
  else if (action == "ALARM_ACTIVATED") {
    alarm();
    server.send(200, "application/json", "{\"status\":\"ok\", \"msg\":\"Alarma activada\"}");
  } 
  else if (action == "SPEED") {
    int new_speed = doc["value"] | 255;
    if (new_speed < 0) new_speed = 0;
    if (new_speed > 255) new_speed = 255;

    if(new_speed = 255) acelerate();
    if(new_speed = 150) slow();
    current_speed = new_speed;
    Serial.println("Nueva velocidad: " + String(current_speed));
    server.send(200, "application/json", "{\"status\":\"ok\", \"msg\":\"Cambio velocidad\"}");

  }
  else {
    Serial.println("❌ Comando desconocido: " + action);
    server.send(400, "application/json", "{\"error\":\"Comando desconocido\"}");
  }
}
#endif