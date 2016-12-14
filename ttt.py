from parse import *
from comandos import *

grafo = parse("marvel.pjk")

x = generar_caminos_minimos(grafo)
