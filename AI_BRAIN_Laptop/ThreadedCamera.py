# Clase para manejar stream MJPEG del ESP32-CAM
import threading, urllib
import time, cv2, numpy as np

class ThreadedESP32Camera:
    def __init__(self, url):
        self.url = url
        self.stream = None
        self.bytes_buffer = b''
        self.current_frame = None
        self._opened = False
        self._connected = False
        self._stop = False
        self._frame_id = 0
        self.real_fps = 0.0
        self._fps_count = 0
        self._fps_timer = time.perf_counter()
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()
    
    def _do_connect(self):  
        try:
            if self.stream: 
                try: self.stream.close()
                except: pass
            print(f"🔄 Conectando a {self.url}...")
            self.stream = urllib.request.urlopen(self.url, timeout=30)
            self._connected = True
            self._opened = True
            print("✅ Cámara ESP32 conectada correctamente")
            return True
        except Exception as e:
            print(f"❌ Error conectando a ESP32: {e}")
            self._connected = False
            time.sleep(2)
            return False
    
    def status_connection(self):
        frame = self.read()
        return frame is not None
    
    def update(self): 
        while not self._stop: 
            if not self._connected: 
                self._do_connect()
                continue
            try: 
                chunk = self.stream.read(4096)
                if not chunk: 
                    self._connected = False
                    continue

                self.bytes_buffer += chunk

                if len(self.bytes_buffer) > 40000:
                    self.bytes_buffer = b''
                    continue
                
                start = self.bytes_buffer.find(b'\xff\xd8')
                end = self.bytes_buffer.find(b'\xff\xd9')

                if start != -1 and end != -1: 
                    jpg = self.bytes_buffer[start:end+2]
                    self.bytes_buffer = self.bytes_buffer[end+2:]
                    try:
                        frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                        if frame is not None: 
                            self.current_frame = frame
                            self._frame_id += 1
                            self._fps_count += 1
                            now = time.perf_counter()
                            elapsed = now - self._fps_timer
                            if elapsed >= 1.0:
                                self.real_fps = round(self._fps_count / elapsed, 1)
                                self._fps_count = 0
                                self._fps_timer = now
                    except:
                        pass 
            except Exception as e:
                print(f"⚠️ Error leyendo frame: {e}, reconectando...")
                self._connected = False
                self.bytes_buffer = b''
                    
    def read(self):
        return self.current_frame

    def get_frame_id(self):
        return self._frame_id
    
    def stop(self):
        self._stop = True