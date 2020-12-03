from random import sample
from servidor_configuracion import *

def cadena_aleatoria():
  if PASSWORD_SOLO_CON_LETRAS:
     cadena=sample(ALFABETO,LONGITUD_PASSWORD)
  else:
     cadena=sample(ALFABETO_OPCIONAL,LONGITUD_PASSWORD)
  string=''
  for c in cadena:
     string +=c 
  return string

if __name__=="__main__":
   print(cadena_aleatoria())

