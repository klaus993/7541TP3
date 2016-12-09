def label_propagation(grafo, label, corte):
	'''Recibe un grafo, un diccionario llamado label y un valor corte. Esta
	función realiza el algoritmo label propagation sobre label hasta que este se
	termina (en caso de que corte sea cero) o hasta que se llegue al número de 
	iteración indicado por corte. '''
	frecuencia = {}
	i = 0
	max_freq = 0
	vertice_max_freq = None
	for clave, valor in label.items():
		for adyacente in grafo.adyacentes(clave):
			if not adyacente in frecuencia:
				frecuencia[adyacente] = 0
			frecuencia[adyacente] += 1
		for clave2, valor2 in frecuencia.items():
			if valor2 > max_freq:
				max_freq = valor2
				vertice_max_freq = clave2
		if vertice_max_freq:
			label[clave] = label[vertice_max_freq]
			vertice_max_freq = None
			frecuencia = {}
			max_freq = 0
		if corte:
			if i == corte:
				break
		i += 1

def comunidades(grafo, corte = 0):
	'''Recibe un grafo y un valor corte que determina si el algoritmo se hace 
	hasta un determinado corte o no y cuántas veces itera. Muestra por pantalla 
	las comunidades que se encuentran en el grafo. '''
	label = {}
	i = 0
	for vertice in grafo.keys():
		label[vertice] = i
		i += 1
	label_propagation(grafo, label, corte)
	dic_comunidades = {}
	for clave, valor in label.items():
		if valor not in dic_comunidades:
			dic_comunidades[valor] = []
		dic_comunidades[valor].append(clave)
	numero_comunidad = 1
	for clave, valor in dic_comunidades.items():
		print("clave:"+ str(clave))
		print("valor: ")
		for integrante in valor:
			print(integrante + " ")
		print("]")

	for clave, valor in dic_comunidades.items():
		print("Comunidad " + str(numero_comunidad) + ": [ ")
		for integrante in valor:
			print(integrante + " ")
		print("]")
		numero_comunidad += 1 
