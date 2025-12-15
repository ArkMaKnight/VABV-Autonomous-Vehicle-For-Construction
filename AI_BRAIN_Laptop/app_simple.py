"""App Flask simple sin YOLO para probar streaming"""
from flask import Flask, Response
import cv2

app = Flask(__name__)
camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

def generate_frame(): 
    frame_count = 0
    while True: 
        success, frame = camera.read()
        frame_count += 1
        
        if not success:
            print(f"❌ Error leyendo frame {frame_count}")
            break
        
        print(f"✓ Frame {frame_count}: {frame.shape}, min={frame.min()}, max={frame.max()}")
        
        # Solo añadir texto
        cv2.putText(frame, f"FRAME {frame_count}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Codificar
        ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
        if not ret:
            print(f"❌ Error codificando frame {frame_count}")
            continue
        
        frame_bytes = buffer.tobytes()
        print(f"✓ Enviando {len(frame_bytes)} bytes")
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + 
               frame_bytes + b'\r\n')

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head><title>Test Cámara 2</title></head>
    <body style="background: #222; color: white; text-align: center;">
        <h1>Test Stream Cámara</h1>
        <img src="/video_feed" width="640" height="480" style="border: 3px solid lime;">
    </body>
    </html>
    '''

@app.route('/video_feed')
def video_feed():
    return Response(generate_frame(), 
                   mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    print("Servidor simple en http://127.0.0.1:5001/")
    app.run(host='0.0.0.0', port=5001, debug=False)
