import math
from collections import Counter

# [0] es cadena vacía
# [1] es camino
# [2] es recomendar
# [3] es similares
# [4] es centralidad_rw
# [5] es centralidad_exacta
# [6] es distancias
# [7] es estadisticas
# [8] es comunidades
# [9] es salir

LISTA_COMANDOS = ["", "camino", "recomendar", "similares", "centralidad_rw", "centralidad_exacta", "distancias", "estadisticas", "comunidades", "salir"]


def validar_comando(comando):
	com = comando.split(" ")
	if com[0] != "estadisticas" and com[0] != "comunidades" and com[0] != "salir" and com[0] != "" and len(com) == 1:
		return False
	return com[0] in LISTA_COMANDOS


def validar_comandos(comando):
	com = comando.split(" ")[0]
	param = comando[len(LISTA_COMANDOS[1]) + 1:].split(", ")
	if com == LISTA_COMANDOS[1] and len(param) == 2:
		return com, param[0], param[1]
	param = comando[len(LISTA_COMANDOS[2]) + 1:].split(", ")
	if com == LISTA_COMANDOS[2] and len(param) == 2 and param[1].isdigit():
		return com, param[0], int(param[1])
	param = comando[len(LISTA_COMANDOS[3]) + 1:].split(", ")
	if com == LISTA_COMANDOS[3] and len(param) == 2 and param[1].isdigit():
		return com, param[0], int(param[1])
	param = comando[len(LISTA_COMANDOS[4]) + 1:].split(", ")
	if com == LISTA_COMANDOS[4] and len(param) == 1 and param[0].isdigit():
		return com, int(param[0])
	param = comando[len(LISTA_COMANDOS[5]) + 1:].split(", ")
	if com == LISTA_COMANDOS[5] and len(param) == 1 and param[0].isdigit():
		return com, int(param[0])
	param = comando[len(LISTA_COMANDOS[6]) + 1:].split(", ")
	if com == LISTA_COMANDOS[6] and len(param) == 1:
		return com, param[0]
	if comando == LISTA_COMANDOS[7]:
		return com,
	if comando == LISTA_COMANDOS[8]:
		return com,
	if com == LISTA_COMANDOS[0]:
		return com,
	if comando == LISTA_COMANDOS[9]:
		return com,
	return None,


def camino(grafo, p1, p2):
	''' Imprime el camino mínimo entre dos personajes p1 y p2.
	Si alguno de los personajes no está en el grafo, atrapa KeyError e imprime un mensaje de error.
	'''
	try:
		caminos = grafo.camino_minimo(p1, p2)
	except KeyError as e:
		print(e)
		return
	camino = [p2]
	camino = lista_camino(caminos, p1, p2, camino)[::-1]
	if camino[0] != p1:
		print("No hay camino desde {} hasta {}.".format(p1, p2))
		return
	for i in range(len(camino) - 1):
		print(camino[i] + ' -> ', end='')
	print(camino[len(camino) - 1])


def lista_camino(caminos, p1, p2, camino):
	''' Recibe un diccionario de items (armado por el método camino_minimo) con los siguientes atributos:
		-dato (id)
		-distancia
		-visitado (bool)
		-padre (id)
	Y visita recursivamente al padre de p2 hasta llegar a p1,
	guardando en una lista ("camino") (al revés) el camino mínimo desde p1 hasta p2.
	Devuelve esa lista. Si no hay camino, la lista 
	'''
	if caminos[p2].padre is None:
		return camino
	camino.append(caminos[p2].padre)
	return lista_camino(caminos, p1, caminos[p2].padre, camino)


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


def centralidad_random_walks(grafo, cantidad):
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


def max_freq(l):
	''' Devuelve el label de máxima frecuencia, o en su defecto
	(si son todos iguales) devuelve el mínimo.
	'''
	valor = l[0]
	if all(val == valor for val in l):
		return valor
	return max(set(l), key=l.count)  # Devuelve el de mayor frecuencia o el mínimo.


def crear_label_d(grafo):
	''' Crea un diccionario de nombres de personajes como claves
	y sus labels como valores, recorriendo el diccionario en un orden aleatorio
	asignando labels de 0 a len(grafo)-1.
	Devuelve el diccionario.
	'''
	label_d = {}
	i = 0
	for v in grafo:
		label_d[v] = i
		i += 1
	return label_d


def propagate_labels(grafo, label_d):
	''' Hace una iteración del algoritmo label propagation sobre un diccionario
	de labels pasado por parámetro. El diccionario de labels sólo puede tener labels positivos.
	'''
	for v in grafo:
		lista_adyacentes = [label_d[w] for w in grafo.adyacentes(v)]
		if len(lista_adyacentes) != 0:
			label_d[v] = max_freq(lista_adyacentes)


def label_propagation(grafo, cant):
	''' Realiza el algoritmo label propagation "cant" veces sobre el grado pasado por parámetro,
	y devuelve el diccionario de labels resultante.
	'''
	label_d = crear_label_d(grafo)
	for i in range(cant):
		propagate_labels(grafo, label_d)
	return label_d


def listas_de_comunidades(grafo, label_d):
	''' Crea una lista de listas de comunidades del grafo, dado un diccionario de labels.
	Agrupa las comunidades por label. Crea len(grafo) listas, aunque algunos labels no tengan
	comunidad.
	'''
	d = []
	for i in range(len(grafo)):
		d.append([v for v in label_d if label_d[v] == i])
	return d


def comunidades(grafo):
	''' Calcula e imprime las comunidades del grafo, realizando el algoritmo
	label propagation 30 veces sobre un grafo.i
	Filtra las comunidades con menos de 4 personajes y más de 1000.
	'''
	label_d = label_propagation(grafo, 30)
	comunidad_l = listas_de_comunidades(grafo, label_d)
	j = 1
	for i in range(len(grafo)):
		if len(comunidad_l[i]) > 4 and len(comunidad_l[i]) < 1000:
			print("--- COMUNIDAD {} ---".format(j))
			j += 1
			for p in comunidad_l[i]:
				print(p)


def ordenar_vertices(caminos):
	''' Recibe un diccionario de Items (caminos) y devuelve una lista de los items
	ordenados de mayor a menor (por distancia) sin incluir los de distancia infinito.
	'''
	aux = caminos.copy()
	for i in caminos:
		if aux[i].distancia == float('inf'):
			aux.pop(i)
	return sorted(aux, key=aux.get, reverse=True)


def generar_caminos_minimos(grafo):
	cont = {}
	for v in grafo:
		cont[v] = 0
	j = 1
	for v in grafo:
		if j == 20: break
		print("V =", str(v) + " ,,, " + str(j)); j+=1
		caminos = grafo.camino_minimo(v)
		cont_aux = {}
		for w in grafo:
			cont_aux[w] = 0
		vertices_ordenados = ordenar_vertices(caminos)
		for w in vertices_ordenados:
			#print("--- W =",w)
			if caminos[w].distancia != float('inf') and caminos[w].padre is not None:
				cont_aux[caminos[w].padre] += 1 + cont_aux[w]
		for w in grafo:
			if w != v:
				cont[w] += cont_aux[w]
	return cont


def centralidad_exacta(grafo, cantidad):
	cont = generar_caminos_minimos(grafo)
	centrales = sorted(cont, key=cont.get, reverse=True)[:cantidad]
	for i in range(len(centrales) - 1):
		print(centrales[i], end=', ')
	print(centrales[len(centrales) - 1])
