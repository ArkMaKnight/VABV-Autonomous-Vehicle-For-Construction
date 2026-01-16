#ifndef CONFIG_H
#define CONFIG_H 
#include "esp_camera.h"

const char* WIFI_ID = "EAPIS";
const char* WIFI_PASS = "e@p1s4k*";

// #define ROBOT_IP 192,168,100,50
// #define GATEWAY 192,168,100,1

#define ROBOT_IP 10,1,77,15
#define GATEWAY 10,1,77,15
#define SUBNET 255,255,255,0

const char* API_ROBOT = "TESI_VEHAUT2025WAHFD";

// Pines Motores
#define PIN_WH1 12
#define PIN_WH2 13
#define PIN_WH3 14
#define PIN_WH4 15

#define INIT_SPEED 200

// Pines Cámara (AI THINKER)
#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27
#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5
#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22

void initCamera() {
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 10000000;
  config.pixel_format = PIXFORMAT_JPEG;
  
  // --- CONFIGURACIÓN SEGURA ---
  // Empezamos con baja calidad para asegurar que arranque
  config.frame_size = FRAMESIZE_QVGA;
  config.jpeg_quality = 20;
  if(config.pixel_format == PIXFORMAT_JPEG){
    if(psramFound()){
      config.fb_count = 2; // Usamos 2 si hay RAM extra
    } else {
      config.fb_count = 1; // Si no, solo 1
    }
  }

  // Iniciar
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("❌ Error iniciando camara: 0x%x\n", err);
    return;
  }
  Serial.println("✅ Cámara Iniciada Correctamente");
}
#endif