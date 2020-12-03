import socket, select,threading
from queue import Queue
from pickle import loads, dumps
import time
from registrar_estudiante import  chequear_cedula, formulario, insertar_cedula_de_otro_nodo, registrar_estudiante

from servidor_generacion_password_aleatorio import cadena_aleatoria
#from servidor_generacion_preguntas_aleatorias import preguntas_aleatorias
from servidor_envio_recepcion import *
from servidor_modelo import  calcular_nota, chequear_cedula_password_examen, armar_preguntas,actualizar_informacion_aspirante
from servidor_configuracion import *
from servidor_guardar_info_archivo import guardar_info_archivo
from fechas_horario_permitido import fechas_horario_permitido

#IPSAUTORIZADAS=['127.0.0.1'] la toma de servidor_configuracion

# ################################################################
# Servidor 4321 cliente 1234
# ################################################################  


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

# #############################################################################################################



class threadCliente(threading.Thread):

    def __init__(self,direccionCliente, socketcliente, q_in, q_out):
        threading.Thread.__init__(self)
        self.csocket = socketcliente 
        print ("Nueva conexion agregada: ", direccionCliente)

    def run(self):
        print ("Conexion desde : ", direccionCliente)
        c=self.csocket

        while not q_in.empty():
           cedula_maracay=q_in.get()
           print("Insertando en base de datos: ", cedula_maracay)
           Maracay.append(cedula_maracay) #Introducir solo password en BD indicando que es del otro nodo 
           print("Maracay :", Maracay)
           if chequear_cedula(cedula_maracay)==1:
              insertar_cedula_de_otro_nodo(cedula_maracay)
           
        objeto=c.recv(1024) #Se recibe lista ['223','1'] con cedula y opcion:   1:  Registro,  2: Presentar examen
        print("Recibido objeto")
        lista=loads(objeto)
        cedula=lista[0]
        opcion=lista[1]
        
        print("Cedula",cedula)
        print("Opcion",opcion)
 
        if opcion=='1':   #Registro
           #if cedula in Maracay:
           if chequear_cedula(cedula)==2:
              c.send(bytes("Usted esta inscrito en el  nodo Maracay debe presentar alla",'utf-8'))
           #elif cedula not in Caracas:
           if chequear_cedula(cedula) ==1: #Usuario no existe
              Caracas.append(cedula) 
              print("Caracas:", Caracas)
              q_out.put(cedula)  #Se coloca en cola de salida para notificar al otro nodo
              c.send(bytes("OK",'utf-8')) #Puede inscribirse
              objeto=c.recv(1024) #Recibe nombre y apellido
              lista=loads(objeto)
              print(lista[0])
              print(lista[1])
              password=cadena_aleatoria() #genera password aleatorio
              registrar_estudiante(lista[0],lista[1],cedula,password)        #Registra al estudiante
              c.send(bytes("Usted acaba de inscribirse en este nodo, use este string junto a su cedula para presentar:" + password,'utf-8'))
           else:
              c.send(bytes("Usted ya esta inscrito en este nodo",'utf-8'))
           
        elif opcion=='2': #Presentar examen

              #if cedula in Maracay:
              if chequear_cedula(cedula)==2:
                 c.send(bytes("Usted esta inscrito en el  nodo Maracay debe presentar alla",'utf-8'))
              #elif cedula not in Caracas:
              elif chequear_cedula(cedula) ==1: #Usuario no existe
                 c.send(bytes("Usted no esta inscrito debe inscribirse",'utf-8'))
              else:
                 c.send(bytes("PRESENTAR",'utf-8'))
                 #1.) SERVIDOR RECIBE credencial ['cedula','password']
                 credencial=recibir_objeto(self.csocket)
                 cedula=credencial[0]
                 print("Cedula: ",credencial[0]) 

                 #2.) SERVIDOR ENVIA codigo 0,1,2 o 3
                 codigo=chequear_cedula_password_examen(credencial)
                 print(codigo)
                 enviar_mensaje(self.csocket,str(codigo)) 
                 if codigo==0:                   
                     ### Cedula password OK y no ha presentado  
                     print("Enviando examen")
                     #### Cedula y password OK y no ha presentado

                     #3.) SERVIDOR ENVIA examen con preguntas aleatorias 
                     preguntas=armar_preguntas()
                     enviar_objeto(self.csocket,preguntas)

                     #4.) SERVIDOR RECIBE respuestas del examen
                     respuestas=recibir_objeto(self.csocket)
                     print(respuestas)

                     ### Servidor calcula la nota del examen, actualiza BD  y envia resultado 
                     nota_examen=calcular_nota(respuestas)
                     print(nota_examen)                   
                     print(credencial[0])
                     actualizar_informacion_aspirante(cedula,nota_examen)
                     ### Esta parte consiste en guardar las respuestas en un archivo 
                     ### cuyo nombre es la cedula del aspirante en formato binario como constancia
                     guardar_info_archivo(cedula,respuestas)

                     #5.) SERVIDOR ENVIA nota del examen 
                     enviar_mensaje(self.csocket,nota_examen)            

            #break
        print ("Cliente en la direccion: ", direccionCliente , " desconectado...")
        self.csocket.close() 


DIRECCIONIP = "127.0.0.1"
PUERTO = 4321 

q_in=Queue()  # Servidor 4321 lee de aqui, cliente 1234 escribe aqui
q_out=Queue() # Servidor 4321 escribe aqui, cliente 1234 lee de aqui
th=threading.Thread(target=cliente1234, args=(q_in, q_out, ))
th.start()

Caracas=[]
Maracay=[]


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((DIRECCIONIP, PUERTO))
print("Servidor en funcionamiento")
print("Esperando por conexion de clientes..")

while True:
    server.listen(5)
    socketcliente, direccionCliente = server.accept()
    # IPs AUTORIZADAS 
    #Chequeo de direcciones IP autorizadas el cliente se conectara, sino es aceptado
    #no sabra que ha sido desconectado pedira cedula y password y se saldra.

    if direccionCliente[0] not in IPSAUTORIZADAS:   #and fechas_horario_permitido(): 
       socketcliente.close() 
       continue 

    #Si la ip es aceptada se creara el thread que la atienda 
    threadnuevo = threadCliente(direccionCliente, socketcliente,q_in, q_out)
    threadnuevo.start()
