from flask import Flask, render_template, Response
from ultralytics import YOLO
from dotenv import load_dotenv
from robot_controller import RobotController
from colors_detection import colorsDetections 
from ThreadedCamera import ThreadedESP32Camera
from flask_socketio import SocketIO, emit
import cv2, os
import time, threading

# ============================================
# CONFIGURACIÓN DE ENTORNO
# ============================================
load_dotenv()
DEBUG_MODE = os.getenv("DEBUG_MODE")
print("========================================")
print(f"🔧 MODO: {'DEBUG (sin cámara)' if DEBUG_MODE else 'PRODUCCIÓN'}")
print("========================================")

# 1. Cargamos el controlador de nuestro robotcito
print("Inicializando vehículo...")


try: 
    robot = RobotController()
    print("Controlador Inicializado.")  
except Exception as e: 
    print("Error al cargar el controlador: ", e)
    robot = None
print("========================================")


# 2. Cargamos el modelo de Roboflow entrenado (solo en producción)
app = Flask(__name__)
app.config['DEBUG_MODE'] = DEBUG_MODE  # Pasar config al template

if not DEBUG_MODE:
    print("Carga de modelo YOLO de Roboflow...")
    model = YOLO(r'AI_BRAIN_Laptop\modelos\model_best.pt')
    if model is not None:
        print("Felicidades, modelo encontrado y cargado.") 
    print("========================================")
    print("Esperando por la cámara...")
    
    # 3. Cámara 
    esp32 = os.getenv("IP_VIDEO")
    print(f"Obteniendo conexión desde {esp32}")
    camera = ThreadedESP32Camera(esp32)
    print("📷 Cámara configurada")
else:
    print("⏭️ Saltando carga de modelo YOLO (modo debug)")
    print("⏭️ Saltando conexión de cámara (modo debug)")
    model = None
    camera = None

socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

# Timestamp de inicio para calcular tiempo activo
start_time = time.time()

def generate_frame(): 
    last_command_sent = ""
    scan_person = False
    scan_epp = False
    timeout_person = 0
    timeout_epp = 0
    limit_timeout = 5

    while True: 
        frame = camera.read()
       
        if frame is None:
           print("Esprando vídeo")
           time.sleep(0.8)
           continue
        frame = cv2.rotate(frame, cv2.ROTATE_180)
        results = model(frame, stream=True, conf=0.5, verbose = False)

        # Parámetros para manipular xd
        count_people = 0
        count_hardhat = 0
        count_vest = 0
        count_vehicle = 0
        count_objects = 0
        detect_objects = False
        detect_stop = False

        # Variables a Cambiar
        success_text = "EQUIPOS DE PROTECCIÓN Y DE SEGURIDAD DETECTADA..."
        fail_text = "NO SE DETECTÓ EQUIPOS DE PROTECCIÓN EPP. - ACTIVANDO ALARMA..."
        stop_text = "SE DETECTÓ SEÑAL DE PARE. PARANDO VEHÍCULO..."
        permission_personal = colorsDetections.gray_color
        msg_output = "NO DETECTADO"
        current_action = "NADA"

        for r in results: 
            boxes = r.boxes
            for box in boxes: 
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                class_id = int(box.cls[0])
                currentClass = model.names[class_id]
                conf = round(float(box.conf[0]), 2)
            
                match currentClass:
                    case "person":
                        count_people +=1
                        cv2.rectangle(frame, (x1,y1), (x2,y2), colorsDetections.blue_color,2)
                    case "hard-hat":
                        count_hardhat +=1
                        cv2.rectangle(frame, (x1,y1), (x2,y2), colorsDetections.green_color, 2)
                    case "vest":
                        count_vest +=1
                        cv2.rectangle(frame, (x1,y1), (x2,y2), colorsDetections.green_color,2)
                    case "vehicle":
                        count_vehicle +=1
                        cv2.rectangle(frame, (x1,y1), (x2,y2), colorsDetections.black_color, 2)
                    case "stop_sign":
                        detect_stop = True
                        cv2.rectangle(frame, (x1, y1), (x2,y2), colorsDetections.red_color, 2)
                    case "objects":
                        count_objects +=1
                        detect_objects = True
                        cv2.rectangle(frame, (x1,y1), (x2,y2), colorsDetections.purple_color, 2)
                    case _: 
                        print("Lo siento, clase no especiifcada", currentClass)

                cv2.putText(frame, f'{currentClass} {conf}', (x1, y1-10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, colorsDetections.white_color, 2)


        if count_people > 0:
            scan_person = True
            timeout_person = 0

        else: 
           timeout_person +=1
           if timeout_person >= limit_timeout:
            scan_person = False
            scan_epp = False
            timeout_person = 0

        if scan_person:
            current_frame = (count_hardhat > 0 and count_vest > 0) 
            print("Hay EPP? : ", scan_epp)
            print("Hay persona?",scan_person)
            print("¿Tiene ambos EPP?",current_frame)
            
            if (current_frame):
                scan_epp = True
                timeout_epp = 0

            else: 
                timeout_epp += 1
                if timeout_epp >= limit_timeout:
                    scan_epp = False

            if scan_epp:
                permission_personal = colorsDetections.green_color
                msg_output = success_text
                print(msg_output)
                current_action = "SLOW"
        
                if detect_stop: 
                    current_action = "FORWARD"
                    msg_output = stop_text  
                else: 
                    print("Disminuyendo velocidad...")
                    current_action = "SLOW"
            else:
                permission_personal = colorsDetections.red_color
                msg_output = fail_text
                print(msg_output)
                current_action = "STOP"

        else:
            print("ZONA DESPEJADA.")
            current_action = "FORWARD"
            if detect_objects:
                current_action = "STOP"
                print("Fin de la vía")
                print("Esperando por más instrucciones...")

       

        cv2.rectangle(frame, (0,0), (640,50), colorsDetections.white_color, -1)
        cv2.putText(frame, msg_output, (10,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.7, permission_personal, 2)


        if robot is not None and current_action != last_command_sent:
                match current_action:
                    case "STOP":
                        robot.stop()
                    case "ALARM":
                        robot.stop()
                        robot.alarm_detector()
                    case "FORWARD":
                        robot.forward()
                    case "SLOW":
                        robot.slow_speed()
                

        ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
        if not ret:
            print("Error al codificar")
            continue

        yield (b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + 
        buffer.tobytes() + b'\r\n')

def background_telemetry():
    last_emit_time = time.time()
    while True:
        current_time = time.time()
        uptime_seconds = int(current_time - start_time)
        hours, remainder = divmod(uptime_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        uptime_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        
        # Calcular latencia (tiempo entre emits)
        latency_ms = int((current_time - last_emit_time) * 1000)
        last_emit_time = current_time
        
        data = {
            "safe": 0,
            "no_safe": 0,
            "fps": 0,
            "alarms": 0,
            "persons": 0,
            "uptime": uptime_str,
            "latency": latency_ms,
            "packet_loss": 0  # Implementar lógica real después
        }
        socketio.emit('update_dashboard', data)
        time.sleep(1)
threading.Thread(target=background_telemetry, daemon=True).start()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/video_feed')
def video_feed():
    if DEBUG_MODE:
        # En modo debug, retorna una imagen placeholder
        return Response("Modo Debug - Cámara deshabilitada", mimetype='text/plain')
    return Response(generate_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

@socketio.on('control_command')
def handle_command(json_data):
    action = json_data['action']
    print(f"Control implementado: {action}")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=DEBUG_MODE, allow_unsafe_werkzeug=DEBUG_MODE)