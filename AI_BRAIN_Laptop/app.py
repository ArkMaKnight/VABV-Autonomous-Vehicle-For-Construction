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
camera.set()