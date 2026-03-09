from colors_detection import colorsDetections
LIMIT_EPP_TIMEOUT = 5 
success_text = "EQUIPOS DE PROTECCIÓN Y DE SEGURIDAD DETECTADA..."
fail_text = "NO SE DETECTÓ EQUIPOS DE PROTECCIÓN EPP. - ACTIVANDO ALARMA..."
stop_text = "SE DETECTÓ SEÑAL DE PARE. PARANDO VEHÍCULO..."
no_detection_text = "ZONA DESPEJADA. No se encuentran personas"

def test_security(data: dict = None) -> tuple[bool, str]:

    if not data:
        return True, "SIN DATOS"
    
    person = data.get('person', 0)
    hard_hat = data.get('hard_hat', 0)
    vest = data.get('vest', 0)
    
    if person == 0:
        return True, "NO HAY PERSONAS EN EL ÁREA"
    
    if hard_hat >= person and vest >= person:
        return True, "SE HAN DETECTADO EQUIPOS DE PROTECCIÓN"
    
    return False, "NO SE HAN DETECTADO EQUIPOS DE PROTECCIÓN"
    
def test_people(count_people, timeout_person, limit_timeout):
    print(f"{timeout_person}, {limit_timeout}, {count_people}")
    if count_people > 0:
        timeout_person = 0
    else:
        timeout_person +=1
        if timeout_person > limit_timeout:
            timeout_person = limit_timeout
    return timeout_person, limit_timeout
        
def test_movement_security(detections, timeout_epp):
    """
    Evalúa el entorno basándose en la jerarquía de seguridad minera/construcción.
    detections: Diccionario con el conteo de cada clase detectada en el frame actual.
    """
    # Extraer conteos del diccionario (si no existe la llave, asume 0)
    person = detections.get('person', 0)
    hard_hat = detections.get('hard_hat', 0)
    vest = detections.get('vest', 0)
    animal = detections.get('animal', 0)
    stop_sign = detections.get('stop_sign', 0)
    arrow_left = detections.get('arrow_left', 0)
    arrow_right = detections.get('arrow_right', 0)
    objects = detections.get('objects', 0)

    # ==========================================
    # PRIORIDAD 0: REVISIÓN DE EPP (SEGURIDAD INDUSTRIAL)
    # ==========================================
    if person > 0:

        has_epp = (hard_hat >= person) and (vest >= person)
        if not has_epp:
            timeout_epp += 1
            if timeout_epp >= LIMIT_EPP_TIMEOUT:
                print("¡ALERTA! Personal sin EPP detectado. Deteniendo operaciones y activando alarma.")
                return "PERSONA(S) SIN EPP DETECTADA AL FRENTE", colorsDetections.red_color, "ALARM", timeout_epp
            else:
                return "PERSONA(S) CON EPP DETECTADA AL FRENTE", colorsDetections.yellow_color, "STOP", timeout_epp
        else:
            timeout_epp = 0
    else:
        timeout_epp = 0

    # ==========================================
    # PRIORIDAD 1: ANTI-COLISIÓN (VIDA)
    # ==========================================
    
    if person > 0 or animal > 0:
        print("Obstáculo vivo en la ruta. FRENANDO para evitar atropello.")
        return "PARADO PARA EVITAR ACCIDENTE", colorsDetections.yellow_color, "STOP", timeout_epp

    # ==========================================
    # PRIORIDAD 2: SEÑALIZACIÓN Y TRÁFICO
    # ==========================================
    if stop_sign > 0:
        print("Señal de PARE detectada. FRENANDO.")
        return "PARADO POR SEÑAL", colorsDetections.red_color, "STOP", timeout_epp
        
    if arrow_left > 0:
        print("Señal de DESVÍO: Girando a la IZQUIERDA.")
        return "GIRANDO IZQUIERDA", colorsDetections.blue_color, "LEFT", timeout_epp
        
    if arrow_right > 0:
        print("Señal de DESVÍO: Girando a la DERECHA.")
        return "GIRADO DERECHA", colorsDetections.blue_color, "RIGHT", timeout_epp

    # ==========================================
    # PRIORIDAD 3: CONDICIONES DE LA VÍA (OBSTÁCULOS)
    # ==========================================
    if objects > 0:
        print("Zona de desmonte/obstáculos. Reduciendo velocidad.")
        return "BAJANDO VELOCIDAD" ,colorsDetections.yellow_color, "SLOW", timeout_epp

    # ==========================================
    # PRIORIDAD 4: VÍA LIBRE
    # ==========================================
    print("Vía despejada. Operación normal de transporte.")
    return "AVANZANDO...", colorsDetections.green_color, "FORWARD", timeout_epp