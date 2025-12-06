from ultralytics import YOLO
from roboflow import Roboflow
from dotenv import load_dotenv
import os
import torch

# Configuraciones 
iteraciones = 0
workspace = "tesi-intelligent-autonomous-smart-vehicle-for-construction"
project = "epp-autonomous-vehicle-construction"
tarjeta_grafica = 0


# Carga de KEY de Roboflow (*)
load_dotenv()
ROBOFLOW_KEY = os.getenv("ROBOFLOW_KEY")

if iteraciones == 0: 
# Verificamos que use la tarjeta gráfica asignada RTX4060
    print("¿CUDA disponible?:", torch.cuda.is_available())
    if torch.cuda.is_available():
        print("¡ÉXITO! Ahora usando:", torch.cuda.get_device_name(tarjeta_grafica))
        print("Versión de CUDA:", torch.version.cuda)
    else:
        print("Sigue saliendo CPU... avísame si pasa esto.")
    if not ROBOFLOW_KEY: 
        print("API no encontrada. Descartando cambios...")

print("Número de iteraciones: ", iteraciones)
#2: Descargar el Dataset para Carrito :) 

rf = Roboflow(api_key=ROBOFLOW_KEY)
project = rf.workspace(workspace).project(project)
dataset = project.version(1).download("yolov8")

# 3. Entrenar el Modelo
    #batch=16 -> En caso, se tenga más memoria RAM.

if __name__ == '__main__':
    model = YOLO("yolov8n.pt")
    print("Comienza el Entrenamiento 🚗...")

    model.train(
        data=f"{dataset.location}/data.yaml",
        epochs=50,
        imgsz=640,
        device = tarjeta_grafica,
        batch=8,
        workers=2,
        cache=False,
        name='modelo_tesiproject_v1'
    )

    print("Felicidades Dre4m Te4m, es una niña...")
    print("Alto no... Eso no era, el carrito ha funcionado 🚗")
    print("Finalizado.")

