from servidor_configuracion import *
import sqlite3
from servidor_generacion_preguntas_aleatorias import preguntas_aleatorias
from pickle import dumps

"""
ESTRUCTURA DE TABLAS Y QUERIES Y COMANDOS MAS USADOS PARA ADMIN Y PROG
----------------------------------------------------------------------
CREATE TABLE `estudiante` (
	`Nombre`	TEXT,
	`Apellido`	TEXT,
	`Cedula`	NUMERIC,
	`Password`	TEXT,
	`Presento`	TEXT,
	`Resultado`	TEXT,
	`Fecha`	TEXT,
	`Examen`	INTEGER,
	PRIMARY KEY(`Cedula`,`Examen`)
);


CREATE TABLE `pregunta` (
	`Numero`	INTEGER,
	`Pregunta`	TEXT,
	`Respuesta1`	TEXT,
	`Respuesta2`	TEXT,
	`Respuesta3`	TEXT,
	`Respuesta4`	TEXT,
	`Respuesta`	INTEGER,
	`Examen`	INTEGER,
	PRIMARY KEY(`Numero`,`Examen`)
);

UPDATE
------
update estudiante set cedula=11512399 where cedula=11512400
update estudiante set Presento='Si' where cedula=11512399 
update estudiante set Resultado='4/6' where cedula=11512399
update estudiante set Fecha = datetime('now') where cedula=11512399

String query = "UPDATE myTable SET displayed = datetime('now') where _id = " + id;

SELECT
------
select Presento from estudiante where cedula=11512399 
select Fecha from estudiante where cedula=11512399
select Resultado from estudiante where cedula=11512399
select Examen from estudiante where cedula=11512399

BACKUP DE .db a .sql
--------------------
$ sqlite3 servidor_BD_examenes.db .dump > servidor_BD_examenes.sql 


RESTORE de .sql a .db
---------------------
$ cat servidor_BD_examenes.sql > sqlite3 prueba.db 


"""
BASEDEDATOS='servidor_BD_examenes.db'

def crear_conexion(BASEDEDATOS):
    """Crea una conexion a la base de datos sqlite 
        Concretamente BASEDEDATOS 
    BASEDEDATOS::Archivo de base de datos 
    :Retorna: Un objeto conexion o  None
    """
    conn = None
    try:
        conn = sqlite3.connect(BASEDEDATOS)
    except Error as e:
        print(e)
 
    return conn


