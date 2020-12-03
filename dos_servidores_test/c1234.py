# ############
# Cliente 1234 
# ############

import socket
from pickle import dumps

c=socket.socket()
c.connect(('',1234))

while True:

   lista=[]
   cedula=input("Introduzca cedula: ")
   opcion=input(" 1. Registrar, 2. Presentar examen: ")

   lista.append(cedula)
   lista.append(opcion)

   objeto=dumps(lista)

   c.send(objeto)

   msg=c.recv(1024).decode()
   print(msg)
   print("Cliente: saliendo")
   break

c.close()

