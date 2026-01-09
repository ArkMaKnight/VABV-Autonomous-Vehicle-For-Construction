#include "config.h"
#include "engine.h" 
#include "Server.h" 

void setup() {
  Serial.begin(115200);
  
  // Iniciar Hardware
  configEngines();
  
  initCamera();
  // Iniciar Red
  iniciarTodoRed(); 
}

void loop() {
  // OBLIGATORIO: Mantener vivo el servidor de control
  server.handleClient(); 
static unsigned long lastCheck = 0;
  if (millis() - lastCheck > 2000) {
    lastCheck = millis();
    
    if (WiFi.status() == WL_CONNECTED) {
      // Imprime la potencia de la señal (RSSI)
      // -30 a -50: Excelente | -60 a -70: Bien | -80 a -90: Pésimo (Casi desconectado)
      long rssi = WiFi.RSSI();
      Serial.print("📶 Señal: ");
      Serial.print(rssi);
      Serial.println(" dBm (Estoy vivo)");
    } else {
      Serial.println("⚠️ ¡SE CAYÓ EL WIFI! Intentando reconectar...");
      WiFi.reconnect();
    }
  }}