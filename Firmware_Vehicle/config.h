#ifndef CONFIG_H
#define CONFIG_H 

const char* WIFI_ID = "WIFI";
const char* WIFI_PASS = "CONTRASEÑA";

// Configuración RED IP para robotcito
#define ROBOT_IP 192,168,100,2
#define GATEWAY 192,168,1,1
#define SUBNET 255,255,255,0

const char* API_ROBOT = "API_ROBOT";

// Pines Motores
#define PIN_FRT 1
#define PIN_WH1 2
#define PIN_WH2 3
#define PIN_WH3 4
#define PIN_WH4 5
#define PIN_BCK 25

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


#endif