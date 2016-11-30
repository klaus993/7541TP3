from grafo import *

def parse(file):
	''' Parsea un archivo .pjk (que posee labels y pesos) en una estructura Grafo.
	'''
	grafo = Grafo()
	vert_dict = {}
	with open(file, "r") as f:
		vertices = int(f.readline().split(' ')[1])  # Cantidad de vertices
		for line in f:								# Agrega los vertices
			line = line.split('"')					# line[0] es el número de arista
			grafo[line[1]] = {}						# line[1] es el label
			vert_dict[int(line[0])] = line[1]
			if int(line[0]) == vertices:			# Corta cuando llega al número de aristas predefinido
				break
		f.readline()
		for line in f:								# Agrega las aristas
			line = line.split(' ')
			line = [int(i) for i in line]
			grafo.agregar_arista(vert_dict[line[0]], vert_dict[line[1]], line[2])
	return grafo
