#!/usr/bin/python3

from time import sleep
from parse import parse
from grafo import Grafo
from comandos import *

USO = "Uso:\n\
	> similares <personaje>, [cantidad]\n\
	> recomendar <personaje>, [cantidad]\n\
	> camino <personaje_1>, <personaje_2>\n\
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
			com = comando.split(" ")[0]
			param = comando[len("camino") + 1:].split(", ")
			if com == "camino" and len(param) == 2:
				camino(grafo, param[0], param[1])
			elif com == "recomendar" and len(comando[len("recomendar") + 1:].split(", ")) == 2 and comando[len("recomendar") + 1:].split(", ")[1].isdigit():
				param = comando[len("recomendar") + 1:].split(", ")
				similares(grafo, param[0], int(param[1]), 500, 30, adyacentes=False)
			elif com == "similares" and len(comando[len("recomendar") + 1:].split(", ")) == 2 and comando[len("recomendar") + 1:].split(", ")[1].isdigit():
				param = param = comando[len("similares") + 1:].split(", ")
				similares(grafo, param[0], int(param[1]), 500, 50, adyacentes=True)
			elif com == "centralidad" and len(comando[len("centralidad") + 1:].split(", ")) == 1:
				param = param = comando[len("centralidad") + 1:].split(", ")
				similares(grafo, None, int(param[0]), 500, 500, adyacentes=True)
			elif com == "distancias":
				pass
			elif com == "estadisticas":
				pass
			elif com == "comunidades":
				pass
			elif com == "":
				pass
			elif comando == "salir":
				return
			else:
				print(USO)
		except (KeyboardInterrupt, EOFError):
			print()
			continue

if __name__ == "__main__":
	main()
