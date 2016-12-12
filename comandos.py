import math

# [1] es camino
# [2] es recomendar
# [3] es similares
# [4] es centralidad
# [5] es distancias
# [6] es estadisticas
# [7] es comunidades
# [8] es salir

lista_comandos = ["", "camino", "recomendar", "similares", "centralidad", "distancias", "estadisticas", "comunidades", "salir"]


def validar_comando(comando):
	com = comando.split(" ")
	if com[0] != "estadisticas" and com[0] != "comunidades" and com[0] != "salir" and com[0] != "" and len(com) == 1:
		return False
	return com[0] in lista_comandos


def validar_comandos(comando):
	com = comando.split(" ")[0]
	param = comando[len("camino") + 1:].split(", ")
	if com == "camino" and len(param) == 2:
		return com, param[0], param[1]
	param = comando[len("recomendar") + 1:].split(", ")
	if com == "recomendar" and len(param) == 2 and param[1].isdigit():
		return com, param[0], int(param[1])
	param = comando[len("similares") + 1:].split(", ")
	if com == "similares" and len(param) == 2 and param[1].isdigit():
		return com, param[0], int(param[1])
	param = comando[len("centralidad") + 1:].split(", ")
	if com == "centralidad" and len(param) == 1:
		return com, int(param[0])
	param = comando[len("distancias") + 1:].split(", ")
	if com == "distancias" and len(param) == 1:
		return com, param[0]
	if comando == "estadisticas":
		return com,
	if comando == "comunidades":
		return com,
	if com == "":
		return com,
	if comando == "salir":
		return com,
	return None,


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


def generar_distancias(v, padre, orden, dic_distancias):
	'''Función que recibe un vértice, un diccionario desde el cual se puede 
	acceder al padre del vértice, otro desde el cual se puede acceder a su orden
	y uno más donde se almacenan las distancias y la cantidad de vértices que 
	cumplen esa distancia a un origen como valores. La función agrega justamente
	a este último diccionario la distancia del vértice y le aumenta en uno
	su valor. '''
	if orden[v] not in dic_distancias:
		dic_distancias[orden[v]] = 0
	dic_distancias[orden[v]] += 1


def distancias(grafo, personaje):
	''' Recibe un grafo y el identificador de un vértice. Imprime por pantalla
	la cantidad de personajes que se encuentran a cada una de las distancias
	posibles. '''
	dic_distancias = {}
	grafo.recorrer("bfs", generar_distancias, dic_distancias, personaje)
	for clave, valor in dic_distancias.items():
		print("Distancia " + str(clave) + ": " + str(valor))


def calcular_vertices(grafo):
	'''Recibe un grafo y calcula su cantidad de vértices. '''
	return len(grafo.keys())


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
	return cant_aristas / cant_max_aristas


def estadisticas(grafo):
	'''Recibe un grafo e imprime por pantalla la cantidad de vértices y de 
	aristas que posee, el promedio del grado de los vértices, el desvío estándar
	del grado de los vértices y por último su densidad. '''
	cant_vertices = calcular_vertices(grafo)
	cant_aristas, promedio_grados_vertices = calcular_aristas_y_promedio_gr_vert(grafo, cant_vertices)
	desvio_estandar = calcular_desvio_estandar(grafo, promedio_grados_vertices, cant_vertices)
	densidad = calcular_densidad(grafo, cant_vertices, cant_aristas)
	print("Cantidad de vértices: {}\nCantidad de aristas: {}\nPromedio del grado de cada vértice: {:.2f}\nDesvío estándar del grado de cada vértice: {:.2f}\nDensidad del grafo: {:.10f}".format(cant_vertices, cant_aristas, promedio_grados_vertices, desvio_estandar, densidad))


def max_freq(l):
	valor = min(l)
	if all(val == valor for val in l):
		return valor
	return max(set(l), key=l.count)


def crear_label_d(grafo):
	label_d = {}
	i = 0
	for v in grafo:
		label_d[v] = i
		i += 1
	return label_d


def propagate_labels(grafo, label_d):
	for v in grafo:
		lista_adyacentes = [label_d[w] for w in grafo.adyacentes(v)]
		if len(lista_adyacentes) != 0:
			label_d[v] = max_freq(lista_adyacentes)


def label_propagation(grafo, cant):
	label_d = crear_label_d(grafo)
	for i in range(cant):
		propagate_labels(grafo, label_d)
	return label_d


def comunidades(grafo):
	label_d = label_propagation(grafo, 30)
	d = []
	for i in range(len(grafo)):
		d.append([v for v in label_d if label_d[v] == i])
	j = 1
	for i in range(len(grafo)):
		if len(d[i]) > 4 and len(d[i]) < 1000:
			print("--- COMUNIDAD {} ---".format(j))
			j += 1
			for p in d[i]:
				print(p)
