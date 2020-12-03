import socket, threading
from pickle import loads, dumps
import time
from servidor_generacion_password_aleatorio import cadena_aleatoria
#from servidor_generacion_preguntas_aleatorias import preguntas_aleatorias
from servidor_envio_recepcion import *
from servidor_modelo import  calcular_nota, chequear_cedula_password_examen, armar_preguntas,actualizar_informacion_aspirante
from servidor_configuracion import *
from servidor_guardar_info_archivo import guardar_info_archivo
from fechas_horario_permitido import fechas_horario_permitido

#IPSAUTORIZADAS=['127.0.0.1'] la toma de servidor_configuracion


class threadCliente(threading.Thread):

    def __init__(self,direccionCliente, socketcliente):
        threading.Thread.__init__(self)
        self.csocket = socketcliente 
        print ("Nueva conexion agregada: ", direccionCliente)

    def run(self):
        print ("Conexion desde : ", direccionCliente)

        while True:
            
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

            break

        print ("Cliente en la direccion: ", direccionCliente , " desconectado...")
        self.csocket.close() 


DIRECCIONIP = "127.0.0.1"
PUERTO = 8080

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
    threadnuevo = threadCliente(direccionCliente, socketcliente)
    threadnuevo.start()
