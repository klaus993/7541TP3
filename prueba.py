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
	return len(grafo.keys())


def calcular_aristas(grafo):
	'''Recibe un grafo y la cantidad de vertices que posee. Devuelve la cantidad
	de aristas que tiene y el promedio del grado de los vértices.'''
	cant_aristas = 0
	for vertice in grafo.keys():
		for adyacente in grafo.adyacentes(vertice):
			cant_aristas += 1
	cant_aristas //= 2
	return cant_aristas


def calcular_promedio_gr_vertices(grafo, cant_vertices):
	sumatoria_grados = 0
	for vertice in grafo.keys():
		sumatoria_grados += len(grafo.adyacentes(vertice))
	promedio_grados_vertices = sumatoria_grados / cant_vertices
	return promedio_grados_vertices

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
	return cant_aristas / cant_max_aristas


def estadisticas(grafo):
	'''Recibe un grafo e imprime por pantalla la cantidad de vértices y de 
	aristas que posee, el promedio del grado de los vértices, el desvío estándar
	del grado de los vértices y por último su densidad. '''
	cant_vertices = calcular_vertices(grafo)
	cant_aristas = calcular_aristas(grafo)
	promedio_grados_vertices = calcular_promedio_gr_vertices(grafo, cant_vertices)
	desvio_estandar = calcular_desvio_estandar(grafo, promedio_grados_vertices, cant_vertices)
	densidad = calcular_densidad(grafo, cant_vertices, cant_aristas)
	print("Cantidad de vértices: {}\nCantidad de aristas: {}\nPromedio del grado de cada vértice: {:.2f}\nDesvío estándar del grado de cada vértice: {:.2f}\nDensidad del grafo: {:.10f}".format(cant_vertices, cant_aristas, promedio_grados_vertices, desvio_estandar, densidad))


def label_propagation(grafo, label, corte):
	'''Recibe un grafo, un diccionario llamado label y un valor corte. Esta
	función realiza el algoritmo label propagation sobre label hasta que este se
	termina (en caso de que corte sea cero) o hasta que se llegue al número de 
	iteración indicado por corte. '''
	frecuencia = {}
	i = 0
	max_freq = 0
	vertice_max_freq = None
	iguales = True
	aux = {}
	vertice_min_label = None
	min_label = 6450 #para tomar como valor maximo, dsp podemos poner la cant de vertices + 1
	for clave, valor in label.items():
		for adyacente in grafo.adyacentes(clave):
			if not adyacente in frecuencia:
				frecuencia[adyacente] = 0
			frecuencia[adyacente] += 1
		for clave2, valor2 in frecuencia.items():
			if valor2 not in aux:
				aux[valor2] = clave2
		referente = valor2
		for frec in aux:
			if frec != referente:
				iguales = False
		if iguales:
			for adyacente in grafo.adyacentes(clave):
				if label[adyacente] < min_label:
					min_label = label[adyacente]
					vertice_min_label = adyacente
			if vertice_min_label:
				label[clave] = label[vertice_min_label]
				vertice_min_label = None
		else:
			for clave2, valor2 in aux.items():
				if clave2 > max_freq:
					max_freq = clave2
					vertice_max_freq = valor2
			if vertice_max_freq:
				label[clave] = label[vertice_max_freq]
				vertice_max_freq = None
				frecuencia = {}
				max_freq = 0
		iguales = True
		if corte:
			if i == corte:
				break
		i += 1

def comunidades(grafo, corte = 0):
	'''Recibe un grafo y un valor corte que determina si el algoritmo se hace 
	hasta un determinado corte o no y cuántas veces itera. Muestra por pantalla 
	las comunidades que se encuentran en el grafo. '''
	label_original = {}
	label_aux = {}
	i = 0
	for vertice in grafo.keys():
		label_original[vertice] = i
		i += 1
	label_aux = label_original
	while(True) :
		label_propagation(grafo, label_aux, corte)
		if(label_aux == label_original): break
		label_original = label_aux
	dic_comunidades = {}
	for clave, valor in label_original.items():
		if valor not in dic_comunidades:
			dic_comunidades[valor] = []
		dic_comunidades[valor].append(clave)
	numero_comunidad = 1
	for clave, valor in dic_comunidades.items():
		print("Comunidad " + str(numero_comunidad) + ":")
		for integrante in valor:
			print(integrante + " ")
		print("----------")
		numero_comunidad += 1 
		
def grafeo():
	grafo = Grafo()
	cantidad = grafo.__contains__("jorge")
	grafo.__setitem__("Fede",5)
	grafo.__setitem__("Martin",5)
	grafo.__setitem__("Gaston",4)
	grafo.__setitem__("Ezequiel",4)
	grafo.__setitem__("Agus",3)
	grafo.__setitem__("Mike",3)
	grafo.__setitem__("Nacho",3)
	grafo.__setitem__("Gonza",3)
	grafo.__setitem__("Cano",3)
	grafo.__setitem__("Joaquin",3)
	grafo.__setitem__("Juan",3)
	grafo.agregar_arista("Fede", "Martin")
	grafo.agregar_arista("Fede", "Gaston")
	grafo.agregar_arista("Fede", "Ezequiel")
	grafo.agregar_arista("Martin", "Agus")
	grafo.agregar_arista("Martin", "Mike")
	grafo.agregar_arista("Gaston", "Nacho")
	grafo.agregar_arista("Gaston", "Gonza")
	grafo.agregar_arista("Ezequiel", "Cano")
	grafo.agregar_arista("Cano", "Joaquin")
	grafo.agregar_arista("Martin", "Gaston")
	grafo.agregar_arista("Martin", "Ezequiel")
	grafo.agregar_arista("Joaquin", "Juan")
	comunidades(grafo)

distancias(grafo, "BLACK PANTHER")