def selecciona_todos_estudiantes(conn):
    """
    Es un query a la tabla de estudiante
    que retorna una lista de tuplas
    donde cada tupla es la informacion
    relativa a cada estudiante.
    fetchone retorna una tupla y fetchall
    una lista de tuplas. Las tuplas son elementos
    inmutables
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM estudiante")
 
    estudiantes = cur.fetchone()
 
    print(estudiantes)
    conn.commit()
    conn.close()



def armar_preguntas():
   """
   Selecciona NRO_PREGUNTAS_ESCOGER parametro
   que  se encuentra en configuracion_servidor
   llamando
   a preguntas_aleatorias, conectandose a la
   Base de Datos y extrayendolas de la
   tabla de preguntas y retornando una lista 
   de tuplas que el servidor de sockets envia
   al cliente con enviar_objeto()
   """
   conn=crear_conexion(BASEDEDATOS) 
   cur=conn.cursor()
   preg=preguntas_aleatorias() 
   lista_preguntas=[] 
   for p in preg: 
      cur.execute('select Numero,Pregunta,Respuesta1,Respuesta2,Respuesta3,      \
                          Respuesta4 from pregunta where Numero ={0}'.format(p))
      pregunta=cur.fetchall()
      for p in pregunta:
         lista_preguntas.append(p)
   conn.commit()
   conn.close() 
   return lista_preguntas



def calcular_nota(resp):
  """    
  resp es un dicionario {preg:resp, preg:resp, preg:resp} enviado por cliente
  en base a la lista de tuplas (preguntas) enviadas por el servidor
  que crea y envia despues de responder el examen
  este diccionario es recorrido por esta funcion conectandose a la tabla 
  preguntas de la base de datos y chequeando su respuesta comparandola
  con la que aparece en el diccionario
  """
   
  conn=crear_conexion(BASEDEDATOS) 
  cur=conn.cursor()
  acertadas=0
  nro_preguntas=len(resp)
  #nro_preguntas=NUMERO_PREGUNTAS_ESCOGER
  print(resp)
  for preg in resp:
     cur.execute('select Respuesta from pregunta where Numero={0}'.format(preg))
     respuesta=cur.fetchall()
     if  respuesta[0][0] == resp[preg]:
        acertadas += 1
  conn.commit()
  conn.close()
  return   str(acertadas) + "/"+ str(nro_preguntas) 





def chequear_cedula_password_examen(credencial): #Al aspirante se le pide cedula y password de una vez
   """ Cedula es un entero en la base de datos   #credencial =  ['cedula','password']


       retorna 0, cedula ok, password Ok y no ha presentado, (puede presentar) enviar lista de preguntas al azar
       retorna 1, no encuentra cedula, la consulta no devuelve tuplas. mensaje (usuario no registrado o credenciales erroneas)
       retorna 2, cedula y password ok pero aspirante ya presento examen,  mensaje (Aspirante ya presento examen) 
       retorna 3, cedula ok pero password erroneo, mensaje (credenciales erroneas)
   """ 
   conn=crear_conexion(BASEDEDATOS)
   cur=conn.cursor()
   cur.execute("select Cedula,Password,Presento from estudiante where Cedula='{0}'".format(credencial[0]))
   
   respuesta=cur.fetchall()
   conn.commit()
   conn.close()
   print(respuesta)                       #respuesta=[(cedula,password,presento)] o [()] donde credencial=[cedula,password]
   if len(respuesta)==1:                  #Cedula OK, genero una entrada lo cual indica que cedula existe
      print(len(respuesta))
      print(respuesta)
      if respuesta[0][1]==credencial[1]:  #Password OK  
         if respuesta[0][2]=='Si':
            #Cedula y password Ok pero aspirante ya presento
            return 2
         else: #Cedula ok, password Ok y aspirante no ha presentado
            return 0   
      else:
         return 3   #Cedula Ok pero password erroneo --> credenciales erroneas
   else:
      return 1      # Aspirante no registrado, puesto que la consulta no genero salida no encontro cedula    





def actualizar_informacion_aspirante(cedula,nota_examen):     #Despues que presenta y envia resultados el servidor actualiza su info
   """
      Actualiza status de que ha presentado la prueba
      Actualiza es decir inserta su resultado en el examen, adicionalmente deja como constancia un archivo en directorio
      con nombre la cedula del aspirante y contenido cedula y dicionario con  numero de las preguntas y respuestas
      inserta la fecha y hora basicamente  del momento de recepcion de resultados y calculo de la nota
   """   
   conn=crear_conexion(BASEDEDATOS)
   cur=conn.cursor()
   cur.execute("update estudiante set Presento='Si' where cedula='{0}'".format(cedula))
   cur.execute("update estudiante set Resultado='{0}' where cedula='{1}'".format(nota_examen,cedula))
   cur.execute("update estudiante set Fecha = datetime('now') where cedula='{0}'".format(cedula)) 

   conn.commit()
   conn.close()



   

if __name__=="__main__":
   #print(armar_preguntas())
   #calcular_nota({25:3,26:2,27:3,28:4,29:4,30:4})
   #calcular_nota({30: 0, 17: 0, 6: 0, 22: 0})
   #print(calcular_nota({26: 0, 8: 0, 4: 0, 13: 0}))
   #credencial=[]
   cedula=input('Introduzca cedula: ' )
   #credencial.append(cedula)
   #password=input('Introduzca password: ')
   #credencial.append(password) 
   #print(chequear_cedula_password_examen(credencial))
   #actualizar_informacion_aspirante(cedula,'3/5')
       
