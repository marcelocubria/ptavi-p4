#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys


class SIPRegisterHandler(socketserver.DatagramRequestHandler):

    dicc_registro = {}

    def handle(self):
        """
        handle method of the server class
        (all requests will be handled by this method)
        """
        for line in self.rfile:
            linea_decod = line.decode('utf-8').split(" ")
            if linea_decod[0] == "REGISTER":
                print("me llega un register")
                usuario = linea_decod[1]
                self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                self.dicc_registro[linea_decod[1]] = self.client_address
            elif linea_decod[0] == "Expires:":
                if int(linea_decod[1]) == 0:
                    del self.dicc_registro[usuario]
                    print("he borrado a " + usuario)
        print("Desde la direccion", self.client_address)


if __name__ == "__main__":

    PORT = int(sys.argv[1])
    # Listens at localhost ('')
    # and calls the EchoHandler class to manage the request
    serv = socketserver.UDPServer(('', PORT), SIPRegisterHandler)

    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
