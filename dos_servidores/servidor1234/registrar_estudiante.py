import sqlite3
import subprocess as sp
from servidor_generacion_password_aleatorio import cadena_aleatoria

"""
database code
"""

DATABASE='servidor_BD_examenes.db'


def registrar_estudiante(Nombre,Apellido,Cedula,Password):
        conn = sqlite3.connect(DATABASE)

        cursor = conn.cursor()
        cursor.execute("select Cedula from estudiante where Cedula='{0}'".format(Cedula))
        respuesta=cursor.fetchall()
        conn.commit()
        if len(respuesta) == 0:      #No hay nadie registrado con esa cedula

           query = '''
               INSERT INTO estudiante( Nombre, Apellido, Cedula, Password)
                           VALUES ( ?,?,?,?)
           '''
           cursor.execute(query,(Nombre,Apellido,Cedula,Password))

           conn.commit()
           conn.close()
        else: 
           print("Aspirante ya registrado") 


def chequear_cedula(Cedula):

   conn = sqlite3.connect(DATABASE)
   cur=conn.cursor()
   cur.execute("select Cedula,Password from estudiante where Cedula='{0}'".format(Cedula))
   respuesta=cur.fetchall()
   conn.commit()
   conn.close()
   print(respuesta)

   if len(respuesta)==0:
      print("Usuario sin password no existente")
      return 1 # Usuario no existente debe registrarse
   elif respuesta[0][1] == None:
      print("Password None esta en el otro nodo")
      return 2 # Esta en el otro nodo
   else:
      print("Password puesto")
      return 3 # Esta en este nodo



def insertar_cedula_de_otro_nodo(cedula):

   conn = sqlite3.connect(DATABASE)
   cur=conn.cursor()
   
   cedula=int(cedula)
   cur.execute("insert into estudiante (Cedula) values(?)", (cedula,))
   print(cedula,type(cedula))
   conn.commit()
   conn.close()


def formulario(cedula):
   Nombre = input('Nombre: ')
   Apellido = input('Apellido: ')
   #Cedula = int(input('Cedula: '))
   Cedula=int(cedula)
   Password=cadena_aleatoria()
   print("Al presentar el examen el aspirante ingresara con su cedula y password: ",Password)
   input("\n\nPresionar enter para registrar al aspirante:")
   registrar_estudiante(Nombre,Apellido,Cedula,Password)



if __name__=="__main__":
   #print(chequear_cedula_otro_nodo('33333333'))
   #print(chequear_cedula_otro_nodo('11111111'))
   #print(chequear_cedula_otro_nodo('1111'))
   #insertar_cedula_de_otro_nodo('6')     
   #if chequear_cedula_otro_nodo('5') == 2:
   #   print("Cedula 5 en otro nodo")
   #insertar_cedula_de_otro_nodo('127')
   print(chequear_cedula('11'))         

