from queue import *
from heapq import *
from itertools import repeat
from collections import Counter
import random
import pdb

INFINITO = float('inf')

visitar_nulo = lambda a, b, c, d: True
heuristica_nula = lambda actual, destino: 0

VS_NOT_FOUND = "Algun/ambos vertice/s pasados no se encuentra/n en el grafo"
V_NOT_FOUND = "El vertice {} no se encuentra en el grafo."
A_NOT_FOUND = "La arista a borrar no se encuentra en el grafo."

class Grafo(object):
	'''Clase que representa un grafo. El grafo puede ser dirigido, o no, y puede no indicarsele peso a las aristas
	(se comportara como peso = 1). Implementado como "diccionario de diccionarios"'''

	def __init__(self, es_dirigido=False):
		'''Crea el grafo. El parametro 'es_dirigido' indica si sera dirigido, o no.'''
		if not isinstance(es_dirigido, bool):
			raise TypeError("{} debe ser un valor booleano".format(es_dirigido))
		self.dirigido = es_dirigido
		self.vertices = {}

	def __str__(self):
		return str(self.vertices)

	def __repr__(self):
		return str(self)

	def __len__(self):
		'''Devuelve la cantidad de vertices del grafo'''
		cant_vertices = 0
		for vertice in self.vertices:
			cant_vertices += 1
		return cant_vertices

	def __iter__(self):
		'''Devuelve un iterador de vertices, sin ningun tipo de relacion entre los consecutivos'''
		return iter(self.vertices)

	def keys(self):
		'''Devuelve una lista de identificadores de vertices. Iterar sobre ellos es equivalente a iterar sobre el grafo.'''
		lista_idvertices = []
		for vertice in self.vertices:
			lista_idvertices.append(vertice)
		return lista_idvertices

	def __getitem__(self, id):
		'''Devuelve el valor del vertice asociado, del identificador indicado. Si no existe el identificador en el grafo, lanzara KeyError.'''
		return self.vertices[id]

	def __setitem__(self, id, valor):
		'''Agrega un nuevo vertice con el par <id, valor> indicado. ID debe ser de identificador unico del vertice.
		En caso que el identificador ya se encuentre asociado a un vertice, se actualizara el valor.
		'''
		self.vertices[id] = {}

	def __delitem__(self, id):
		'''Elimina el vertice del grafo. Si no existe el identificador en el grafo, lanzara KeyError.
		Borra tambien todas las aristas que salian y entraban al vertice en cuestion.
		'''
		if id not in self.vertices:
			raise KeyError(V_NOT_FOUND.format(id))
		if not self.dirigido:
			adyacentes = self.vertices[id]
			for vertice in adyacentes:
				self.vertices[vertice].pop(id)
		else:
			for vertice in self.vertices:
				if id in self.vertices[vertice]:
					self.vertices[vertice].pop(id)
		self.vertices.pop(id)

	def __contains__(self, id):
		''' Determina si el grafo contiene un vertice con el identificador indicado.'''
		return id in self.vertices

	def agregar_arista(self, desde, hasta, peso = 1):
		'''Agrega una arista que conecta los vertices indicados. Parametros:
			- desde y hasta: identificadores de vertices dentro del grafo. Si alguno de estos no existe dentro del grafo, lanzara KeyError.
			- Peso: valor de peso que toma la conexion. Si no se indica, valdra 1.
			Si el grafo es no-dirigido, tambien agregara la arista reciproca.
		'''
		if desde not in self.vertices:
			raise KeyError(V_NOT_FOUND.format(desde))
		if hasta not in self.vertices:
			raise KeyError(V_NOT_FOUND.format(hasta))
		self.vertices[desde][hasta] = peso
		if not self.dirigido:
			self.vertices[hasta][desde] = peso

	def borrar_arista(self, desde, hasta):
		'''Borra una arista que conecta los vertices indicados. Parametros:
			- desde y hasta: identificadores de vertices dentro del grafo. Si alguno de estos no existe dentro del grafo, lanzara KeyError.
		   En caso de no existir la arista, se lanzara ValueError.
		'''
		if desde not in self.vertices or hasta not in self.vertices:
			raise KeyError(VS_NOT_FOUND)
		if hasta not in self.vertices[desde]:
			raise ValueError(A_NOT_FOUND)
		self.vertices[desde].pop(hasta)
		if not self.dirigido:
			self.vertices[hasta].pop(desde)

	def obtener_peso_arista(self, desde, hasta):
		'''Obtiene el peso de la arista que va desde el vertice 'desde', hasta el vertice 'hasta'. Parametros:
			- desde y hasta: identificadores de vertices dentro del grafo. Si alguno de estos no existe dentro del grafo, lanzara KeyError.
			En caso de no existir la union consultada, se devuelve None.
		'''
		if desde not in self.vertices:
			raise KeyError(V_NOT_FOUND.format(desde))
		if hasta not in self.vertices:
			raise KeyError(V_NOT_FOUND.format(hasta))
		if hasta not in self.vertices[desde]:
			return None
		else:
			return self.vertices[desde][hasta]

	def adyacentes(self, id):
		'''Devuelve una lista con los vertices (identificadores) adyacentes al indicado. Si no existe el vertice, se lanzara KeyError'''
		if id not in self.vertices:
			raise KeyError(V_NOT_FOUND.format(id))
		lista_adyacentes = []
		for adyacente in self.vertices[id]:
			lista_adyacentes.append(adyacente)
		return lista_adyacentes

	def recorrer(self, recorrido, visitar=visitar_nulo, extra=None, inicio=None):
		'''Realiza un recorrido BFS o DFS dentro del grafo (segun sea indicado), aplicando la funcion pasada por parametro en cada vertice visitado.
		Parametros:
			- visitar: una funcion cuya firma sea del tipo: 
					visitar(v, padre, orden, extra) -> Boolean
					Donde 'v' es el identificador del vertice actual, 
					'padre' el diccionario de padres actualizado hasta el momento,
					'orden' el diccionario de ordenes del recorrido actualizado hasta el momento, y 
					'extra' un parametro extra que puede utilizar la funcion (cualquier elemento adicional que pueda servirle a la funcion a aplicar). 
					La funcion aplicar devuelve True si se quiere continuar iterando, False en caso contrario.
			- extra: el parametro extra que se le pasara a la funcion 'visitar'
			- inicio: identificador del vertice que se usa como inicio. Si se indica un vertice, el recorrido se comenzara en dicho vertice, 
			y solo se seguira hasta donde se pueda (no se seguira con los vertices que falten visitar)
			- recorrido: sera "bfs" o "dfs"
		Salida:
			Tupla (padre, orden), donde :
				- 'padre' es un diccionario que indica para un identificador, cual es el identificador del vertice padre en el recorrido (None si es el inicio)
				- 'orden' es un diccionario que indica para un identificador, cual es su orden en el recorrido
		'''
		if recorrido != "dfs" and recorrido != "bfs":
			raise ValueError("El parametro \"recorrido\" debe ser \"bfs\" o \"dfs\"")
		visitados = {}
		padre = {}
		orden = {}
		if inicio != None:
			padre[inicio] = None
			orden[inicio] = 0
			if recorrido == "bfs":
				self.bfs(visitar, extra, inicio, visitados, padre, orden)
			elif recorrido == "dfs":
				self.dfs(visitar, extra, inicio, visitados, padre, orden)
		for v in self.vertices:
			if v not in visitados:
				padre[v] = None
				orden[v] = 0
				if recorrido == "bfs":
					self.bfs(visitar, extra, v, visitados, padre, orden)
				elif recorrido == "dfs":
					self.dfs(visitar, extra, v, visitados, padre, orden)
		return padre, orden

	def bfs(self, visitar, extra, origen, visitados, padre, orden):
		q = Queue()
		q.put(origen)
		visitados[origen] = True
		while not q.empty():
			v = q.get()
			for u in self.adyacentes(v):
				if u not in visitados:
					visitados[u] = True
					padre[u] = v
					orden[u] = orden[v] + 1
					q.put(u)
					if visitar(u, padre, orden, extra) == False:
						return

	def dfs(self, visitar, extra, origen, visitados, padre, orden):
		visitados[origen] = True
		for w in self.adyacentes(origen):
			if w not in visitados:
				padre[w] = origen
				orden[w] = orden[origen] + 1
				if visitar(w, padre, orden, extra) == False:
					return
				self.dfs(visitar, extra, w, visitados, padre, orden)

	def componentes_conexas(self):
		'''Devuelve una lista de listas con componentes conexas. Cada componente conexa es representada con una lista, con los identificadores de sus vertices.
		Solamente tiene sentido de aplicar en grafos no dirigidos, por lo que
		en caso de aplicarse a un grafo dirigido se lanzara TypeError'''
		raise NotImplementedError()

	def camino_minimo(self, origen, destino=None, heuristica=heuristica_nula):
		'''Devuelve el recorrido minimo desde el origen hasta el destino, aplicando el algoritmo de Dijkstra, o bien
		A* en caso que la heuristica no sea nula. Parametros:
			- origen y destino: identificadores de vertices dentro del grafo. Si alguno de estos no existe dentro del grafo, lanzara KeyError.
			- heuristica: funcion que recibe dos parametros (un vertice y el destino) y nos devuelve la 'distancia' a tener en cuenta para ajustar los resultados y converger mas rapido.
			Por defecto, la funcion nula (devuelve 0 siempre)
		Devuelve:
			- Listado de vertices (identificadores) ordenado con el recorrido, incluyendo a los vertices de origen y destino. 
			En caso que no exista camino entre el origen y el destino, se devuelve None. 
		'''
		if origen not in self.vertices:
			raise KeyError(V_NOT_FOUND.format(origen))
		if destino is not None and destino not in self.vertices:
			raise KeyError(V_NOT_FOUND.format(destino))
		items = {}
		for i in self:
			if i != origen:
				items[i] = Item(i, INFINITO)
			else:
				items[i] = Item(i, 0, True)
		q = Heap()
		q.push(items[origen])
		cortar = False
		while not q.empty():
			v = q.pop()
			for w in self.adyacentes(v.dato):
				if not items[w].visitado:
					if (items[v.dato].distancia + self.obtener_peso_arista(v.dato, w)) < items[w].distancia:
						items[w].distancia = items[v.dato].distancia + self.obtener_peso_arista(v.dato, w)
						items[w].padre = v.dato
						items[w].visitado = True
						q.push(items[w])
						if (items[w].dato == destino):
							cortar = True
							break
			if cortar:
				break
		return items

	def mst(self):
		'''Calcula el Arbol de Tendido Minimo (MST) para un grafo no dirigido. En caso de ser dirigido, lanza una excepcion.
		Devuelve: un nuevo grafo, con los mismos vertices que el original, pero en forma de MST.'''
		raise NotImplementedError()

	def random_walk(self, largo, origen=None, pesado=True):
		''' Devuelve una lista con un recorrido aleatorio de grafo.
			Parametros:
				- largo: El largo del recorrido a realizar
				- origen: Vertice (id) por el que se debe comenzar el recorrido. Si origen = None, se comenzara por un vertice al azar.
				- pesado: indica si se tienen en cuenta los pesos de las aristas para determinar las probabilidades de movernos de un vertice a uno de sus vecinos (False = todo equiprobable). 
			Devuelve:
				Una lista con los vertices (ids) recorridos, en el orden del recorrido. 
		'''
		walk = []
		i = 0
		if origen is None:
			origen = random.choice(list(self.vertices.keys()))
		actual = origen
		while i < largo:
			if pesado:
				lista = []
				actual = vertice_aleatorio(self[actual])
			else:
				actual = random.choice(self.adyacentes(actual))
			walk.append(actual)
			i += 1
		return walk

	def recomendar(self, personaje, walk_len, walk_q):
		if personaje not in self.vertices:
			raise KeyError("El personaje {} no se encuentra en el grafo".format(personaje))
		personajes = list()
		for i in range(walk_q):
			lista = self.random_walk(walk_len, personaje)
			for j in lista:
				if personaje not in self.adyacentes(j) and j != personaje:
					personajes.append(j)
		return Counter(personajes)


