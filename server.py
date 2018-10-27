#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        """
        handle method of the server class
        (all requests will be handled by this method)
        """
        cabecera = self.rfile.readline().decode('utf-8')
        if cabecera.split()[0] == "REGISTER":
                print("me llega un register")
                self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
        print("Desde la direccion", self.client_address)

if __name__ == "__main__":
    
    PORT = int(sys.argv[1])
    # Listens at localhost ('') port 6001 
    # and calls the EchoHandler class to manage the request
    serv = socketserver.UDPServer(('', PORT), SIPRegisterHandler) 

    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
