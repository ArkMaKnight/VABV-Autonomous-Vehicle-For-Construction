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
  const cameraIcon = document.getElementById('camera-icon');
  const cameraStatus = document.getElementById('camera-status');
  const wheelsIcon = document.getElementById('wheels-icon');
  const wheelsStatus = document.getElementById('wheels-status');

   const ICONS = {
    online: '/static/img/online_icon.svg',
    offline: '/static/img/offline_icon.svg'
  };

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

  if (cameraIcon && cameraStatus) {
      cameraIcon.src = d.camera_connected ? ICONS.online : ICONS.offline;
      cameraStatus.textContent = d.camera_connected ? 'Cámara Conectada' : 'Cámara Desconectada';
    }

    if (wheelsIcon && wheelsStatus) {
      wheelsIcon.src = d.wheels_connected ? ICONS.online : ICONS.offline;
      wheelsStatus.textContent = d.wheels_connected ? 'Ruedas Conectadas' : 'Ruedas Desconectadas';
    }
  if (d.hard_hat >= d.person && d.vest >= d.person) {
    ui.normalStatus();

  } else {
    ui.detectAlarm();
  }

  chartMg.updateCharts(dataArray);


})
});

// Variables de control
let currentMode = 'autoIA';

// Debug: verificar conexión del socket
socket.on('connect', () => {
  console.log('✅ Socket conectado al servidor');
});

socket.on('disconnect', () => {
  console.log('❌ Socket desconectado');
});

// Función para cambiar modo
function setMode(mode) {
  console.log(`🎮 Cambiando a modo: ${mode}`);
  currentMode = mode;
  socket.emit('control_command', { action: mode });
  
  const btnAuto = document.getElementById('btn-autoIA');
  const btnManual = document.getElementById('btn-manual');
  const modeLabel = document.getElementById('current-mode');
  const wasdControls = document.getElementById('wasd-controls');
  
  if (mode === 'autoIA') {
    btnAuto.classList.add('active');
    btnManual.classList.remove('active');
    modeLabel.textContent = 'AUTOMÁTICO';
    wasdControls.classList.remove('enabled');
  } else {
    btnManual.classList.add('active');
    btnAuto.classList.remove('active');
    modeLabel.textContent = 'MANUAL';
    wasdControls.classList.add('enabled');
  }
}

// Inicializar controles cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
  // Botones de modo
  document.getElementById('btn-autoIA')?.addEventListener('click', () => setMode('autoIA'));
  document.getElementById('btn-manual')?.addEventListener('click', () => setMode('manual'));
  
  // Botones WASD
  ['w', 'a', 's', 'd'].forEach(key => {
    const btn = document.getElementById(`btn-${key}`);
    if (btn) {
      btn.addEventListener('mousedown', () => {
        if (currentMode === 'manual') {
          socket.emit('control_command', { command: key, action: 'start' });
          btn.classList.add('pressed');
        }
      });
      btn.addEventListener('mouseup', () => {
        socket.emit('control_command', { command: key, action: 'stop' });
        btn.classList.remove('pressed');
      });
      btn.addEventListener('mouseleave', () => {
        btn.classList.remove('pressed');
      });
    }
  });
  
  // Botón alarma
  document.getElementById('btn-alarm')?.addEventListener('click', () => {
    socket.emit('control_command', { action: 'alarm' });
  });
  
  // Botón stop
  document.getElementById('btn-stop')?.addEventListener('click', () => {
    socket.emit('control_command', { action: 'stop' });
  });
});

// Control por teclado
document.addEventListener('keydown', (event) => {
  const key = event.key.toLowerCase();
  console.log(`⌨️ Tecla presionada: ${key}, Modo: ${currentMode}`);
  if(['w', 'a', 's', 'd'].includes(key) && currentMode === 'manual') {
    console.log(`📤 Enviando comando: ${key} start`);
    socket.emit('control_command', {command: key, action: 'start'});
    document.getElementById(`btn-${key}`)?.classList.add('pressed');
  }
})

document.addEventListener('keyup', e => {
  const key = e.key.toLowerCase();
  if(['w', 'a', 's', 'd'].includes(key)) {
    console.log(`📤 Enviando comando: ${key} stop`);
    socket.emit('control_command', {command: key, action: 'stop'});
    document.getElementById(`btn-${key}`)?.classList.remove('pressed');
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


