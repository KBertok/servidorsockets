from datetime import datetime

def fechas_horario_permitido():
   """
   Funcion:     fechas_horario_permitido
   descripcion: determina si la fecha y hora actual estan
                en las fechas y horario permitidos
   Primero se determina si la fecha esta comprendida
   en el rango permitido, si no es asi retorna False 
   en ese instante, si esta en el rango permitido, chequea el horario
   la hora actual es comparada con el rango de horario permitido
   Dado que cada maquina tiene funciones de tiempo definidas
   de manera distinta por ejemplo y  la hora y fecha pueden estar desconfiguradas
   se deja comentada la funcion  para su adaptacion en el ambiente 
   donde se vaya a ejecutar, la funcion ha sido probada en dos ambientes, definir aqui 
   """

   fecha_hoy=datetime.now().date().strftime('%Y-%m-%d')


   fecha_dada1=datetime(2018,9,1)        #Definir aqui la fecha inicial, mes y dia sin ceros por delante  
   fecha_inicial=fecha_dada1.strftime('%Y-%m-%d')

   
   fecha_dada2=datetime(2019,10,1)        #Definir aqui la fecha final, mes y dia colocar 9 no 09
   fecha_final=fecha_dada2.strftime('%Y-%m-%d')

   if fecha_hoy < fecha_final:
      if fecha_inicial < fecha_hoy:
         #print("Fecha Si")
         pass                        # Fecha OK pero falta chequear horario mas abajo por eso: pass
      else:
         #print("Fecha No")
         return False               # Ya no se chequea horario puesto que fecha no esta en rango 
   else:
     #print("Fecha No") 
     return False                 # igual que anterior 


   hora_inicial = datetime.strptime("07:00:00", "%X").time() #Hora inicial, definir aqui
   hora_final = datetime.strptime("12:45:00", "%X").time()   #Hora final, definir aqui  
   hora_actual = datetime.now().time()

   if hora_actual < hora_final:
      if hora_inicial < hora_actual:
         #print("Hora Si")
         return True
      else:
         #print("Hora No")
         return False 
   else:
     #print("Hora No")         
     return False 
  

    
if __name__=="__main__":
   if fechas_horario_permitido():
      print("Ok")
   else:
       print("No Ok") 

