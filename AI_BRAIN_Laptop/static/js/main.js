import { UIManager } from "./modules/uiManager";
console.log("Importando Interfaz...");

try {
  const ui = new UIManager();
  console.log("Importación UI Finalizada.")
} catch {
  console.log("Falló en implementar UI de Dashboard.")
} finally {
  console.log("Módulo I: Ejecutado.")
}



var socket = io();
socket.on('update_dashboard', data => {
  
});



