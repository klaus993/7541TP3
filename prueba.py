from parse import *
from grafo import *

grafo = parse("marvel.pjk")


def generar_distancias(v, padre, orden, distancias):
	if not padre:
		distancias[1][0] = 0 #diccionario distancia: contador
		return
	elif padre != distancias[0][0]:
		if distancias[0][1] not in distancias[1]:
			distancias[1][distancias[0][1]] = 0
			distancias[0][1] += 1
		distancias[0][0] = padre
	distancias[1][distancias[0][1] - 1] += 1

def distancias(grafo, personaje):
	''' Recibe un grafo y el identificador de un vértice. Imprime por pantalla
	la cantidad de personajes que se encuentran a cada una de las distancias
	posibles. '''
	dic_distancias = {}
	distancias = [[None, 1], dic_distancias] 
	grafo.recorrer("bfs", generar_distancias, distancias, personaje)
	for clave,valor in distancias[1].items():
		print("Distancia "+ str(clave)+": "+str(valor))

distancias(grafo, "BLACK PANTHER")
