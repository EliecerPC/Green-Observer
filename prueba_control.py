
from core.parametros import Parametros
from core.control import Controlador

p = Parametros()
controlador = Controlador(p)

eventos = controlador.evaluar(
    tiempo=0,
    temperatura=31,
    humedad=35,
    luz_natural=10,
    hora=10
)

for evento in eventos:
    print(evento)
