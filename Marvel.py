#!/usr/bin/python3

from time import sleep
from parse import parse
from grafo import Grafo
from comandos import *

USO = "Uso:\n\
	> similares <personaje> [cantidad]\n\
	> recomendar <personaje> [cantidad]\n\
	> camino <personaje_1> <personaje_2>\n\
	> centralidad [cantidad]\n\
	> distancias <personaje>\n\
	> estadisticas\n\
	> comunidades\n\
	> salir"


def main():
	print("¡Bienvenido al mundo de Marvel!")
	print(USO)
	grafo = parse("marvel.pjk")
	while True:
		try:
			comando = input("> ")
			if not validar_comando(comando):
				print(USO)
				continue
			param = comando[len("camino") + 1:].split(", ")
			if comando.split(" ")[0] == "camino" and len(param) == 2:
				camino(grafo, param[0], param[1])
			elif comando == "salir":
				return
		except (KeyboardInterrupt, EOFError):
			print()
			continue

if __name__ == "__main__":
	main()
