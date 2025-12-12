import cv2

camera_integrated = 0

cap = cv2.VideoCapture(camera_integrated, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("Error ARTURO en encontrar la cámara", camera_integrated)
else: 
    print(f"Cámara {camera_integrated} detectada")

while True: 
    ret, frame = cap.read()
    if not ret:
        print("No se recibe una imagen.")
        print("Saliendo...")
        break
    
    cv2.imshow('Prueba de cámara', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows() 