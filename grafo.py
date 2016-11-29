from queue import *

visitar_nulo = lambda a,b,c,d: True
heuristica_nula = lambda actual,destino: 0

VS_NOT_FOUND = "Algun/ambos vertice/s pasados no se encuentra/n en el grafo"
V_NOT_FOUND = "El vertice {} no se encuentra en el grafo."
A_NOT_FOUND = "La arista a borrar no se encuentra en el grafo."

class Grafo(object):
	'''Clase que representa un grafo. El grafo puede ser dirigido, o no, y puede no indicarsele peso a las aristas
	(se comportara como peso = 1). Implementado como "diccionario de diccionarios"'''
	
	def __init__(self, es_dirigido = False):
		'''Crea el grafo. El parametro 'es_dirigido' indica si sera dirigido, o no.'''
		if not isinstance(es_dirigido, bool):
			raise TypeError("{} debe ser un valor booleano".format(es_dirigido))
		self.dirigido = es_dirigido
		self.grafo = {}
	
	def __len__(self):
		'''Devuelve la cantidad de vertices del grafo'''
		cant_vertices = 0
		for vertice in self.grafo:
			cant_vertices += 1
		return cant_vertices
	
	def __iter__(self):
		'''Devuelve un iterador de vertices, sin ningun tipo de relacion entre los consecutivos'''
		return iter(self.grafo)
		
	def keys(self):
		'''Devuelve una lista de identificadores de vertices. Iterar sobre ellos es equivalente a iterar sobre el grafo.'''
		lista_idvertices = []
		for vertice in self.grafo:
			lista_idvertices.append(vertice)
		return lista_idvertices
		
	def __getitem__(self, id):
		'''Devuelve el valor del vertice asociado, del identificador indicado. Si no existe el identificador en el grafo, lanzara KeyError.'''
		return self.grafo[id]
		
	def __setitem__(self, id, valor):
		'''Agrega un nuevo vertice con el par <id, valor> indicado. ID debe ser de identificador unico del vertice.
		En caso que el identificador ya se encuentre asociado a un vertice, se actualizara el valor.
		'''
		self.grafo[id] = {}
	
	def __delitem__(self, id):
		'''Elimina el vertice del grafo. Si no existe el identificador en el grafo, lanzara KeyError.
		Borra tambien todas las aristas que salian y entraban al vertice en cuestion.
		'''
		if id not in self.grafo:
			raise KeyError(V_NOT_FOUND.format(id))
		if not self.dirigido:
			adyacentes = self.grafo[id]
			for vertice in adyacentes:
				self.grafo[vertice].pop(id)
		else:
			for vertice in self.grafo:
				if id in self.grafo[vertice]:
					self.grafo[vertice].pop(id)
		self.grafo.pop(id)
	
	def __contains__(self, id):
		''' Determina si el grafo contiene un vertice con el identificador indicado.'''
		return id in self.grafo
		
	def agregar_arista(self, desde, hasta, peso = 1):
		'''Agrega una arista que conecta los vertices indicados. Parametros:
			- desde y hasta: identificadores de vertices dentro del grafo. Si alguno de estos no existe dentro del grafo, lanzara KeyError.
			- Peso: valor de peso que toma la conexion. Si no se indica, valdra 1.
			Si el grafo es no-dirigido, tambien agregara la arista reciproca.
		'''
		if desde not in self.grafo:
			raise KeyError(V_NOT_FOUND.format(desde))
		if hasta not in self.grafo:
			raise KeyError(V_NOT_FOUND.format(hasta))
		self.grafo[desde][hasta] = peso
		if not self.dirigido:
			self.grafo[hasta][desde] = peso

	def borrar_arista(self, desde, hasta):
		'''Borra una arista que conecta los vertices indicados. Parametros:
			- desde y hasta: identificadores de vertices dentro del grafo. Si alguno de estos no existe dentro del grafo, lanzara KeyError.
		   En caso de no existir la arista, se lanzara ValueError.
		'''
		if desde not in self.grafo or hasta not in self.grafo:
			raise KeyError(VS_NOT_FOUND)
		if hasta not in self.grafo[desde]:
			raise ValueError(A_NOT_FOUND)
		self.grafo[desde].pop(hasta)
		if not self.dirigido:
			self.grafo[hasta].pop(desde)

	def obtener_peso_arista(self, desde, hasta):
		'''Obtiene el peso de la arista que va desde el vertice 'desde', hasta el vertice 'hasta'. Parametros:
			- desde y hasta: identificadores de vertices dentro del grafo. Si alguno de estos no existe dentro del grafo, lanzara KeyError.
			En caso de no existir la union consultada, se devuelve None.
		'''
		if desde not in self.grafo:
			raise KeyError(V_NOT_FOUND.format(desde))
		if hasta not in self.grafo:
			raise KeyError(V_NOT_FOUND.format(hasta))
		if hasta not in self.grafo[desde]:
			return None
		else:
			return self.grafo[desde][hasta]
		
	def adyacentes(self, id):
		'''Devuelve una lista con los vertices (identificadores) adyacentes al indicado. Si no existe el vertice, se lanzara KeyError'''
		if id not in self.grafo:
			raise KeyError(V_NOT_FOUND.format(id))
		lista_adyacentes = []
		for adyacente in self.grafo[id]:
			lista_adyacentes.append(adyacente)
		return lista_adyacentes
	
	def bfs(self, visitar = visitar_nulo, extra = None, inicio=None):
		'''Realiza un recorrido BFS dentro del grafo, aplicando la funcion pasada por parametro en cada vertice visitado.
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
		Salida:
			Tupla (padre, orden), donde :
				- 'padre' es un diccionario que indica para un identificador, cual es el identificador del vertice padre en el recorrido BFS (None si es el inicio)
				- 'orden' es un diccionario que indica para un identificador, cual es su orden en el recorrido BFS
		'''
		for v in self.grafo:
			i.visitado = False
		for v in self.grafo:
			if not v.visitado:
				self._bfs(v, visitar, extra, inicio)
		raise NotImplementedError()

	def _bfs(self, vertice, visitar, extra, inicio):
		para_analizar = Queue()
		para_analizar.put(vertice)
		while not para_analizar.empty():
			v = para_analizar.get()
			for u in v
	
	def dfs(self, visitar = visitar_nulo, extra = None, inicio=None):
		'''Realiza un recorrido DFS dentro del grafo, aplicando la funcion pasada por parametro en cada vertice visitado.
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
		Salida:
			Tupla (padre, orden), donde :
				- 'padre' es un diccionario que indica para un identificador, cual es el identificador del vertice padre en el recorrido DFS (None si es el inicio)
				- 'orden' es un diccionario que indica para un identificador, cual es su orden en el recorrido DFS
		'''
		raise NotImplementedError()
	
	def componentes_conexas(self):
		'''Devuelve una lista de listas con componentes conexas. Cada componente conexa es representada con una lista, con los identificadores de sus vertices.
		Solamente tiene sentido de aplicar en grafos no dirigidos, por lo que
		en caso de aplicarse a un grafo dirigido se lanzara TypeError'''
		raise NotImplementedError()
		
	def camino_minimo(self, origen, destino, heuristica=heuristica_nula):
		'''Devuelve el recorrido minimo desde el origen hasta el destino, aplicando el algoritmo de Dijkstra, o bien
		A* en caso que la heuristica no sea nula. Parametros:
			- origen y destino: identificadores de vertices dentro del grafo. Si alguno de estos no existe dentro del grafo, lanzara KeyError.
			- heuristica: funcion que recibe dos parametros (un vertice y el destino) y nos devuelve la 'distancia' a tener en cuenta para ajustar los resultados y converger mas rapido.
			Por defecto, la funcion nula (devuelve 0 siempre)
		Devuelve:
			- Listado de vertices (identificadores) ordenado con el recorrido, incluyendo a los vertices de origen y destino. 
			En caso que no exista camino entre el origen y el destino, se devuelve None. 
		'''
		raise NotImplementedError()
	
	def mst(self):
		'''Calcula el Arbol de Tendido Minimo (MST) para un grafo no dirigido. En caso de ser dirigido, lanza una excepcion.
		Devuelve: un nuevo grafo, con los mismos vertices que el original, pero en forma de MST.'''
		raise NotImplementedError()
	
	def random_walk(self, largo, origen = None, pesado = False):
		''' Devuelve una lista con un recorrido aleatorio de grafo.
			Parametros:
				- largo: El largo del recorrido a realizar
				- origen: Vertice (id) por el que se debe comenzar el recorrido. Si origen = None, se comenzara por un vertice al azar.
				- pesado: indica si se tienen en cuenta los pesos de las aristas para determinar las probabilidades de movernos de un vertice a uno de sus vecinos (False = todo equiprobable). 
			Devuelve:
				Una lista con los vertices (ids) recorridos, en el orden del recorrido. 
		'''
		raise NotImplementedError()

g = Grafo(True)
g["Hola"] = {}
g["Chau"] = {}
g.agregar_arista("Hola", "Chau")
