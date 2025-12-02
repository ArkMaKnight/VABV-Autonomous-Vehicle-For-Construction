import torch

print("¿CUDA disponible?:", torch.cuda.is_available())

if torch.cuda.is_available():
    print("¡ÉXITO! Ahora usando:", torch.cuda.get_device_name(0))
    print("Versión de CUDA:", torch.version.cuda)
else:
    print("Sigue saliendo CPU... avísame si pasa esto.")