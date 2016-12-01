from grafo import *

def parse(file):
	''' Parsea un archivo .pjk (que posee labels y pesos) a una estructura Grafo.
	Primero se agregan los vértices, siendo:
	- line[0] el número de arista,
	- line[1] el label.
	Luego se agregan las aristas, siendo:
	- line[0] el vértice origen,
	- line[1] el vértice destino,
	- line[2] el peso.
	Devuelve el grafo.
	'''
	grafo = Grafo()
	vert_dict = {}									# Diccionario de vértices con su número de vértice usado para
	with open(file, "r") as f:						# luego agregar las aristas según el número de vértice.
		vertices = int(f.readline().split(' ')[1])  # Cantidad de vertices
		for line in f:								# Agrega los vertices
			line = line.split('"')
			grafo[line[1]] = {}
			vert_dict[int(line[0])] = line[1]
			if int(line[0]) == vertices:			# Corta cuando llega al número de aristas predefinido
				break
		f.readline()
		for line in f:								# Agrega las aristas
			line = line.split(' ')
			line = [int(i) for i in line]
			grafo.agregar_arista(vert_dict[line[0]], vert_dict[line[1]], line[2])
	return grafo
