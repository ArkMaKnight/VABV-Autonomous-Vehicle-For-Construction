import time
from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class TelemetryData:
    person: int = 0
    vest: int = 0
    hard_hat: int = 0
    animal: int = 0
    objects: int = 0
    uptime: str = "00:00:00"
    latency: int = 0
    packet_loss: int = 0
    camera_connected: bool = False
    wheels_connected: bool = False
    
    def to_dict(self):
        return asdict(self)

class TelemetryService:
    def __init__(self, start_time: float):
        self.start_time = start_time
        self.last_emit_time = start_time
        self._data = TelemetryData()
    
    def update_detection(self, person=0, vest=0, hard_hat=0, animal=0, objects=0):
        self._data.person = person
        self._data.vest = vest
        self._data.hard_hat = hard_hat
        self._data.animal = animal
        self._data.objects = objects
    
    def get_telemetry(self) -> dict:
        current = time.time()
        self._data.latency = int((current - self.last_emit_time) * 1000)
        self._data.uptime = self._calculate_uptime()
        self.last_emit_time = current
        return self._data.to_dict()
    
    def _calculate_uptime(self) -> str:
        seconds = int(time.time() - self.start_time)
        h, r = divmod(seconds, 3600)
        m, s = divmod(r, 60)
        return f"{h:02d}:{m:02d}:{s:02d}"