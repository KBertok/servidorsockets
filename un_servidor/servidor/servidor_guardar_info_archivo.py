from datetime import datetime
from pickle import dump,load

def guardar_info_archivo(cedula,respuestas):
   archivo=cedula
   fechayhora=datetime.now()
   lista=[]
   lista.append(cedula)
   lista.append(fechayhora)
   lista.append(respuestas)
   fdw=open(archivo, 'wb')
   dump(lista,fdw)
   fdw.close()


def recuperar_info_archivo(cedula):
   archivo=cedula
   fdr=open(archivo,'rb')
   lista=load(fdr)
   fdr.close() 
   print(lista)

   
if __name__=="__main__":
   #guardar_info_archivo('10123456',{1:2,2:2,3:1,4:2})
   #recuperar_info_archivo('9888777') 
   recuperar_info_archivo('12345888') 
   recuperar_info_archivo('29111222') 
