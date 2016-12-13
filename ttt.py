from comandos import *
from grafo import *
from parse import *


grafo = parse("marvel.pjk")
camino(grafo, "SPIDER-MAN", "IRON MAN")
