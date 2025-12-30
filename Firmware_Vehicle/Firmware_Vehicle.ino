#include <WiFi.h>
#include <ArduinoJson.h>
#include "config.h"
#include "engine.h"
#include "esp_http_server.h"
#include "ESP32_Stream_Driver.h"

httpd_handle_t camera_httpd = NULL;
httpd_handle_t control_httpd = NULL;

static esp_err_t cmd_handler(httpd_req_t *req) {
  char content[100];

  int ret = httpd_req_recv(req, content, sizeof(content));
  if (ret <= 0) return ESP_FAIL;
  content[ret] = '\0'; 


  StaticJsonDocument<200> doc;
  DeserializationError error = deserializeJson(doc, content);

  if (error) {
    httpd_resp_send_500(req);
    return ESP_FAIL;
  }

  const char* action = doc["action"];

  if (strcmp(action, "FORWARD") == 0) {
    avanzar();
    httpd_resp_send(req, "OK: Forward", HTTPD_RESP_USE_STRLEN);
  } 
  else if (strcmp(action, "STOP") == 0) {
    detener();
    httpd_resp_send(req, "OK: Stop", HTTPD_RESP_USE_STRLEN);
  }
  else {
    httpd_resp_send(req, "Unknown", HTTPD_RESP_USE_STRLEN);
  }
  return ESP_OK;

  void setup() {
  Serial.begin(115200);
  
  Serial.println("==============================================")
  Serial.println("|                                             |")
  Serial.println("|    INICIANDO CONFIGURACIÓN ESP-32-MB        |")
  Serial.println("|                                             |")
  Serial.println("==============================================")
  configEngines();
  configureHardwareCamera(); 

  // 2. Conectar Wi-Fi
  IPAddress local_ip(ROBOT_IP);
  IPAddress gateway(GATEWAY);
  IPAddress subnet(SUBNET);
  WiFi.config(local_ip, gateway, subnet);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  
  Serial.print("Conectando");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500); Serial.print(".");
  }
  Serial.println("\nVEHÍCULO Conectado!");


  httpd_config_t config = HTTPD_DEFAULT_CONFIG();

  config.server_port = 81;
  config.ctrl_port = 32768 + 1;
  httpd_uri_t stream_uri = { .uri = "/stream", .method = HTTP_GET, .handler = stream_handler, .user_ctx = NULL };
  httpd_start(&camera_httpd, &config);
  httpd_register_uri_handler(camera_httpd, &stream_uri);


  config.server_port = 80;
  httpd_uri_t cmd_uri = { .uri = "/control", .method = HTTP_POST, .handler = cmd_handler, .user_ctx = NULL };
  httpd_start(&control_httpd, &config);
  httpd_register_uri_handler(control_httpd, &cmd_uri);
  
  Serial.println("🚀 Robot Listo para Tesis");
}

void loop() {
  delay(10000);
}
}