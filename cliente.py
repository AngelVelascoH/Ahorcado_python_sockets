import socket
import sys

#Creamos el socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost',8888 )
sock.connect(server_address)

try:
    #Imprimimos el menú cuando la conexión sea exitosa.
    print("""
        ---Ahorcado---

        Selecciona la dificultad:
        1-Facil
        2-Medio
        3-Dificil

        Tematica: Animales


        """)

    
    #Mandamos la dificultad
    dificultad = bytes(str(input('Selecciona: ')), encoding="utf-8")
    sock.sendall(dificultad)
    #Recibimos la palabra con el formato ___
    palabra = sock.recv(254)
    print(palabra.decode("utf-8"))
    print("\n")

    #Entramos a un ciclo para mandar letras
    while True:
        sys.stdin.flush()
        letra = bytes(str(input('> ')), encoding="utf-8")
        sock.sendall(letra)
        resultado = sock.recv(512)
        print(resultado.decode("utf-8") + "\n\n")

        #Si ya no hay _ seguimos salimos
        if '_' not in resultado.decode("utf-8"):
            break
        #Si dentro del mensaje recibido, hay un 0, quiere decir que son los 0 fallos restantes.
        elif '0' in resultado.decode("utf-8"):
            break
            
except:
    print('Fin de conexion...')

