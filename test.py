import cv2

# ⚠️ PON AQUÍ TU IP DIRECTAMENTE (Sin .env para descartar errores)
# Asegúrate de poner :81/stream al final
URL_DIRECTA = "http://10.1.77.15:81/stream" 

print(f"Conectando a: {URL_DIRECTA} ...")

cap = cv2.VideoCapture(URL_DIRECTA, cv2.CAP_FFMPEG)

if not cap.isOpened():
    print("❌ FALLÓ: OpenCV no puede abrir la cámara.")
    print("   -> ¿Está el navegador abierto? CIÉRRALO.")
    print("   -> ¿La IP cambió? Revisa el Monitor Serie.")
else:
    print("✅ ¡ÉXITO! Cámara funcionando. Presiona 'q' para salir.")
    
    while True:
        ret, frame = cap.read()
        if ret:
            cv2.imshow("PRUEBA", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print("⚠️ Frame perdido (Lag)")

cap.release()
# Scv2.destroyAllWindows()