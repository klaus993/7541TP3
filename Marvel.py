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
	> centralidad_rw [cantidad] (centralidad por random walks)\n\
	> centralidad_exacta [cantidad] (centralidad exacta por camínos mínimos)\n\
	> distancias <personaje>\n\
	> estadisticas\n\
	> comunidades\n\
	> salir o Ctrl-D para salir"


def main():
	'''Flujo principal. Menú de opciones.
	Manejo de excepciones por mala entrada de usuario y validación del archivo.
	El programa termina en caso de ingresarse "salir" o lanzar EOFError (Ctrl-D).
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
			if com_tup[0] == LISTA_COMANDOS[1]:
				camino(grafo, com_tup[1], com_tup[2])
			elif com_tup[0] == LISTA_COMANDOS[2]:
				recomendar(grafo, com_tup[1], com_tup[2])
			elif com_tup[0] == LISTA_COMANDOS[3]:
				similares(grafo, com_tup[1], com_tup[2])
			elif com_tup[0] == LISTA_COMANDOS[4]:
				centralidad_random_walks(grafo, com_tup[1])
			elif com_tup[0] == LISTA_COMANDOS[5]:
				centralidad_exacta(grafo, com_tup[1])
			elif com_tup[0] == LISTA_COMANDOS[6]:
				distancias(grafo, com_tup[1])
			elif com_tup[0] == LISTA_COMANDOS[7]:
				estadisticas(grafo)
			elif com_tup[0] == LISTA_COMANDOS[8]:
				comunidades(grafo)
			elif com_tup[0] == LISTA_COMANDOS[0]:
				pass
			elif com_tup[0] == LISTA_COMANDOS[9]:
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
