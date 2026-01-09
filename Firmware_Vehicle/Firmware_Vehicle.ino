#include "esp_camera.h"
#include "esp_http_server.h"
#include <WiFi.h>
#include <ArduinoJson.h>

// Librerías para "La Vacuna" (Evitar reinicios por energía)
#include "soc/soc.h"
#include "soc/rtc_cntl_reg.h"

#include "config.h"
#include "engine.h"
#include "ESP32_Stream_Driver.h"

// Instancias de servidores
httpd_handle_t camera_httpd = NULL;
httpd_handle_t control_httpd = NULL;

// --- TU LÓGICA DE CONTROL ---
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
    forward();
    httpd_resp_send(req, "OK: Forward", HTTPD_RESP_USE_STRLEN);
  } 
  else if (strcmp(action, "STOP") == 0) {
    stop();
    httpd_resp_send(req, "OK: Stop", HTTPD_RESP_USE_STRLEN);
  }
  else {
    httpd_resp_send(req, "Unknown", HTTPD_RESP_USE_STRLEN);
  }
  return ESP_OK;
}

void setup() {
  // 1. LA VACUNA: Desactivar detector de caídas de tensión
  WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0); 
  delay(1000);
  Serial.begin(115200);
  Serial.println("==============================================")
  Serial.println("|                                             |")
  Serial.println("|    INICIANDO CONFIGURACIÓN ESP-32-MB        |")
  Serial.println("|                                             |")
  Serial.println("==============================================")
  delay(3000);
  // 2. Hardware
  Serial.println("1. Motores... ");
  configEngines();
  Serial.println("OK");

  Serial.print("2. Cámara... ");
  configureHardwareCamera(); 
  Serial.println("OK");

  // 3. Wi-Fi
  Serial.print("3. Conectando WiFi... ");
  IPAddress local_ip(ROBOT_IP);
  IPAddress gateway(GATEWAY);
  IPAddress subnet(SUBNET);
  WiFi.config(local_ip, gateway, subnet);
  WiFi.begin(WIFI_ID, WIFI_PASS);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500); Serial.print(".");
  }
  Serial.println("\n✅ WiFi Conectado!");

  // 4. Servidores
  Serial.println("4. Iniciando Servidores...");
 httpd_config_t config_video = HTTPD_DEFAULT_CONFIG(); // Configuración NUEVA para video
  config_video.server_port = 81;
  config_video.ctrl_port = 32768; // Puerto interno A
  
  httpd_uri_t stream_uri = { .uri = "/stream", .method = HTTP_GET, .handler = stream_handler, .user_ctx = NULL };
  
  Serial.print("   -> Iniciando Video... ");
  if (httpd_start(&camera_httpd, &config_video) == ESP_OK) {
    httpd_register_uri_handler(camera_httpd, &stream_uri);
    Serial.println("OK");
  } else {
    Serial.println("FALLO");
  }

  // --- B) Servidor de CONTROL (Puerto 80) ---
  httpd_config_t config_control = HTTPD_DEFAULT_CONFIG(); // Configuración NUEVA para control
  config_control.server_port = 80;
  config_control.ctrl_port = 32769; // Puerto interno B (¡DIFERENTE!)
  
  httpd_uri_t cmd_uri = { .uri = "/control", .method = HTTP_POST, .handler = cmd_handler, .user_ctx = NULL };

  Serial.print("   -> Iniciando Control... ");
  if (httpd_start(&control_httpd, &config_control) == ESP_OK) {
    httpd_register_uri_handler(control_httpd, &cmd_uri);
    Serial.println("OK");
  } else {
    Serial.println("FALLO");
  }
}

void loop() {
  delay(10000);
}
