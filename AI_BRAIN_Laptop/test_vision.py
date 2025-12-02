from ultralytics import YOLO

# Paso N°01 -> Cargamos el Modelo NANO 
model = YOLO('yolov8n.pt')

# Usar source = 0 es la webcam integrado. Si es con USB es 1 
# show = true para desplegar nueva ventana
# Device = 0 fuerza el uso de la tarjeta gráfica

results = model.predict(source="0", show=True, device="0", stream=True)
for r in results:
    pass 