from random import sample
from servidor_configuracion import *

def preguntas_aleatorias(): # Retorna lista con munero  de preguntas a contestar
   """ 
   genera una lista de numeros aleatorios correspondientes a las preguntas 
   a resolver
   """
   l=list(range(1,NUMERO_PREGUNTAS_TOTALES + 1))
   s=sample(l,NUMERO_PREGUNTAS_ESCOGER)
   if ALEATORIO_DESORDENADO == False:
      s.sort()
   return s

if __name__=="__main__":
   print(preguntas_aleatorias())
