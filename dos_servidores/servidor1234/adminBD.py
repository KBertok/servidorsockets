"""
importantes links para usar sqlite en python:
http://sebastianraschka.com/Articles/2014_sqlite_in_python_tutorial.html
http://www.pythoncentral.io/introduction-to-sqlite-in-python/
"""


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

	query = '''
	    INSERT INTO estudiante( Nombre, Apellido, Cedula, Password)
	    	        VALUES ( ?,?,?,?)
	'''

	cursor.execute(query,(Nombre,Apellido,Cedula,Password))

	conn.commit()
	conn.close()



def obtener_estudiantes():
	conn = sqlite3.connect(DATABASE)

	cursor = conn.cursor()

	query = '''
	    SELECT Nombre, Apellido, Cedula, Password, Presento, Fecha,Resultado
	    FROM estudiante
	'''

	cursor.execute(query)
	all_rows = cursor.fetchall()

	conn.commit()
	conn.close()

	return all_rows


def obtener_estudiante_por_cedula(Cedula):
	conn = sqlite3.connect(DATABASE)

	cursor = conn.cursor()

	query = '''
	    SELECT Nombre, Apellido, Cedula, Password,Presento, Fecha, resultado
	    FROM estudiante
	    WHERE Cedula = {}
	''' .format(Cedula)

	cursor.execute(query)
	all_rows = cursor.fetchall()

	conn.commit()
	conn.close()

	return all_rows



def borrar_estudiante(Cedula):
	conn = sqlite3.connect(DATABASE)

	cursor = conn.cursor()

	query = '''
	    DELETE
	    FROM estudiante 
	    WHERE Cedula = {}
	''' .format(Cedula)

	cursor.execute(query)
	all_rows = cursor.fetchall()

	conn.commit()
	conn.close()

	return all_rows

"""
Interfaz o bucle principal
"""

def mostrar_datos():
	estudiantes = obtener_estudiantes()
	for estudiante in estudiantes:
		print(estudiante)

def mostrar_datos_por_cedula(Cedula):
	estudiantes = obtener_estudiante_por_cedula(Cedula)
	if not estudiantes:
		print("No hay datos de estudiantes con la cedula:",Cedula)
	else:
		print (estudiantes)

def seleccionar():
	sp.call('clear',shell=True)
	sel = input("1.Registrar Estudiante\n2.Mostrar estudiantes\n3.Buscar estudiantes\n4.Borrar\n5.Exit\n\n")
	if sel=='1':
		sp.call('clear',shell=True)
		Nombre = input('Nombre: ')
		Apellido = input('Apellido: ')
		Cedula = int(input('Cedula: '))
		Password=cadena_aleatoria()
		print("Al presentar el examen el aspirante ingresara con su cedula y password: ",Password)               
		input("\n\nPresionar enter para registrar al aspirante:")
		registrar_estudiante(Nombre,Apellido,Cedula,Password)
	elif sel=='2':
		sp.call('clear',shell=True)
		mostrar_datos()
		input("\n\nPresionar enter para regresar:")
	elif sel=='3':
		sp.call('clear',shell=True)
		Cedula = int(input('Ingresar Cedula: '))
		mostrar_datos_por_cedula(Cedula)
		input("\n\nPresionar enter para regresar:")
	elif sel=='4':
		sp.call('clear',shell=True)
		Cedula = int(input('Ingresar Cedula: '))
		mostrar_datos_por_cedula(Cedula)
		borrar_estudiante(Cedula)
		input("\n\nLos Datos han sido norrados \nPresionar enter para regresar:")
	else:
		return 0;
	return 1;


while(seleccionar()):
   pass
