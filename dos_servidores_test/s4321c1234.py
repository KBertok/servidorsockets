# ##########################
# Servidor 4321 cliente 1234 
# ##########################

#!/usr/bin/python

import socket, select
from queue import Queue
from threading import Thread

##################
# Cliente de  1234
# ################

def cliente1234(q_in, q_out):  #Comparte colas con servidor 4321 para comunicacion por memoria compartida

   c=socket.socket()
   c.connect(('',10000))

   ensal = [c]

   while True:
           en, sal, err = select.select(ensal, ensal, [], 5)
           if len(en) != 0:
                   msg = c.recv(1024).decode()
                   if len(msg) != 0:
                           print ('recibido:', msg)
                           # lo que le llega lo escribe en q_in para que el servidor 4321 lo lea
                           q_in.put(msg) 

           if len(sal) != 0:
                   if not q_out.empty(): # Lee lo que server 4321 escribe en q_out y lo envia al otro servidor
                      msg=q_out.get()
                      c.send(bytes(msg,'utf-8'))
   c.close()

# ###################################################################


q_in=Queue()  # Servidor 4321 lee de aqui, cliente 1234 escribe aqui
q_out=Queue() # Servidor 4321 escribe aqui, cliente 1234 lee de aqui

th=Thread(target=cliente1234, args=(q_in, q_out, ))
th.start()

Caracas=[]
Maracay=[]


# #############
# Servidor 4321 
# #############

import socket
from pickle import loads

s=socket.socket()
s.bind(('',4321))
s.listen(3)

while True:
   c , d = s.accept()
   while not q_in.empty():
      Maracay.append(q_in.get())
      print("Maracay :", Maracay)
   
   objeto=c.recv(1024) #Se recibe lista ['123','1'] con cedula y opcion:   1:  Registro,  2: Presentar examen
   lista=loads(objeto)
   cedula=lista[0]
   opcion=lista[1]
   

   print("Cedula",cedula)
   print("Opcion",opcion)

   if opcion=='1':   #Registro

      if cedula in Maracay:
         c.send(bytes("Usted esta inscrito en el  nodo Maracay debe presentar alla",'utf-8'))
      elif cedula not in Caracas:
         Caracas.append(cedula) 
         print("Caracas:", Caracas)
         q_out.put(cedula)
         c.send(bytes("Usted quedo inscrito en el nodo Caracas",'utf-8'))
      else:
         c.send(bytes("Usted ya esta inscrito en este nodo",'utf-8'))
   
   elif opcion=='2': #Presentar examen
      
      if cedula in Maracay:
         c.send(bytes("Usted esta inscrito en el  nodo Maracay debe presentar alla",'utf-8'))
      elif cedula not in Caracas:
         c.send(bytes("Usted no esta inscrito debe inscribirse",'utf-8'))
      else:
         c.send(bytes("Usted ya esta inscrito  en este nodo y puede comenzar a presentar el examen",'utf-8'))
              




