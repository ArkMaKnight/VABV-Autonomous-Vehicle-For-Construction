#ifndef CONFIG_H
#define CONFIG_H 

// Configuración de HOST
const char* WIFI_ID = "WIFI";
const char* WIFI_PASS = "CONTRASEÑA";

// Configuración RED IP para robotcito
#define ROBOT_IP 192,168,100,2
#define GATEWAY 192,168,1,1
#define SUBNET 255,255,255,0

const char* API_ROBOT = "API_ROBOT";

// Pines 
#define PIN_FRT 1
#define PIN_WH1 2
#define PIN_WH2 3
#define PIN_WH3 4
#define PIN_WH4 5
#define PIN_BCK 25

#define SPEED_BASE 200

#endif