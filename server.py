#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import time
import json


class SIPRegisterHandler(socketserver.DatagramRequestHandler):

    dicc_registro = {}

    def handle(self):
        """
        funcion que responde con un OK si llega un REGISTER correctamente
        almacena los clientes y su direccion y expire en un diccionario
        importa y exporta el diccionario a un archivo json
        """
        self.json2registered()
        self.elimina_expires()
        info_usuario = {}
        for line in self.rfile:
            linea_decod = line.decode('utf-8').split(" ")
            if linea_decod[0] == "REGISTER":
                usuario = linea_decod[1]
                self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                info_usuario["address"] = self.client_address[0]
                self.dicc_registro[usuario] = info_usuario
            elif linea_decod[0] == "Expires:":
                expires = int(linea_decod[1])
                tiempo_fin = time.strftime('%Y-%m-%d %H:%M:%S',
                                           time.gmtime(time.time() + expires))
                self.dicc_registro[usuario]["expires"] = tiempo_fin
                if expires == 0:
                    del self.dicc_registro[usuario]
        self.register2json()
        # print("Llega mensaje desde la direccion", self.client_address)
        print(self.dicc_registro)

    def register2json(self):
        """ funcion que pasa el diccionario de clientes a json"""
        with open("registered.json", 'w') as file:
            json.dump(self.dicc_registro, file)

    def json2registered(self):
        """lee un archivo json para importar un diccionario de clientes"""
        try:
            with open("registered.json") as f:
                datos_json = json.load(f)
                self.dicc_registro = datos_json
        except:
            pass

    def elimina_expires(self):
        """elimina clientes que han expirado en el diccionario"""
        hora_actual = time.strftime('%Y-%m-%d %H:%M:%S',
                                    time.gmtime(time.time()))
        for usuario in list(self.dicc_registro.keys()):
            if hora_actual >= self.dicc_registro[usuario]['expires']:
                del self.dicc_registro[usuario]


if __name__ == "__main__":
    """
    escucha en el puerto PORT y abre un servidor para peticiones SIP
    escucha indefinidamente hasta que se finaliza el servidor
    """
    PORT = int(sys.argv[1])
    serv = socketserver.UDPServer(('', PORT), SIPRegisterHandler)
    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
