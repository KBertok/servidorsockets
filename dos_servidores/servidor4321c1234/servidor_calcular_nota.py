from servidor_preguntas import preguntas
from servidor_configuracion import *

def calcular_nota(resp): #resp es un dicionario {preg:resp, preg:resp, preg:resp} enviado por cliente
  acertadas=0
  nro_preguntas=len(resp)
  #nro_preguntas=NUMERO_PREGUNTAS_ESCOGER  
  for preg  in resp:
     if resp[preg]==preguntas[preg][5]:
        acertadas +=1
  return "Tiene " +  str(acertadas) + " de "+ str(nro_preguntas) + " preguntas acertadas"
 
if __name__=="__main__":
   print(calcular_nota({1:2, 2:2, 5:3, 6:1, 9:2, 3:1}))
  
   
