import requests
import os, time
import threading

class RobotController:
    def __init__(self):
        self.base_url = os.getenv("ESP32_IP")
        self.api_key = os.getenv("API_KEY")
        self.last_send = 0
        self.endpoint = os.getenv("ENDPOINT_VIDEO")
        self.is_connected = False

        if not self.base_url or not self.api_key:
            raise ValueError("Instancias no implementadas.")
        
    def _send_background(self, endpoint, command): 
        url = f"{self.base_url}:81/{endpoint}"
        if endpoint == 'control':
            url = f"{self.base_url}/control"

        payload = {
            "action": command,
            "auth": self.api_key
        }
        try: 
            response = requests.post(url, json = payload, timeout= 0.5)
            if response.status_code == 200:
                self.is_connected = True
                print("Ejecución realizada. Correcto")
                return True
            else: 
                print("Ejecución rechazada. ")
                return False
        except requests.exceptions.Timeout:
            self.is_connected = False
            print(f"Sin respuesta de robot. {command}")
        except Exception as e: 
            self.is_connected = False
            print(f"Hubo un error, error detectado: {e}")
        return False
    

    def _send_request(self, endpoint, command): 
        # STOP siempre se envía inmediatamente, otros comandos tienen cooldown de 100ms
        if command != "STOP" and time.time() - self.last_send < 0.1:
            return False

        self.last_send = time.time()
        thread = threading.Thread(target=self._send_background, args=(endpoint, command), daemon= True)
        thread.start()

        return True
    def set_speed(self, speed_value):
        speed_value = max(0, min(255, int(speed_value)))
        url = f"{self.base_url}/control"
        payload = {
            "action": "SPEED",
            "value": speed_value,
            "auth": self.api_key
        }
        try: 
            requests.post(url, json=payload, timeout=0.5)
            return True
        except:
            return False

    def stop(self):
        return self._send_request("control", "STOP")
    
    def forward(self):
        return self._send_request("control", "FORWARD")
    
    def backward(self):
        return self._send_request("control", "BACKWARD")
    
    def turn_left(self):
        return self._send_request("control", "LEFT")
    
    def turn_right(self):
        return self._send_request("control", "RIGHT")
    
    def alarm_detector(self):
        return self._send_request("control", "ALARM_ACTIVATED")
    
    def slow_speed(self):
        return self._send_request("control", "SLOW")
    