def vertice_aleatorio(pesos):
    '''Pesos es un diccionario de pesos, clave vertice vecino, valor el peso.
    '''
    total = sum(pesos.values())
    rand = random.uniform(0, total)
    acum = 0
    for vertice, peso_arista in pesos.items():
        if acum + peso_arista >= rand:
            return vertice
        acum += peso_arista


class Item(object):

	def __init__(self, dato, distancia, visitado=False):
		self.dato = dato
		self.distancia = distancia
		self.visitado = visitado
		self.padre = None

	def __str__(self):
		return str((self.dato, self.distancia, self.visitado))

	def __repr__(self):
		return str((self.dato, self.distancia, self.visitado, self.padre))

	def __lt__(self, otro):
		return self.distancia < otro.distancia

	def __gt__(self, otro):
		return self.distancia > otro.distancia


class Heap(object):
	''' Clase wrapper que modela un Heap usando la biblioteca heapq brindada por defecto en python.
	'''

	def __init__(self, lista=[]):
		self.lista = lista
		if len(self.lista) > 1:
			heapify(self.lista)

	def push(self, item):
		heappush(self.lista, item)

	def pop(self):
		return heappop(self.lista)

	def min(self):
		return self.lista[0]

	def empty(self):
		return len(self.lista) == 0

	def __len__(self):
		return len(self.lista)

	def heapify(self):
		heapify(self.lista)
