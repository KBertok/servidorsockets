import socket, select
from queue import Queue
from threading import Thread



# ##################################
# Comunicacion  con cliente de s4321 
# ##################################

def servidor(q_in, q_out):

   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   s.bind(('', 10000))
   s.listen(5)
   entradas = [s]

   while True:
           en, sal, err = select.select(entradas, entradas, [], 5)
           if len(en) != 0:
                   for f in en:
                           if f is s:
                                   c, a = f.accept()
                                   entradas.append(c)
                           else:
                                   datos = f.recv(1024).decode()
   
                                   if not datos:
                                       entradas.remove(f)
                                   else:
                                       print ("Recibido :",datos)
                                       q_in.put(datos)
           if len(sal) != 0:
                   for f in sal:
                           if not q_out.empty():
                              msg=q_out.get()
                              f.send(bytes(msg,'utf-8'))

# #######################################################################################

q_in=Queue()  # Servidor 1234 lee de aqui, servidor  escribe aqui
q_out=Queue() # Servidor 1234 escribe aqui, servidor  lee de aqui

th=Thread(target=servidor, args=(q_in, q_out, ))
th.start()

Caracas=[]
Maracay=[]

# #############
# Servidor 1234 
# #############

import socket 
from pickle import loads

s=socket.socket()
s.bind(('',1234))
s.listen(3)


while True:
   c , d = s.accept()
   while not q_in.empty():
      Caracas.append(q_in.get())
      print("Caracas :", Caracas)

   objeto=c.recv(1024) #Se recibe lista ['223','1'] con cedula y opcion:   1:  Registro,  2: Presentar examen
   lista=loads(objeto)
   cedula=lista[0]
   opcion=lista[1]

   print("Cedula",cedula)
   print("Opcion",opcion)


   if opcion=='1':   #Registro

      if cedula in Caracas:
         c.send(bytes("Usted esta inscrito en el  nodo Caracas debe presentar alla",'utf-8'))
      elif cedula not in Maracay:
         Maracay.append(cedula)
         print("Maracay:", Maracay)
         q_out.put(cedula)
         c.send(bytes("Usted quedo inscrito",'utf-8'))
      else:
         c.send(bytes("Usted ya esta inscrito en esta nodo",'utf-8'))

   elif opcion=='2': #Presentar examen

      if cedula in Caracas:
         c.send(bytes("Usted esta inscrito en el  nodo Caracas debe presentar alla",'utf-8'))
      elif cedula not in Maracay:
         c.send(bytes("Usted no esta inscrito debe inscribirse",'utf-8'))
      else:
         c.send(bytes("Usted ya esta inscrito  en este nodo y puede comenzar a presentar el examen",'utf-8'))


