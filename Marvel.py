#!/usr/bin/python3

from time import sleep
from parse import parse
from grafo import Grafo
from comandos import *
import sys

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
	'''Main. Hay que arreglar los if, elif, etc ya que las validaciones de cada comando son un choclo.
	Habría que ponerlas en funciones aparte, pero lo voy a hacer al final porque no es algo crucial, son detalles.
	El try except es por si el usuario toca Control+C o Control+D, para que no termine el programa.
	'''
	try:
		if sys.argv[1][-3:] != "pjk":
			print("El archivo indicado debe ser formato pajek (.pjk)")
			return
	except IndexError:
		print("Uso: {} <archivo>".format(sys.argv[0]))
		return
	try:
		grafo = parse(sys.argv[1])
	except FileNotFoundError:
		print("El archivo {} no existe.".format(sys.argv[1]))
		return
	print("¡Bienvenido al mundo de Marvel!")
	print(USO)
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
				recomendar(grafo, param[0], int(param[1]))
			elif com == "similares" and len(comando[len("similares") + 1:].split(", ")) == 2 and comando[len("similares") + 1:].split(", ")[1].isdigit():
				param = param = comando[len("similares") + 1:].split(", ")
				similares(grafo, param[0], int(param[1]))
			elif com == "centralidad" and len(comando[len("centralidad") + 1:].split(", ")) == 1:
				param = param = comando[len("centralidad") + 1:].split(", ")
				centralidad(grafo, int(param[0]))
			elif com == "distancias" and len(comando[len("distancias") + 1:].split(", ")) == 1:
				param = param = comando[len("centralidad") + 1:].split(", ")
				distancias(grafo, param[0])
				
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
