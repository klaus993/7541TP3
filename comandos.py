from parse import *
import math

# 1 es camino
# 2 es recomendar
# 3 es similares
# 4 es centralidad
# 5 es distancias
# 6 es estadisticas
# 7 es comunidades
# 8 es salir

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
	if com == "estadisticas":
		return com,
	if com == "comunidades":
		return com,
	if com == "":
		return com,
	if com == "salir":
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
	print (v,)
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


def calcular_aristas(grafo):
	'''Recibe un grafo. Devuelve la cantidad de aristas que tiene. '''
	cant_aristas = 0
	for vertice in grafo.keys():
		for adyacente in grafo.adyacentes(vertice):
			cant_aristas += 1
	cant_aristas //= 2
	return cant_aristas


def calcular_promedio_gr_vertices(grafo, cant_vertices):
	'''Recibe un grafo y sus cantidad de vértices. Devuelve el promedio de grados
	de los vertices. '''
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


def comunidades(grafo, corte=0):
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
	while True:
		label_propagation(grafo, label_aux, corte)
		if(label_aux == label_original):
			break
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
