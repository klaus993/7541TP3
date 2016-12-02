lista_comandos = ["", "salir", "similares", "recomendar", "camino", "centralidad", "distancias", "estadisticas", "comunidades"]


def camino(grafo, p1, p2):
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


def validar_comando(comando):
	com = comando.split(" ")
	if com[0] != "estadisticas" and com[0] != "comunidades" and com[0] != "salir" and com[0] != "" and len(com) == 1:
		return False
	return com[0] in lista_comandos
