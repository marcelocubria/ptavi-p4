#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente UDP que abre un socket a un servidor
"""

import socket
import sys

# Constantes. Dirección IP del servidor y contenido a enviar
SERVER = sys.argv[1]
PORT = int(sys.argv[2])
PETICION = sys.argv[3]
ADDRESS = sys.argv[4]
EXPIRES = sys.argv[5]

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    """
    envia un paquete de registro con la direccion ADDRESS
    a SERVER en el puerto PORT, con un valor de EXPIRES
    """
    my_socket.connect((SERVER, PORT))
    linea_registro = "REGISTER sip:" + ADDRESS + " SIP/2.0\r\n"
    linea_registro += "Expires: " + EXPIRES + "\r\n\r\n"
    print(linea_registro)
    my_socket.send(bytes(linea_registro, 'utf-8'))
    data = my_socket.recv(1024)
    print('Recibido -- ', data.decode('utf-8'))

print("Socket terminado.")
