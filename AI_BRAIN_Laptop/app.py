from flask import Flask, render_template, Response
from ultralytics import YOLO 

app  = Flask(__name__)

# model = YOLO('modelos/best.pt')