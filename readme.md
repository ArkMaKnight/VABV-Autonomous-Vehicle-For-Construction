# 🤖 Carrito EPP-Core — Vehículo Autónomo de Verificación de EPP

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.1.2-000000?style=for-the-badge&logo=flask&logoColor=white)
![YOLO](https://img.shields.io/badge/YOLOv8-Ultralytics-00FFFF?style=for-the-badge)
![ESP32](https://img.shields.io/badge/ESP32-CAM-E7352C?style=for-the-badge&logo=espressif&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-7.3.1-646CFF?style=for-the-badge&logo=vite&logoColor=white)

**Proyecto Final — Tópicos Especiales en Sistemas Inteligentes**

| Campo | Detalle |
|---|---|
| 📚 **Curso** | Tópicos Especiales en Sistemas Inteligentes |
| 🔢 **Código** | 11Q252 |
| 🏫 **Universidad** | Universidad Nacional de Cajamarca |
| 📍 **Sede** | Cajamarca, Perú |
| 👨‍🏫 **Docente** | Nestor E. Muñoz Abanto |
| 👥 **Estudiantes** | David Campos Mines · Carlo F. Díaz Rodríguez · Víctor A. Marín Alcalde · Harold A. Ramos Callirgos · Witman D. Saldaña Vargas |

</div>

---

## 📋 Tabla de Contenidos

1. [Descripción General](#-descripción-general)
2. [Características Principales](#-características-principales)
3. [Arquitectura del Sistema](#-arquitectura-del-sistema)
4. [Tecnologías Utilizadas](#-tecnologías-utilizadas)
5. [Estructura del Proyecto](#-estructura-del-proyecto)
6. [Requisitos Previos](#-requisitos-previos)
7. [Instalación y Configuración](#-instalación-y-configuración)
8. [Uso del Sistema](#-uso-del-sistema)
9. [API y Endpoints](#-api-y-endpoints)
10. [Lógica de Seguridad](#-lógica-de-seguridad)
11. [Hardware](#-hardware)
12. [Autores](#-autores)

---

## 🎯 Descripción General

**Carrito EPP-Core** es un sistema de vehículo autónomo inteligente diseñado para entornos industriales, mineros y de construcción. Su objetivo principal es **verificar el uso correcto del Equipo de Protección Personal (EPP)** por parte de los trabajadores, además de navegar de forma segura detectando obstáculos, señales de tráfico y personas.

El sistema integra:
- **Visión por computadora** con YOLOv8 para detección en tiempo real.
- **Control autónomo** basado en una jerarquía de prioridades de seguridad.
- **Panel de control web** con telemetría en tiempo real.
- **Firmware embebido** en microcontrolador ESP32 para el movimiento del vehículo.

---

## ✨ Características Principales

- 🦺 **Verificación de EPP**: Detecta si los trabajadores usan casco y chaleco de seguridad.
- 🚨 **Alarma automática**: Activa una alarma sonora ante incumplimiento de EPP.
- 🛑 **Anticolisión**: Detiene el vehículo ante personas u obstáculos en su trayecto.
- 🚦 **Reconocimiento de señales**: Interpreta señales de detención y flechas direccionales.
- 🎮 **Modo manual y autónomo**: Alternancia entre control WASD por operador y conducción autónoma por IA.
- 📊 **Dashboard en tiempo real**: Estadísticas de detección, velocidad y telemetría vía WebSocket.
- 📷 **Video en vivo**: Transmisión MJPEG desde la cámara ESP32.

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────┐
│                   LAPTOP / SERVIDOR                     │
│                                                         │
│  ┌──────────────┐     ┌───────────────────────────────┐ │
│  │  Dashboard   │◄────│     Flask + Socket.IO         │ │
│  │  (Vite/JS)   │────►│  app.py  |  logic.py          │ │
│  └──────────────┘     │  ThreadedCamera.py             │ │
│                       │  robot_controller.py           │ │
│                       └───────────┬───────────────────┘ │
│                                   │ YOLOv8 Inference    │
│                                   │ (model_best.pt)     │
└───────────────────────────────────┼─────────────────────┘
                                    │ WiFi / HTTP REST
                          ┌─────────▼──────────┐
                          │   ESP32-CAM + L298N │
                          │   Firmware_Vehicle  │
                          │  (Arduino C++)      │
                          │  Motor A │ Motor B  │
                          └─────────────────────┘
```

### Flujo de Datos

1. La **cámara ESP32** transmite video MJPEG por WiFi al servidor Flask.
2. El servidor ejecuta **inferencia YOLOv8** sobre cada frame.
3. La **lógica de seguridad** (`logic.py`) evalúa las detecciones y emite un comando de movimiento.
4. El **controlador de robot** (`robot_controller.py`) envía el comando HTTP al ESP32.
5. Los resultados se emiten al **dashboard** por Socket.IO en tiempo real.

---

## 🛠️ Tecnologías Utilizadas

### Backend (Python)
| Librería | Versión | Uso |
|---|---|---|
| Flask | 3.1.2 | Servidor web y API REST |
| Flask-SocketIO | — | Comunicación en tiempo real |
| OpenCV | 4.12.0 | Captura y procesamiento de video |
| Ultralytics (YOLOv8) | 8.3.234 | Detección de objetos |
| PyTorch | 2.9.1+cu128 | Motor de inferencia de IA |
| NumPy | 2.2.6 | Operaciones numéricas |
| Polars | 1.35.2 | Procesamiento de datos |

### Frontend (JavaScript)
| Herramienta | Versión | Uso |
|---|---|---|
| Vite | 7.3.1 | Bundler y servidor de desarrollo |
| Chart.js | 4.5.1 | Gráficas de detecciones en tiempo real |
| Socket.IO Client | 4.8.3 | Comunicación WebSocket |

### Hardware (Firmware C++)
| Componente | Descripción |
|---|---|
| ESP32-CAM (AI Thinker) | Microcontrolador con módulo de cámara OV2640 |
| L298N | Driver de motores DC de doble canal |
| Motor DC × 2 | Tracción diferencial del vehículo |
| Buzzer | Alarma sonora ante falta de EPP |

---

## 📁 Estructura del Proyecto

```
Carrito-EPP-Core/
│
├── AI_BRAIN_Laptop/                 # 🧠 Módulo principal (servidor + IA)
│   ├── modelos/
│   │   └── model_best.pt            # Modelo YOLOv8 entrenado (EPP, señales, obstáculos)
│   ├── src/                         # Código fuente frontend (Vite)
│   │   ├── main.js                  # Punto de entrada, eventos Socket.IO
│   │   └── modules/
│   │       ├── chartManager.js      # Gráficas Chart.js
│   │       ├── uiManager.js         # Gestión del estado del UI
│   │       └── socketManager.js     # Capa de comunicación WebSocket
│   ├── static/                      # Archivos estáticos servidos por Flask
│   │   ├── css/                     # Hojas de estilo
│   │   └── img/                     # Iconos e imágenes
│   ├── templates/
│   │   └── index.html               # Plantilla Jinja2 del dashboard
│   ├── app.py                       # Servidor Flask principal
│   ├── logic.py                     # Motor de decisiones de seguridad
│   ├── robot_controller.py          # Interfaz de control del vehículo
│   ├── ThreadedCamera.py            # Manejo del stream MJPEG del ESP32
│   ├── best_telemetry.py            # Modelo de datos de telemetría
│   ├── colors_detection.py          # Constantes de colores para bounding boxes
│   ├── requirements.txt             # Dependencias Python
│   ├── package.json                 # Dependencias Node.js
│   └── vite.config.js               # Configuración del bundler Vite
│
├── Firmware_Vehicle/                # ⚙️ Firmware embebido (ESP32-CAM)
│   ├── Firmware_Vehicle.ino         # Sketch principal de Arduino
│   ├── config.h                     # Pines GPIO, credenciales WiFi, config cámara
│   ├── engine.h                     # Control PWM de motores y buzzer
│   ├── Server.h                     # Servidor HTTP y setup WiFi
│   └── ESP32_Stream_Driver.h        # Transmisión MJPEG
│
└── readme.md                        # Este archivo
```

---

## ✅ Requisitos Previos

### Software
- **Python** 3.10 o superior
- **Node.js** 18 o superior y **npm**
- **Arduino IDE** 2.x con soporte para ESP32 (placa *AI Thinker ESP32-CAM*)
- GPU con CUDA (opcional, recomendado para inferencia en tiempo real)

### Hardware
- ESP32-CAM (modelo AI Thinker)
- Driver de motores L298N
- 2 motores DC con reductora
- Buzzer activo 5V
- Fuente de alimentación (batería LiPo o banco de energía)
- Red WiFi compartida entre laptop y ESP32

---

## 🚀 Instalación y Configuración

### 1. Clonar el Repositorio

```bash
git clone https://github.com/ArkMaKnight/Carrito-EPP-Core.git
cd Carrito-EPP-Core
```

### 2. Configurar el Backend Python

```bash
cd AI_BRAIN_Laptop

# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
# .venv\Scripts\activate         # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Configurar el Frontend

```bash
# Instalar dependencias Node.js
npm install

# Compilar assets estáticos
npm run build
```

### 4. Configurar Variables de Entorno

Crear el archivo `.env` en `AI_BRAIN_Laptop/`:

```env
DEBUG_MODE=false
IP_VIDEO=http://<IP_DEL_ESP32>/stream
ESP32_IP=http://<IP_DEL_ESP32>
API_KEY=TESI_VEHAUT2025WAHFD
ENDPOINT_VIDEO=/stream
```

> ⚠️ **Nota:** Reemplazar `<IP_DEL_ESP32>` con la dirección IP asignada al ESP32 en la red WiFi local.

### 5. Cargar Firmware en el ESP32

1. Abrir `Firmware_Vehicle/Firmware_Vehicle.ino` en Arduino IDE.
2. Editar `config.h` con las credenciales WiFi correctas:
   ```cpp
   #define WIFI_SSID     "NOMBRE_DE_TU_RED"
   #define WIFI_PASSWORD "CONTRASEÑA"
   ```
3. Seleccionar la placa **AI Thinker ESP32-CAM**.
4. Compilar y cargar el firmware.

---

## ▶️ Uso del Sistema

### Iniciar el servidor (modo producción)

```bash
cd AI_BRAIN_Laptop
source .venv/bin/activate
python app.py
```

El dashboard estará disponible en: **`http://localhost:5000`**

### Modo desarrollo (hot-reload del frontend)

```bash
# Terminal 1 - Backend Flask
python app.py

# Terminal 2 - Frontend Vite (dev server)
npm run dev
```

El servidor de desarrollo Vite correrá en: **`http://0.0.0.0:5173`**

### Controles del Dashboard

| Acción | Control |
|---|---|
| Avanzar | `W` o botón ▲ |
| Retroceder | `S` o botón ▼ |
| Girar izquierda | `A` o botón ◄ |
| Girar derecha | `D` o botón ► |
| Detener | `Espacio` o botón ■ |
| Cambiar a modo autónomo | Interruptor en el dashboard |
| Ajustar velocidad | Control deslizante (0–255 PWM) |

---

## 🌐 API y Endpoints

### Flask (Servidor Principal)

| Endpoint | Método | Descripción |
|---|---|---|
| `/` | GET | Sirve el dashboard HTML |
| `/video_feed` | GET | Stream MJPEG del ESP32 vía proxy |
| `/api/control` | POST | Envía comandos manuales o cambia de modo |

**Ejemplo de comando manual:**
```json
POST /api/control
{
  "mode": "manual",
  "command": "FORWARD"
}
```

### WebSocket (Socket.IO)

| Evento | Dirección | Payload |
|---|---|---|
| `update_dashboard` | Servidor → Cliente | Conteo de detecciones, telemetría, estado |
| `speed_change` | Cliente → Servidor | Valor PWM (0–255) |

### ESP32 (Firmware)

| Endpoint | Método | Descripción |
|---|---|---|
| `:81/stream` | GET | Stream MJPEG de la cámara |
| `:80/control` | POST | Ejecuta comandos de movimiento |

**Comandos soportados por el ESP32:**
`FORWARD` · `BACKWARD` · `LEFT` · `RIGHT` · `STOP` · `ALARM_ON` · `ALARM_OFF`

---

## 🔐 Lógica de Seguridad

El módulo `logic.py` implementa una **jerarquía de prioridades** evaluada en cada frame de video:

```
Prioridad 0 — Verificación de EPP
  └─ ¿Hay personas sin casco O sin chaleco?
     └─ SÍ → ALARMA 🚨

Prioridad 1 — Anticolisión
  └─ ¿Hay personas O animales detectados?
     └─ SÍ → DETENER 🛑

Prioridad 2 — Señales de Tráfico
  └─ ¿Señal de stop detectada? → DETENER 🔴
  └─ ¿Flecha izquierda/derecha? → GIRAR ↔️

Prioridad 3 — Obstáculos
  └─ ¿Objetos en el camino?
     └─ SÍ → REDUCIR VELOCIDAD ⚠️

Prioridad 4 — Operación Normal
  └─ Camino despejado → AVANZAR ✅
```

> Esta lógica garantiza que la seguridad de las personas siempre tenga precedencia sobre cualquier otro objetivo de navegación.

---

## ⚙️ Hardware

### Diagrama de Pines ESP32-CAM + L298N

| Función | Pin ESP32 | Descripción |
|---|---|---|
| Motor A — IN1 | GPIO 12 | Dirección motor izquierdo |
| Motor A — IN2 | GPIO 13 | Dirección motor izquierdo |
| Motor B — IN3 | GPIO 14 | Dirección motor derecho |
| Motor B — IN4 | GPIO 15 | Dirección motor derecho |
| Buzzer | GPIO 4 | Señal de alarma activa |
| Cámara OV2640 | Pines dedicados | Resolución QVGA (320×240) |

### Parámetros de Cámara

| Parámetro | Valor |
|---|---|
| Resolución | QVGA (320 × 240 px) |
| Formato | JPEG |
| Puerto streaming | 81 |
| Puerto control | 80 |

---

## 👥 Autores

### 🎓 Estudiantes

| Nombre | Escuela | Universidad | Correo |
|---|---|---|---|
| David Campos Mines | Ingeniería de Sistemas | Universidad Nacional de Cajamarca | [dcamposm23_1@unc.edu.pe](mailto:dcamposm23_1@unc.edu.pe) |
| Carlo F. Díaz Rodríguez | Ingeniería de Sistemas | Universidad Nacional de Cajamarca | [cdiazr23_1@unc.edu.pe](mailto:cdiazr23_1@unc.edu.pe) |
| Víctor A. Marín Alcalde | Ingeniería de Sistemas | Universidad Nacional de Cajamarca | [vmarina23_2@unc.edu.pe](mailto:vmarina23_2@unc.edu.pe) |
| Harold A. Ramos Callirgos | Ingeniería de Sistemas | Universidad Nacional de Cajamarca | [hramosc23_1@unc.edu.pe](mailto:hramosc23_1@unc.edu.pe) |
| Witman D. Saldaña Vargas | Ingeniería de Sistemas | Universidad Nacional de Cajamarca | [wsaldanav23_1@unc.edu.pe](mailto:wsaldanav23_1@unc.edu.pe) |

### 👨‍🏫 Docente

| Nombre | Escuela | Universidad | Sede | Correo |
|---|---|---|---|---|
| Nestor E. Muñoz Abanto | Ingeniería de Sistemas | Universidad Nacional de Cajamarca | Cajamarca, Perú | [nestor.munoz@unc.edu.pe](mailto:nestor.munoz@unc.edu.pe) |

---

<div align="center">

*Desarrollado como Proyecto Final para el curso **Tópicos Especiales en Sistemas Inteligentes** (11Q252)*  
*Escuela Profesional de Ingeniería de Sistemas — **Universidad Nacional de Cajamarca**, Cajamarca, Perú*  
*Docente: **Nestor E. Muñoz Abanto***

</div> 