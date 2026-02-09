import { UIManager } from "./modules/uiManager.js";
import { chartManager } from "./modules/chartManager.js";


console.log("Importando Interfaz...");
var chartMg;
var ui;

try {
  ui = new UIManager();
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
    d.person || 0,
    d.animal || 0,
    d.hard_hat || 0,
    d.vest || 0,
    d.objects || 0 
  ];

  if(chartMg) {
    chartMg.updateCharts(dataArray);
  }

  // Actualizar métricas del footer
  const uptimeEl = document.getElementById('metric-uptime');
  const latencyEl = document.getElementById('metric-latency');
  const lossEl = document.getElementById('metric-loss');
  
  if(uptimeEl) uptimeEl.textContent = d.uptime || '00:00:00';
  if(latencyEl) latencyEl.textContent = d.latency || 0;
  if(lossEl) lossEl.textContent = d.packet_loss || 0;
});



