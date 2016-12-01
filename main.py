from parse import parse
from grafo import Grafo

lista_comandos = { "": "", "similares": "", "recomendar": "", "camino": "", "centralidad": "", "distancias": "",
"estadisticas": "", "comunidades": "" }

uso = "Uso:\n\
	> similares <personaje> [cantidad]\n\
	> recomendar <personaje> [cantidad]\n\
	> camino <personaje_1> <personaje_2>\n\
	> centralidad [cantidad]\n\
	> distancias <personaje>\n\
	> estadisticas\n\
	> comunidades"

def camino(grafo, p1, p2):
	caminos = grafo.camino_minimo(p1, p2)
	camino = [p2]
	return _camino(caminos, p1, p2, caminos)[::-1]

def _camino(caminos, p1, p2, camino):
	if caminos[p2].padre == p1:
		camino.append(caminos[p2].padre)
		return camino
	camino.append(caminos[p2].padre)
	return _camino(caminos, p1, caminos[p2].padre)


def validar_comando(comando):
	com = comando.split(" ")
	if com[0] != "estadisticas" and com[0] != "comunidades" and com[0] != "" and len(com) == 1:
		return False
	return com[0] in lista_comandos

def main():
	grafo = parse("marvel.pjk")
	while True:
		try:
			comando = input("> ")
			if not validar_comando(comando):
				print(uso)
				continue
			if comando.split(" ")[0] == "distancias":
		except (KeyboardInterrupt):
			print()
			continue

if __name__ == "__main__":
	main()
