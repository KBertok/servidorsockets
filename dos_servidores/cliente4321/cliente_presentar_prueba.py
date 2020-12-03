#from cliente_preguntas import preguntas
from cliente_configuracion import *
import time 
import sys
from threading import Thread
import subprocess as sp

hora1=''
min1=''
sec1=''

def contador_regresivo():
   hora=HORAS
   min=MINUTOS
   sec=SEGUNDOS   
   global hora1,min1,sec1
   c=':'
   while hora > -1:
       while min > -1:
           while sec > 0:
               sec=sec-1
               time.sleep(1)
               sec1 = ('%02.f' % sec)  # format
               min1 = ('%02.f' % min)
               hora1 = ('%02.f' % hora)
               sys.stdout.write('\r' + str(hora1) + c + str(min1) + c + str(sec1)+ "-- 1,2,3,4 o s para salir>>")
               #print('\r' + str(hora1) + c + str(min1) + c + str(sec1))
               #lbl4.configure(text='\r' + str(hora1) + c + str(min1) + c + str(sec1))
               #texto= str(hora1) + c + str(min1) + c + str(sec1)
               #lbl4['text']= str(hora1) + c + str(min1) + c + str(sec1)
               #lbl4.update()
               #if hora1=='00' and min1=='00' and sec1=='00':
               #   procesar()
               #   messagebox.showinfo(message="Examen finalizado", title="Fin del Examen")
           min=min-1
           sec=60
       hora=hora-1
       min=59


def presentar_prueba(preguntas):
    global hora1,min1,sec1
    Thread(target = contador_regresivo).start()
    d={}
    #contador_regresivo(HORAS, MINUTOS, SEGUNDOS)
    for p in preguntas:
       d[p[0]]=0
    print(d)
    nro=1
    for p in preguntas:
        if (hora1=='00' and min1=='00' and sec1=='00'):
           print(d)
           break
        sp.call('clear',shell=True) 
        print(nro,'.)',p[1])
        print("1.)",p[2])
        print("2.)",p[3])
        print("3.)",p[4])
        print("4.)",p[5])
        #entrada=input("-- 1,2,3,4 o s para salir>")        
        entrada=input()
        while entrada not in ['1','2','3','4','s']:
           #entrada=input("-- 1,2,3,4 o s para salir>") 
           entrada=input()
        if entrada=='s':
           print(d)
           break
        d[p[0]]=int(entrada)
        nro += 1
        print(d)
    return d

if __name__=='__main__': #Testing ....
 p=[(10, 'La capital de España es', 'Caracas', 'Bogota', 'Madrid ', 'Peru'),
 (3, 'Cual es la capital de Brasil', 'Caracas', 'Bogota', 'Lima ', 'Brasilia'),
 (23, 'Sea P(X) = X³-X² + X-1. El calculo de P(-1)es igual a:', '-2', '-4', '3', '5'),
 (24, 'La ecuacion X² + X - 12 = 0 tiene como soluciones:', 'X₁=3 ; X₂=-4', 'X₁=1 ; X₂=-2', 'X₁=2 ; X₂=3', 'X₁=3 ; X₂=-1'),
 (30, 'Al efectuar (-2, 0] ∩ [0, 3], obtenemos:', '[0]', '(-2,3]', '{-2,3}', '{0}'),
 (27, 'Al resolver el sistema de ecuaciones X - Y + 1 = 0 y X + Y + 1 = 0 obtenemos:', 'X₁=1 ; X₂=-1', 'X₁=0 ; X₂=2', 'X₁=0 ; X₂=1', 'X₁=-1 ; X₂=3'),
 (19, 'La constitucion de mas larga vigencia en la historia de Venezuela es la de:', '1961', '1811', '1931', '1830'),
 (7, 'Cuantos lados tiene un pentagono', 'Seis ', 'Tres ', 'Cuatro', 'Cinco'),
 (2, 'Cual es la capital de Colombia', 'Caracas', 'Bogota', 'Lima', 'Rio de Janeiro'),
 (29, 'Si X₁ y X₂ son soluciones de la ecuacion ax² + bx + c  = 0, entonces dicha ecuacion puede factorizarse como:', '(X - X₁)(X + X₂) = 0', 'a(X - X₁)(X + X₂) = 0', 'a(X - X₁)(X - X₂) = 0'    , '(X + X₁)(X + X₂) = 0')]
 presentar_prueba(p)
