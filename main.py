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
		except (KeyboardInterrupt):
			print()
			continue

if __name__ == "__main__":
	main()