import socket
from pickle import dumps,loads
import time 
from cliente_presentar_prueba import presentar_prueba
from cliente_envio_recepcion import *
from ingresar_cedula_password import ingresar_cedula_password
from time import sleep
from registrar_estudiante import formulario
import re    # Para asegurarse que cedula y opcion son correctamente introducidos 

SERVIDOR = "127.0.0.1"

PUERTO= 1234 

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((SERVIDOR, PUERTO))


while True:
   c=cliente
   lista=[]

   #cedula=input("Introduzca cedula: ")

   while True:
      cedula=input("Introduzca cedula (solo numeros) >")
      cedula=re.sub(r"\s+", "", cedula)
      print(cedula)
      if cedula.isdigit():
         break
      else:
         pass

   #opcion=input(" 1. Registrar, 2. Presentar examen: ")

   while True:
      opcion=input("1. Registrar, 2. Presentar examen: (solo numeros 1 o 2) >")
      opcion=re.sub(r"\s+", "", opcion)
      print(opcion)
      if opcion.isdigit() and (opcion=='1' or opcion=='2'):
         break
      else:
         pass

   lista.append(cedula)
   lista.append(opcion)
   print(lista)
   objeto=dumps(lista)

   c.send(objeto)
   msg=c.recv(1024).decode()
   if msg=='OK':
      nombre=input("Introduzca su Nombre: ") 
      apellido=input("Introduzca su Apellido: ")
      lista=[]
      lista.append(nombre)
      lista.append(apellido)
      objeto=dumps(lista)
      c.send(objeto)
      msg=c.recv(1024).decode()
      print("Imprimiendo por el if")
      print(msg) # En este mensaje se le dice al aspirante que ya esta inscrito y se le proporciona string aleatorio 
      break
   else:
      print("Imprimiendo por el else")
      print(msg)
   if msg=='PRESENTAR':  
      #1.) CLIENTE ENVIA credencial ['cedula','password']
      credencial=ingresar_cedula_password()    
      cedula=credencial[0]
      #Si fue desconectado por el servidor por ip no autorizada    
      #Despues de rellenar cedula y password y dar enter se saldra
      enviar_objeto(cliente,credencial)

      #2.) CLIENTE RECIBE codigo 0,1,2 o 3
      codigo=recibir_mensaje(cliente) 
      if codigo=='3':
         print("Ingreso credenciales erroneas")
         break
      elif codigo=='2': 
         print("El aspirante ya presento la prueba")
         break
      elif codigo=='1':
         print("Credenciales erroneas o no se encuentra registrado")
         break
      elif codigo=='0':  #Solo en este caso se continua intercambio de mensajes
         print("El aspirante presentara la prueba a continuacion")  

         #3.)CLIENTE RECIBE examen con preguntas aleatorias 
         preguntas=recibir_objeto(cliente)
         print(preguntas)

         ### Cliente efectua examen y envia respuestas 
         respuestas=presentar_prueba(preguntas)
         print(respuestas)
         #4.) CLIENTE ENVIA respuestas {preg i: resp i, preg j: resp j}
         enviar_objeto(cliente,respuestas)
 
         #5.)CLIENTE RECIBE nota de examen
         nota_examen=recibir_mensaje(cliente)
         print("El aspirante: ",cedula,"obtuvo: ",nota_examen,"respuestas acertadas") 
   print("Cliente saliendo") 
   break 

c.close()
