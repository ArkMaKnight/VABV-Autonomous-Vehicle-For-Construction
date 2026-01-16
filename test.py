import cv2
import urllib.request
import numpy as np

# URL del ESP32-CAM
URL_DIRECTA = "http://10.1.77.15:81/stream"

print(f"Conectando a: {URL_DIRECTA} ...")

# Método 1: Intentar con diferentes backends de OpenCV
def try_opencv_backends():
    backends = [
        (cv2.CAP_ANY, "CAP_ANY (auto)"),
        (cv2.CAP_FFMPEG, "CAP_FFMPEG"),
        (cv2.CAP_GSTREAMER, "CAP_GSTREAMER"),
    ]
    
    for backend, name in backends:
        print(f"   Probando {name}...")
        cap = cv2.VideoCapture(URL_DIRECTA, backend)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Reduce buffer lag
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print(f"✅ ¡ÉXITO con {name}!")
                return cap
            cap.release()
    return None

# Método 2: Usar urllib para leer el stream MJPEG manualmente
def stream_manual():
    print("   Usando método manual (urllib)...")
    stream = urllib.request.urlopen(URL_DIRECTA, timeout=10)
    bytes_buffer = b''
    
    print("✅ ¡ÉXITO con método manual! Presiona 'q' para salir.")
    
    while True:
        bytes_buffer += stream.read(4096)
        
        # Buscar inicio y fin del frame JPEG
        start = bytes_buffer.find(b'\xff\xd8')  # SOI marker
        end = bytes_buffer.find(b'\xff\xd9')    # EOI marker
        
        if start != -1 and end != -1 and end > start:
            jpg = bytes_buffer[start:end+2]
            bytes_buffer = bytes_buffer[end+2:]
            
            # Decodificar JPEG
            frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
            
            if frame is not None:
                cv2.imshow("ESP32-CAM Stream", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
    
    stream.close()
    cv2.destroyAllWindows()

# Intentar primero con OpenCV, si falla usar método manual
cap = try_opencv_backends()

if cap is not None:
    print("Presiona 'q' para salir.")
    while True:
        ret, frame = cap.read()
        if ret:
            cv2.imshow("ESP32-CAM Stream", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print("⚠️ Frame perdido")
    cap.release()
    cv2.destroyAllWindows()
else:
    print("❌ OpenCV backends fallaron, usando método alternativo...")
    try:
        stream_manual()
    except Exception as e:
        print(f"❌ Error: {e}")
        print("   -> ¿Está el navegador abierto? CIÉRRALO.")
        print("   -> ¿La IP cambió? Revisa el Monitor Serie.")