import random
import socket
import sys
#definimos las palabras depeniendo su dificultad
facil =  [
    'perro',
    'gato',
    'oso',
    'pez'
]
medio = [
    'ardilla',
    'elefante',
    'pulpo',
    'tortuga'
]
dificil = [
    'ornitorrinco',
    'puercoespin',
    'hipopotamo',
    'cocodrilo'
]
#Creamos el socket y usamos la opcion de REUSEADDR para poder reusar el puerto   
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
#definimos la dirección y puerto, y lo ponemos a escuchar.
server_address = ('localhost', 8888)
sock.bind(server_address)
sock.listen()
#Entramos a un bucle donde esperará conexiones
while True:
    print('Esperando para conectarse...')
    #acepta una conexión del cliente.
    con, addr = sock.accept()
    try:
        print('jugador conectado!')
        #recibimos la opción de dificultad, y establecemos fallos y el set de palabras a utilizar con base en la respuesta.
        dificultad = con.recv(32)
        print('Juego Iniciado...')

        if dificultad == b'1':
            fallos = 4
            palabras = facil
            dif = 'facil'

        elif dificultad == b'2':
            fallos = 4
            palabras = medio
            dif = 'medio'

        else:
            fallos = 5
            palabras = dificil
            dif = 'dificil'

        palabra = random.choice(palabras)
        print('Juego actual: ', palabra)
        num_letras = '_ ' * len(palabra)

        #mandamos por el socket la palabra en formato _____

        juego = b'Ahorcado -- Dificultad ' + bytes(dif,encoding="utf-8") + b' Tema: animales \n'+ b'\n' + bytes(num_letras, encoding="utf-8")  
        con.sendall(juego)
        intento_palabra = num_letras

        #Entramos a un bucle para recibir letras del cliente, por eso solo recibimos 8 bytes.
        while 1:
            sys.stdin.flush()
            letra_recibida = con.recv(8)
            letra_recibida = str(letra_recibida, encoding="utf-8")
            print(f"letra recibida = {letra_recibida}")
            actualizacion_juego = intento_palabra.split()
            #Entramos en un for para comparar la letra recibida con las letras de la palabra original, si la hayamos, remplazamos el _ por la letra
            for x in range(len(palabra)):
                if letra_recibida == palabra[x-1]:
                    actualizacion_juego[x-1] = letra_recibida
            print(f"Actualizacion = {actualizacion_juego}")

            #Si no encontramos, restamos un fallo.
            if str(letra_recibida) not in palabra:
                fallos -= 1

            intento_palabra = ' '.join(actualizacion_juego)
            estatus = bytes(intento_palabra, encoding="utf-8") + b'''
            Fallos restantes: ''' + bytes(str(fallos), encoding="utf-8") + b'\n'
            con.sendall(estatus)
            #comprobamos si existen símbolos _, cuando ya no haya, quiere decir que se adivinó todo
            if '_' not in intento_palabra:
                con.send(b'\nGanaste!\n')
                sys.stdin.flush()
                break
            #Si los fallos son 0, se perdió
            elif fallos == 0:
                con.send(b'\nPerdiste :(\n')
                sys.stdin.flush()
                break
    finally:
        con.close()