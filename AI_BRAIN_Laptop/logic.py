from robot_controller import RobotController
from colors_detection import colorsDetections

robot = RobotController
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
        

def test_movement_security(count_person, count_hardhat, count_vest, detect_stop, detect_objects, timeout_epp):
    if (count_person > 0):
        current_frame = (count_hardhat > 0 & count_vest > 0)

        if current_frame: 
            permission_personal = colorsDetections.green_color
            timeout_epp = 0
            msg_output = success_text
            print(msg_output)
            print("DISMINUYENDO LA VELOCIDAD....")
            action = "SLOW"
            if detect_stop:
                action = "STOP"
                msg_output = stop_text
                print(f"{msg_output}: {action}")
                permission_personal = colorsDetections.yellow_color
            else: 
                action = "FORWARD"
                msg_output = no_detection_text
                print(f"{msg_output}: {action}")
                return permission_personal, action
            return permission_personal, action
        else: 
            timeout_epp +=1
            permission_personal = colorsDetections.red_color
            msg_output = fail_text
            print(msg_output)
            return permission_personal, "STOP"
        
    else: 
        if detect_objects: 
            print("Esperando por más instrucciones...")
            print("Se han detecado objetos en la vía.")
            return "STOP"
        print(no_detection_text)
        return colorsDetections.gray_color, "FORWARD"
