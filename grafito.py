from grafo import *

def visitar(v, padre, orden, extra):
	print("Vértice: "+v)
	print("Padre: "+padre[v])

def grafeo():
	grafo = Grafo()
	cantidad = grafo.__contains__("jorge")
	print(cantidad)
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
	distancias(grafo,"Fede")

def generar_distancias(v, padre, orden, dic_distancias):
	if orden[v] not in dic_distancias:
		dic_distancias[orden[v]] = 0
	dic_distancias[orden[v]] += 1

def distancias(grafo, personaje):
	''' Recibe un grafo y el identificador de un vértice. Imprime por pantalla
	la cantidad de personajes que se encuentran a cada una de las distancias
	posibles. '''
	dic_distancias = {}
	grafo.recorrer("bfs", generar_distancias, dic_distancias, personaje)
	for clave,valor in dic_distancias.items():
		print("Distancia "+ str(clave)+": "+str(valor))


grafeo()
