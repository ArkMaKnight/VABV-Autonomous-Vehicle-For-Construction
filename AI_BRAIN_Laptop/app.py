from flask import Flask, render_template, Response
from ultralytics import YOLO
import cv2
import math

app  = Flask(__name__)
model = YOLO('modelos/best.pt')

classNames=["person", "helmet", "animal", "vest", "object", "vehicle"]
webcam = 0
esp32 = 1

camera = cv2.VideoCapture(webcam)
camera.set(3,640)
camera.set(4,480)

def generar_frames(): 
    while True: 
        success, frame = camera.read()
        if not success:
            break

        results = model(frame, stream=True, conf=0.5)

        # Estadísticas

        count_people = 0
        count_hardhat = 0
        count_vest = 0
        count_vehicle = 0
        green_color = (0,255,0)
        blue_color = (255,0,0)
        black_color = (0,0,0)
        white_color = (255,255,255)
        gray_color = (200,200,200)

        # Variables a Cambiar
        success_text = "SEGURIDAD DETECTADA"
        fail_text = "NO SE DETECTÓ EQUIPOS DE PROTECCIÓN EPP."
        permission_personal = gray_color

        for r in results: 
            boxes = r.boxes
            for box in boxes: 
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        
            class_detected = int(box.class_detected[0])
            currentClass = model.names[class_detected]
            conf = round(box.conf[0], 2)

        match currentClass:
            case "person":
                count_people +=1
                cv2.rectangle(frame, (x1,y1), (x2,y2), blue_color,2)
            case "hard-hat":
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
            if count_hardhat >= count_people:
                print("Cascos detectados para todas las personas.")
                print(success_text)
            else:
                print(permission_personal)
                print(fail_text)
    