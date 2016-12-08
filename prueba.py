from parse import *
from grafo import *
import math

grafo = parse("marvel.pjk")


def generar_distancias(v, padre, orden, dic_distancias):
	if orden[v] not in dic_distancias:
		dic_distancias[orden[v]] = 0
	if padre[v]:
		dic_distancias[orden[v]] += 1
	if orden[v] == 1 and dic_distancias[1] > 724:
		print(v)

def distancias(grafo, personaje):
	''' Recibe un grafo y el identificador de un vértice. Imprime por pantalla
	la cantidad de personajes que se encuentran a cada una de las distancias
	posibles. '''
	dic_distancias = {}
	grafo.recorrer("bfs", generar_distancias, dic_distancias, personaje)
	for clave,valor in dic_distancias.items():
		print("Distancia "+ str(clave)+": "+str(valor))

def contar_dist1(grafo, personaje):
	dic_distancias = {}
	padre, orden = grafo.recorrer("bfs", None, None,personaje)
	dic_dist = {}
	for clave,valor in orden.items():
		if valor not in dic_dist:
			dic_dist[valor] = []
		dic_dist[valor].append(clave)
	for clave,valor in dic_dist.items():
		print("Distancia "+ str(clave)+": "+str(len(valor)))

def calcular_vertices(grafo):
	'''Recibe un grafo y calcula su cantidad de vértices. '''
	lista_idvertices = grafo.keys()
	return len(lista_idvertices)

def calcular_aristas_y_promedio_gr_vert(grafo, cant_vertices):
	'''Recibe un grafo y la cantidad de vertices que posee. Devuelve la cantidad
	de aristas que tiene y el promedio del grado de los vértices.'''
	cant_aristas = 0
	sumatoria_grados = 0
	for vertice in grafo.keys():
		sumatoria_grados += len(grafo.adyacentes(vertice))
		for adyacente in grafo.adyacentes(vertice):
			cant_aristas += 1
	cant_aristas //= 2
	promedio_grados_vertices = sumatoria_grados / cant_vertices	
	return cant_aristas, promedio_grados_vertices

def calcular_desvio_estandar(grafo, promedio_grados_vertices, cant_vertices):
	'''Recibe un grafo junto a su cantidad de vértices y a su promedio del grado
	de los vértices y devuelve el desvío estándar del grado de los vértices. '''
	sumatoria_numerador = 0
	for vertice in grafo.keys():
		sumatoria_numerador +=  ((len(grafo.adyacentes(vertice)) - promedio_grados_vertices)**2)
	return math.sqrt(sumatoria_numerador / (cant_vertices - 1)) 
	
def calcular_densidad(grafo, cant_vertices, cant_aristas):
	'''Recibe un grafo junto a su cantidad de vertices y de aristas y devuelve
	su densidad. '''
	cant_max_aristas = cant_vertices * (cant_vertices - 1) / 2
	densidad = cant_aristas / cant_max_aristas
	return densidad
	

def estadisticas(grafo):
	'''Recibe un grafo e imprime por pantalla la cantidad de vértices y de 
	aristas que posee, el promedio del grado de los vértices, el desvío estándar
	del grado de los vértices y por último su densidad. '''
	cant_vertices = calcular_vertices(grafo)
	cant_aristas, promedio_grados_vertices = calcular_aristas_y_promedio_gr_vert(grafo, cant_vertices)
	desvio_estandar = calcular_desvio_estandar(grafo, promedio_grados_vertices, cant_vertices)
	densidad = calcular_densidad(grafo, cant_vertices, cant_aristas)
	print("Cantidad de vértices: {}\nCantidad de aristas: {}\nPromedio del grado de cada vértice: {}\nDesvío estándar del grado de cada vértice: {}\nDensidad del grafo: {}".format(cant_vertices, cant_aristas, promedio_grados_vertices, desvio_estandar, densidad))
		

estadisticas(grafo)
