from ultralytics import YOLO
from roboflow import Roboflow
import torch

tarjeta_grafica = 0
# Verificamos que use RTX4060
print("¿CUDA disponible?:", torch.cuda.is_available())

#2: Descargar el Dataset para Carrito :) 

if torch.cuda.is_available():
    print("¡ÉXITO! Ahora usando:", torch.cuda.get_device_name(tarjeta_grafica))
    print("Versión de CUDA:", torch.version.cuda)
else:
    print("Sigue saliendo CPU... avísame si pasa esto.")

rf = Roboflow(api_key="")
project = rf.workspace("...").project("...")
dataset = project.version(1).download("yolov8")

# 3. Entrenar el Modelo
if __name__ = '__main__':
    model = YOLO("yolov8n.pt")
    print("Comienza el Entrenamiento 🚗...")

    model.train(
        data=f"{dataset.location}/data.yaml",
        epochs=50,
        imgsz=640,
        device = tarjeta_grafica,
        batch=16
        name='modelo_tesiproject_v1'
    )

    print("Felicidades Dre4m Te4m, es una niña...")
    print("Alto no... Eso no era, el carrito ha funcionado 🚗")
    print("Finalizado.")