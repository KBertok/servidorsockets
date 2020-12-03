from random import sample
from cliente_configuracion import *

def muestra_aleatoria():
   """ 
   genera una lista de numeros aleatorios correspondientes a las preguntas 
   a resolver
   """
   l=list(range(1,NUMERO_PREGUNTAS_TOTALES + 1))
   s=sample(l,NUMERO_PREGUNTAS_ESCOGER)
   #s.sort()
   return s

if __name__=="__main__":
   print(muestra_aleatoria())
