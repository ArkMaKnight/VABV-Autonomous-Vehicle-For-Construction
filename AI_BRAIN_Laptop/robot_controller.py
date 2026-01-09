import requests
import os, time
import threading

class RobotController:
    def __init__(self):
        self.base_url = os.getenv("ESP32_IP")
        self.api_key = os.getenv("API_KEY")
        self.last_send = 0
        self.endpoint = os.getenv("stream")

        if not self.base_url or not self.api_key:
            raise ValueError("Instancias no implementadas.")
    def _send_background(self, endpoint, command): 
        url = f"{self.base_url}:81/{endpoint}"
        payload = {
            "action": command,
            "auth": self.api_key
        }
        try: 
            response = requests.post(url, json = payload, timeout= 0.5)
            if response.status_code == 200:
                print("Ejecución realizada. Correcto")
                return True
            else: 
                print("Ejecución rechazada. ")
                return False
        except requests.exceptions.Timeout:
            print(f"Sin respuesta de robot. {command}")
        except Exception as e: 
            print(f"Hubo un error, error detectado: {e}")
        return False
    
    def _send_request(self, endpoint, command): 
        if time.time() - self.last_send < 0.5:
            return False

        self.last_send = time.time()
        thread = threading.Thread(target=self._send_background, args=(endpoint, command), daemon= True)
        thread.start()

        return True

    def stop(self):
        return self._send_request("control", "STOP")
    
    def forward(self):
        return self._send_request("control", "FORWARD")
    
    def alarm_detector(self):
        return self._send_request("control", "ALARM_ACTIVATED")
    
    def slow_speed(self):
        return self._send_request("control", "SLOW")
    


