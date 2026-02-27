import {Chart, registerables} from 'chart.js';
Chart.register(...registerables);
import {io} from 'socket.io-client';
import { UIManager } from "./modules/uiManager.js";
import { ChartManager } from "./modules/chartManager.js";

console.log("Importando Interfaz...");
var chartMg;
var socket = io();
var ui;

try {
  ui = new UIManager();
  console.log("✅Importación UI Finalizada.")
  chartMg = new ChartManager();
  console.log("✅Importación de Gráficos.")
} catch (e) {
  console.log("Falló en implementar UI de Dashboard.", e)
} finally {
  console.log("Módulo I: Ejecutado.")
}


document.addEventListener('DOMContentLoaded', () => {
  const uptimeEl = document.getElementById('metric-uptime');
  const latencyEl = document.getElementById('metric-latency');
  const lossEl = document.getElementById('metric-loss');

  
  ui.showSideBar();
  ui.showLogs();
  ui.showControl();
  
  socket.on('update_dashboard', (d) => {
   const dataArray = [
    d.person || 0,
    d.animal || 0,
    d.hard_hat || 0,
    d.vest || 0,
    d.objects || 0 
  ];

  if(uptimeEl) uptimeEl.textContent = d.uptime || '00:00:00';
  if(latencyEl) latencyEl.textContent = d.latency || 0;
  if(lossEl) lossEl.textContent = d.packet_loss || 0;


  if (d.hard_hat >= d.person && d.vest >= d.person) {
    ui.normalStatus();

  } else {
    ui.detectAlarm();
  }

  chartMg.updateCharts(dataArray);


})
});

document.addEventListener('keydown', (event) => {
  const key = event.key.toLowerCase();
  if(['w', 'a', 's', 'd'].includes(key)) {
    socket.emit('control_command', {command: key, action: 'start'});
  }
})

document.addEventListener('keyup', e => {
  const key = e.key.toLowerCase();
  if(['w', 'a', 's', 'd'].includes(key)) {
    socket.emit('control_command', {command: key, action: 'stop'});
  }
})



function addLog(msg) {
  const logs = document.getElementById("logsBox");
  const time = new Date().toLocaleDateString();
  const newLine = document.createElement('div');
  newLine.style.borderBottom = "1px solid #444";
  newLine.innerHTML = `<small>[${time}</small> ${msg}`;
  logs.insertBefore(newLine, logs.firstChild);

}


