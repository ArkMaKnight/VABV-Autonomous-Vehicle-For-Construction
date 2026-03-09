from flask import Flask, render_template, Response
from ultralytics import YOLO
from dotenv import load_dotenv
from robot_controller import RobotController
from colors_detection import colorsDetections 
from ThreadedCamera import ThreadedESP32Camera
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import logic
import cv2, os
import time, threading, random


# ============================================
# CONFIGURACIÓN DE ENTORNO
# ============================================
load_dotenv()
DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() in ("true", "1", "yes")
DATA_SIMULATED = DEBUG_MODE
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
CORS(app)
app.config['DEBUG_MODE'] = DEBUG_MODE  # Pasar config al template

if not DEBUG_MODE:
    print("Carga de modelo YOLO de Roboflow...")
    model = YOLO("./modelos/model_best.pt")
    if model is not None:
        print("Felicidades, modelo encontrado y cargado.") 
    print("========================================")
    print("Esperando por la cámara...")
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
start_time = time.time()
count_people = 0
count_hardhat = 0
count_vest = 0
count_vehicle = 0
count_objects = 0
count_animals = 0
timeout_person = 0
timeout_epp = 0
limit_timeout = 5
frame = None
mode_detection = True
detect_objects = False
detect_stop = False
scan_epp = False
success_text = "EQUIPOS DE PROTECCIÓN Y DE SEGURIDAD DETECTADA..."
fail_text = "NO SE DETECTÓ EQUIPOS DE PROTECCIÓN EPP. - ACTIVANDO ALARMA..."
stop_text = "SE DETECTÓ SEÑAL DE PARE. PARANDO VEHÍCULO..."
permission_personal = colorsDetections.gray_color
msg_output = "NO DETECTADO"
current_action = "NADA"

