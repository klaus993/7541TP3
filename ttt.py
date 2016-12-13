class Item(object):
	'''Clase Item, utilizada en el algoritmo de camino mínimo para almacenar
	datos de un nodo.
	'''

	def __init__(self, dato, distancia, visitado=False):
		self.dato = dato
		self.distancia = distancia
		self.visitado = visitado
		self.padre = None

	def __str__(self):
		return str((self.dato, self.distancia, self.visitado, self.padre))

	def __repr__(self):
		return str((self.dato, self.distancia, self.visitado, self.padre))

	def __lt__(self, otro):
		return self.distancia < otro.distancia

	def __gt__(self, otro):
		return self.distancia > otro.distancia
