from flask import Flask, render_template, Response
from ultralytics import YOLO
from dotenv import load_dotenv
from robot_controller import RobotController
from colors_detection import colorsDetections 
import cv2, os, requests
import urllib.request
import numpy as np

load_dotenv()
print("========================================")
print("Inicializando controlador...")

try: 
    robot = RobotController()
    print("Controlador Inicializado.")  
except Exception as e: 
    print("Error al cargar el controlador: ", e)
    robot = None
print("========================================")

print("Carga de modelo YOLO de Roboflow...")
app  = Flask(__name__)
model = YOLO(r'AI_BRAIN_Laptop\modelos\model_best.pt')

if model is not None:
    print("Felicidades, modelo encontrado y cargado.") 
print("========================================")
print("Esperando por la cámara...")

webcam = 0
esp32 = os.getenv("IP_VIDEO")

print(f"Obteniendo conexión desde {esp32}")

# Clase para manejar stream MJPEG del ESP32-CAM
class ESP32Camera:
    def __init__(self, url):
        self.url = url
        self.stream = None
        self.bytes_buffer = b''
        self._opened = False
        self.max_retries = 3
    
    def _connect(self):
        for attempt in range(self.max_retries):
            try:
                print(f"🔄 Conectando a {self.url}... (intento {attempt + 1}/{self.max_retries})")
                req = urllib.request.Request(self.url)
                self.stream = urllib.request.urlopen(req, timeout=30)
                self.bytes_buffer = b''
                self._opened = True
                print("✅ Cámara ESP32 conectada correctamente")
                return True
            except urllib.error.URLError as e:
                print(f"⚠️ Intento {attempt + 1} falló: {e}")
                if attempt < self.max_retries - 1:
                    import time
                    time.sleep(1)
            except Exception as e:
                print(f"❌ Error conectando a ESP32: {e}")
                if attempt < self.max_retries - 1:
                    import time
                    time.sleep(1)
        
        self._opened = False
        return False
    
    def isOpened(self):
        if not self._opened:
            return self._connect()
        return self._opened
    
    def read(self):
        if not self.isOpened():
            return False, None
        
        try:
            # Leer chunks del stream
            chunk = self.stream.read(4096)
            if not chunk:
                self._opened = False
                return False, None
            
            self.bytes_buffer += chunk
            
            # Buscar marcadores JPEG (SOI y EOI)
            start = self.bytes_buffer.find(b'\xff\xd8')
            end = self.bytes_buffer.find(b'\xff\xd9')
            
            if start != -1 and end != -1 and end > start:
                jpg = self.bytes_buffer[start:end+2]
                self.bytes_buffer = self.bytes_buffer[end+2:]
                
                # Decodificar JPEG a frame OpenCV
                frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                return frame is not None, frame
            
            return False, None
        except Exception as e:
            print(f"⚠️ Error leyendo frame: {e}, reconectando...")
            self._opened = False
            return False, None
    
    def release(self):
        if self.stream:
            self.stream.close()
        self._opened = False

# Usar la clase personalizada para ESP32 (conexión lazy)
camera = ESP32Camera(esp32)
print("📷 Cámara configurada (conexión al solicitar video)")

def generate_frame(): 
    frame_count = 0
    consecutive_errors = 0
    max_consecutive_errors = 30
    
    while True: 
        success, frame = camera.read()
        frame_count += 1
        
        if not success:
            consecutive_errors += 1
            if consecutive_errors > max_consecutive_errors:
                print(f"❌ Demasiados errores consecutivos ({consecutive_errors}), reconectando...")
                camera._opened = False
                consecutive_errors = 0
            continue
        
        consecutive_errors = 0  # Reset en frame exitoso

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

        for r in results: 
            boxes = r.boxes
            for box in boxes: 
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        
                class_id = int(box.cls[0])
                currentClass = model.names[class_id]
                conf = round(float(box.conf[0]), 2)

                match currentClass:
                    case "person":
                        count_people +=1
                        cv2.rectangle(frame, (x1,y1), (x2,y2), colorsDetections.blue_color,2)
                    case "hard_hat":
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
            if count_hardhat >= count_people and count_vest >= count_people:
                permission_personal = colorsDetections.green_color
                msg_output = success_text
                print(msg_output)
                robot.slow_speed()
            
                if detect_stop: 
                    robot.stop()  
                    msg_output = stop_text  
                else: 
                    print("Disminuyendo velocidad...")
                    robot.slow_speed()
            else:
                permission_personal = colorsDetections.red_color
                msg_output = fail_text
                print(msg_output)
                robot.stop()
                robot.alarm_detector()
        else: 
            print("ZONA DESPEJADA.")
            # robot.forward()
            if detect_objects:
                robot.stop()
                print("Fin de la vía")
                print("Esperando por más instrucciones...")


        cv2.rectangle(frame, (0,0), (640,50), colorsDetections.white_color, -1)
        cv2.putText(frame, msg_output, (10,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.7, permission_personal, 2)


        ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
        if not ret:
            print(f"Error al codificar frame {frame_count}")
            continue

        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + 
               buffer.tobytes() + b'\r\n')

        # key = cv2.waitKey(1) & 0xFF
        # if key == ord('w'):
        #     robot.forward()
        # elif key == ord('s'):
        #     robot.stop()
        # elif key == ord('q'):
        #     print("Saliendo...")
        #     break

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/video_feed')
def video_feed():
    return Response(generate_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)