def generate_frame(): 
    last_command_sent = ""
    global scan_epp, detect_stop, detect_objects
    global count_people, count_hardhat, count_vest,count_vehicle, count_objects 
    global timeout_person, limit_timeout, timeout_epp
    global msg_output, current_action, count_animals


    count_people = 0
    count_hardhat = 0
    count_vest = 0
    count_vehicle = 0
    count_stops = 0
    count_objects = 0
    count_arrow_left = 0
    count_arrow_right = 0
    count_animals = 0
    timeout_person = 0
    timeout_epp = 0

    while True: 
        # Resetear contadores en cada frame
        count_people = 0
        count_hardhat = 0
        count_stops = 0
        count_vest = 0
        count_vehicle = 0
        count_arrow_left = 0
        count_arrow_right = 0
        count_objects = 0
        count_animals = 0
        detect_stop = False
        detect_objects = False
        
        frame = camera.read()
       
        if frame is None:
           print("Esprando vídeo")
           time.sleep(0.8)
           continue
        frame = cv2.rotate(frame, cv2.ROTATE_180)
        results = model(frame, stream=True, conf=0.5, verbose = False)

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
                        cv2.rectangle(frame, (x1,y1), (x2,y2), colorsDetections.blue_color,3)
                    case "hard-hat":
                        count_hardhat +=1
                        cv2.rectangle(frame, (x1,y1), (x2,y2), colorsDetections.green_color, 3)
                    case "vest":
                        count_vest +=1
                        cv2.rectangle(frame, (x1,y1), (x2,y2), colorsDetections.green_color,3)
                    case "vehicle":
                        count_vehicle +=1
                        cv2.rectangle(frame, (x1,y1), (x2,y2), colorsDetections.black_color, 2)
                    case "stop_sign":
                        count_stops +=1
                        detect_stop = True
                        cv2.rectangle(frame, (x1, y1), (x2,y2), colorsDetections.red_color, 3)
                    case "objects":
                        count_objects +=1
                        detect_objects = True
                        cv2.rectangle(frame, (x1,y1), (x2,y2), colorsDetections.purple_color, 2)
                    case "animal":
                        count_animals +=1
                        cv2.rectangle(frame, (x1,y1), (x2,y2), colorsDetections.yellow_color, 2)
                    case "arrow_left":
                        count_arrow_left +=1
                        cv2.rectangle(frame, (x1,y1), (x2,y2), colorsDetections.gray_color, 2)
                    case "arrow_right":
                        count_arrow_right +=1
                        cv2.rectangle(frame, (x1,y1), (x2,y2), colorsDetections.pink_color, 2)
                    case _: 
                        print("Lo siento, clase no especiifcada", currentClass)

                cv2.putText(frame, f'{currentClass} {conf}', (x1, y1-10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, colorsDetections.white_color, 2)

        detections = {
            'person' : count_people,
            'hard-hat': count_hardhat,
            'vest': count_vest,
            'vehicle': count_vehicle,
            'animal' : count_animals,
            'stop_sign': count_stops,
            "arrow_left": count_arrow_left,
            "arrow_right": count_arrow_right,
            'objects': count_objects

        }
        timeout_person, limit_timeout = logic.test_people(count_people, timeout_person, limit_timeout)
        msg_output, permission_personal, current_action, timeout_epp = logic.test_movement_security(detections ,timeout_epp)        

        if robot is not None and current_action != last_command_sent and mode_detection:
                match current_action:
                    case "STOP":
                        robot.stop()
                    case "ALARM":
                        robot.alarm_detector()
                    case "FORWARD":
                        robot.forward()
                    case "SLOW":
                        robot.slow_speed()
                    case "RIGHT":
                        robot.turn_right()
                    case "LEFT":
                        robot.turn_left()
                last_command_sent = current_action

        ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
        if not ret:
            print("Error al codificar")
            continue

        yield (b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + 
        buffer.tobytes() + b'\r\n')

def data_simulated():
    while True:
        if DATA_SIMULATED:
            person = random.randint(0, 3)
            hard_hat = random.randint(0, person)
            vest = random.randint(0, person)
            animal = random.choice([0, 0, 0, 1])
            objects = random.choice([0, 0, 0, 1])

            # Simular lógica de detección
            if person > 0 and (hard_hat < person or vest < person):
                sim_msg = "PERSONA(S) SIN EPP DETECTADA"
                sim_action = "ALARM"
            elif person > 0 or animal > 0:
                sim_msg = "PARADO PARA EVITAR ACCIDENTE"
                sim_action = "STOP"
            elif objects > 0:
                sim_msg = "BAJANDO VELOCIDAD"
                sim_action = "SLOW"
            else:
                sim_msg = "AVANZANDO..."
                sim_action = "FORWARD"

            data = {
                "person": person,
                "vest": vest,
                "hard_hat": hard_hat,
                "camera_connected": False,
                "wheels_connected": False,
                "latency": random.randint(10, 100),
                "animal": animal,
                "objects": objects,
                "uptime": get_uptime(),
                "packet_loss": random.randint(0, 5),
                "msg_output": sim_msg,
                "current_action": sim_action
            }
            socketio.emit('update_dashboard', data)
        time.sleep(1)



def get_uptime():
    """Calcula el tiempo de actividad del servidor"""
    uptime_seconds = int(time.time() - start_time)
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def background_telemetry():
    last_emit_time = time.time()
    while True:
        current_time = time.time()
        state_camera = camera is not None and camera.status_connection()
        state_wheels = robot is not None
        uptime_seconds = int(current_time - start_time)
        hours, remainder = divmod(uptime_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        uptime_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        
        latency_ms = int((current_time - last_emit_time) * 1000)
        last_emit_time = current_time
        
        data = {
            "person": count_people,
            "hard_hat": count_hardhat,
            "vest": count_vest,
            "animal": count_animals,
            "objects": count_objects,
            "camera_connected": state_camera,
            "wheels_connected": state_wheels,
            "uptime": uptime_str,
            "latency": latency_ms,
            "packet_loss": 0,
            "msg_output": msg_output,
            "current_action": current_action
        }
        socketio.emit('update_dashboard', data)
        time.sleep(1)
    
if (DEBUG_MODE):
    threading.Thread(target=data_simulated, daemon=True).start()
else:  
    threading.Thread(target=background_telemetry, daemon=True).start()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/video_feed')
def video_feed():
    if DEBUG_MODE:
        return Response("Modo Debug - Cámara deshabilitada", mimetype='text/plain')
    return Response(generate_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/control', methods=['POST'])
def api_control():
    global mode_detection
    from flask import request, jsonify
    json_data = request.get_json()
    action = json_data.get('action', '')
    command = json_data.get('command', '')
    print(f"🎮 [HTTP] Control Establecido: mode={mode_detection}, action={action}, command={command}")

    # Cambio de modo
    if action == "manual":
        mode_detection = False
        print("🎮 Modo MANUAL activado")
        return jsonify({"status": "ok", "mode": "manual"})
    elif action == "autoIA":
        mode_detection = True
        print("🤖 Modo AUTOMÁTICO (IA) activado")
        return jsonify({"status": "ok", "mode": "autoIA"})

    if robot is None:
        print("⚠️ Robot no detectado.")
        return jsonify({"status": "error", "msg": "Robot no conectado"}), 503

    # Control manual con WASD
    if command in ['w', 'a', 's', 'd'] and not mode_detection:
        if action == 'start':
            match command:
                case 'w':
                    robot.forward()
                case 's':
                    robot.backward()
                case 'a':
                    robot.turn_left()
                case 'd':
                    robot.turn_right()
        elif action == 'stop':
            robot.stop()
        return jsonify({"status": "ok", "command": command, "action": action})

    # Comandos directos
    match action:
        case "forward":
            robot.forward()
        case "backward":
            robot.backward()
        case "left":
            robot.turn_left()
        case "right":
            robot.turn_right()
        case "stop":
            robot.stop()
        case "slow":
            robot.slow_speed()
        case "alarm":
            robot.alarm_detector()
        case _:
            print(f"Acción desconocida: {action}")
            return jsonify({"status": "error", "msg": f"Acción desconocida: {action}"}), 400

    return jsonify({"status": "ok", "action": action})

@socketio.on("speed_change")
def handle_speed(data): 
    speed_value = data.get('speed', 255)
    print(f"Cambio de velocidad: {speed_value}")
    if robot is not None: 
        robot.set_speed(speed_value)

@socketio.on('control_command')
def handle_command(json_data):
    global mode_detection
    action = json_data.get('action', '')
    command = json_data.get('command', '')
    print(f"🎮 [WS] Control Establecido: mode={mode_detection}, action={action}, command={command}")

    # Cambio de modo
    if action == "manual":
        mode_detection = False
        return
    elif action == "autoIA":
        mode_detection = True
        return

    if robot is None:
        print("⚠️ Robot no detectado.")
        return

    if command in ['w', 'a', 's', 'd'] and not mode_detection:
        if action == 'start':
            match command:
                case 'w': robot.forward()
                case 's': robot.backward()
                case 'a': robot.turn_left()
                case 'd': robot.turn_right()
        elif action == 'stop':
            robot.stop()
        return

    match action:
        case "forward": robot.forward()
        case "backward": robot.backward()
        case "left": robot.turn_left()
        case "right": robot.turn_right()
        case "stop": robot.stop()
        case "slow": robot.slow_speed()
        case "alarm": robot.alarm_detector()
        case _: print(f"Acción desconocida: {action}")


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=DEBUG_MODE, allow_unsafe_werkzeug=DEBUG_MODE)