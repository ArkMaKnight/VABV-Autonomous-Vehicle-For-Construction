from flask import Flask, render_template, Response
from ultralytics import YOLO
import cv2, math

app  = Flask(__name__)
model = YOLO(r'AI_BRAIN_Laptop\modelos\model_best.pt')

classNames=["person", "hard_hat", "animal", "vest", "object", "vehicle"]
webcam = 0
esp32 = 1

camera = cv2.VideoCapture(webcam, cv2.CAP_DSHOW)
#camera.set(3,640)
# camera.set(4,480)

def generate_frame(): 
    while True: 
        success, frame = camera.read()
        if not success:
            break

        results = model(frame, stream=True, conf=0.5)
        frame = cv2.resize(frame, (640,480))
        results = model(frame, stream=True, conf=0.5)
        # Parámetros para manipular xd

        count_people = 0
        count_hardhat = 0
        count_vest = 0
        count_vehicle = 0
        green_color = (0,255,0)
        blue_color = (255,0,0)
        red_color = (0,0,255)
        black_color = (0,0,0)
        white_color = (255,255,255)
        gray_color = (200,200,200)

        # Variables a Cambiar
        success_text = "EQUIPOS DE PROTECCIÓN Y DE SEGURIDAD DETECTADA..."
        fail_text = "NO SE DETECTÓ EQUIPOS DE PROTECCIÓN EPP. - ACTIVANDO ALARMA..."
        permission_personal = gray_color
        msg_output = "NO DETECTADO"

        for r in results: 
            boxes = r.boxes
            for box in boxes: 
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        
                class_id = int(box.cls[0])
                currentClass = model.names[class_id]
                conf = math.ceil(box.conf[0])

                match currentClass:
                    case "person":
                        count_people +=1
                        cv2.rectangle(frame, (x1,y1), (x2,y2), blue_color,2)
                    case "hard_hat":
                        count_hardhat +=1
                        cv2.rectangle(frame, (x1,y1), (x2,y2), green_color, 2)
                    case "vest":
                        count_vest +=1
                        cv2.rectangle(frame, (x1,y1), (x2,y2), green_color,2)
                    case "vehicle":
                        count_vehicle +=1
                        cv2.rectangle(frame, (x1,y1), (x2,y2), black_color, 2)
                    case _: 
                        print("Lo siento, clase no especiifcada", currentClass)

                cv2.putText(frame, f'{currentClass} {conf}', (x1, y1-10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, white_color, 2)

            if count_people > 0:
                if count_hardhat >= count_people and count_vest >= count_people:
                    permission_personal = green_color
                    msg_output = success_text
                    print(msg_output)
                else:
                    permission_personal = red_color
                    msg_output = fail_text
                    print(msg_output)

            cv2.rectangle(frame, (0,0), (650,50), white_color, -1)
            cv2.putText(frame, msg_output, (10,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.7, permission_personal, 2)

            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret: 
                continue
            frame_bytes = buffer.tobytes()

            yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/video_feed')
def video_feed():
    return Response(generate_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)