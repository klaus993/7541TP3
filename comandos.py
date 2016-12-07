from parse import *

lista_comandos = ["", "salir", "similares", "recomendar", "camino", "centralidad", "distancias", "estadisticas", "comunidades"]


def validar_comando(comando):
	com = comando.split(" ")
	if com[0] != "estadisticas" and com[0] != "comunidades" and com[0] != "salir" and com[0] != "" and len(com) == 1:
		return False
	return com[0] in lista_comandos


def camino(grafo, p1, p2):
	''' Imprime el camino mínimo entre dos personajes p1 y p2.
	Si alguno de los personajes no está en el grafo, lanza KeyError.
	'''
	try:
		caminos = grafo.camino_minimo(p1, p2)
	except KeyError as e:
		print(e)
		return
	camino = [p2]
	camino = _camino(caminos, p1, p2, camino)[::-1]
	for i in range(len(camino) - 1):
		print(camino[i] + ' -> ', end='')
	print(camino[len(camino) - 1])


def _camino(caminos, p1, p2, camino):
	if caminos[p2].padre == p1:
		camino.append(caminos[p2].padre)
		return camino
	camino.append(caminos[p2].padre)
	return _camino(caminos, p1, caminos[p2].padre, camino)


def similares(grafo, personaje, cantidad):
	''' Llama a la función random_walks para devolver "cantidad" personajes similares 
	al personaje pasado por parámetro.
	Realiza 500 caminos de 50 pasos.
	'''
	random_walks(grafo, personaje, cantidad, 500, 50, adyacentes=True)


def recomendar(grafo, personaje, cantidad):
	''' Llama a la función random_walks para devolver "cantidad" personajes recomendados
	respecto del personaje pasado por parámetro, se excluyen los personajes adyacentes.
	Realiza 500 random walks de 30 pasos.
	'''
	random_walks(grafo, personaje, cantidad, 500, 30, adyacentes=False)


def centralidad(grafo, cantidad):
	''' Llama a la función random_walks para devolver "cantidad" de elementos
	centrales en el grafo. Inicia en un nodo aleatorio.
	Realiza 500 random walks de 250 pasos.
	'''
	random_walks(grafo, None, cantidad, 500, 250, adyacentes=True)


def generar_distancias(v, padre, orden, distancias):
	if padre != distancias[0]:
		distancias[1][distancias[0][1]] = 0
		distancias[0][1] += 1
		distancias[0] = padre
	distancias[1][distancias[0][1]] += 1

def distancias(grafo, personaje):
	''' Recibe un grafo y el identificador de un vértice. Imprime por pantalla
	la cantidad de personajes que se encuentran a cada una de las distancias
	posibles. '''
	dic_distancias = {}
	distancias = [[None, 1], dic_distancias] 
	grafo.recorrer("bfs", generar_distancias, distancias, personaje)
	for clave,valor in distancias[1].items():
		print("Distancia "+ str(clave)+": "+str(valor))


def estadisticas():
	pass


def comunidades():
	pass


def random_walks(grafo, personaje, cantidad, cant_caminos, profundidad, adyacentes):
	''' Recibe el grafo, un personaje, la cantidad de personajes a devolver, la cantidad de caminos,
	la profundidad del random walk, y un booleano. Si es True se consideran los adyacentes, si es False no.
	Esto último es así para que la función sea reutilizable. 
	Imprime los "cantidad" personajes por pantalla. Si no hay personajes, imprime un mensaje de error.
	'''
	try:
		counter = grafo.random_walks(personaje, cant_caminos, profundidad, adyacentes)
	except KeyError as e:
		print(e)
		return
	recomendados = sorted(counter, key=counter.get, reverse=True)[:cantidad]  #Arma una lista con los "cantidad" personajes que más aparecen
	for i in range(len(recomendados) - 1):
		print(recomendados[i], end=', ')
	if len(recomendados) > 0:
		print(recomendados[len(recomendados) - 1])
	else:
		print("El personaje no tiene suficientes conexiones")
