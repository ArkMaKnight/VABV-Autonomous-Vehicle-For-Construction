import { UIManager } from "./modules/uiManager.js";
import { chartManager, charts } from "./modules/chartManager.js";

console.log("Importando Interfaz...");
var chartMg
var ui

try {
  const ui = new UIManager();
  console.log("✅Importación UI Finalizada.")
  chartMg = new chartManager();
  console.log("✅Importación de Gráficos.")
} catch {
  console.log("Falló en implementar UI de Dashboard.")
} finally {
  console.log("Módulo I: Ejecutado.")
}



var socket = io();
socket.on('update_dashboard', (d) => {
  const dataArray = [
    d.person || 0
  ]

  if(chartMg) {
    chartMg.updateCharts(dataArray);
  }
});



