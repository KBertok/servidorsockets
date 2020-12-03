import re

def ingresar_cedula_password():
   #cedula=input("Ingrese su cedula:> ") 

   while True:
      cedula=input("Introduzca cedula (solo numeros) >")
      cedula=re.sub(r"\s+", "", cedula)
      print(cedula)
      if cedula.isdigit():
         break
      else:
         pass

   password=input("Ingrese clave :> ") 
   credencial=[]
   credencial.append(cedula)
   credencial.append(password)
   return credencial

if __name__=="__main__":
   print(ingresar_cedula_password())
   
