#!/usr/bin/python3

from parse import parse
from grafo import Grafo
from comandos import *
import sys

USO_PROG = "Uso: {} <archivo>"

USO_COM = "Uso:\n\
	> similares <personaje>, [cantidad]\n\
	> recomendar <personaje>, [cantidad]\n\
	> camino <personaje_1>, <personaje_2>\n\
	> centralidad [cantidad]\n\
	> distancias <personaje>\n\
	> estadisticas\n\
	> comunidades\n\
	> salir o Ctrl-D para salir"


def main():
	'''
	'''
	try:
		if sys.argv[1][-3:] != "pjk":
			print("El archivo indicado debe ser formato pajek (.pjk)")
			return
	except IndexError:
		print(USO_PROG.format(sys.argv[0]))
		return
	try:
		grafo = parse(sys.argv[1])
	except FileNotFoundError:
		print("El archivo {} no existe.".format(sys.argv[1]))
		return
	print("¡Bienvenido al mundo de Marvel!")
	print(USO_COM)
	while True:
		try:
			comando = input("> ")
			if not validar_comando(comando):
				print(USO_COM)
				continue
			com_tup = validar_comandos(comando)
			if com_tup[0] == "camino":
				camino(grafo, com_tup[1], com_tup[2])
			elif com_tup[0] == "recomendar":
				recomendar(grafo, com_tup[1], com_tup[2])
			elif com_tup[0] == "similares":
				similares(grafo, com_tup[1], com_tup[2])
			elif com_tup[0] == "centralidad":
				centralidad(grafo, com_tup[1])
			elif com_tup[0] == "distancias":
				distancias(grafo, com_tup[1])
			elif com_tup[0] == "estadisticas":
				estadisticas(grafo)
			elif com_tup[0] == "comunidades":
				comunidades(grafo)
			elif com_tup[0] == "":
				pass
			elif com_tup[0] == "salir":
				return
			else:
				print(USO_COM)
		except KeyboardInterrupt:
			print()
			continue
		except EOFError:
			print()
			return


if __name__ == "__main__":
	main()
