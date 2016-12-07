from parse import *
from Marvel import *
from grafo import *

grafo = parse("marvel.pjk")

def contador(dic, indice):
	dic[indice] = "caca"

def generar_distancias(v, padre, orden, distancias):
	if padre != distancias[0][0]:
		distancias[1][v] = {}
		distancias[1][v][padre] = (, 0) 
		distancias[0][1] += 1
		distancias[0][0] = padre
	if padre != None:
		distancias[1][distancias[0][1]] += 1

def distancias(grafo, personaje):
	''' Recibe un grafo y el identificador de un vértice. Imprime por pantalla
	la cantidad de personajes que se encuentran a cada una de las distancias
	posibles. '''
	dic_distancias = {}
	distancias = [[0, 1], dic_distancias] 
	grafo.recorrer("bfs", generar_distancias, distancias, personaje)
	for clave,valor in distancias[1].items():
		print("Distancia "+ str(clave)+": "+str(valor))

distancias(grafo, "HULK")

main()
