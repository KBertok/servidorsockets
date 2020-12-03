
def ingresar_cedula_password():
   cedula=input("Ingrese su cedula:> ") 
   password=input("Ingrese clave :> ") 
   credencial=[]
   credencial.append(cedula)
   credencial.append(password)
   return credencial

if __name__=="__main__":
   print(ingresar_cedula_password())
   
