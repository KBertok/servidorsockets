from pickle import loads, dumps   #para enviar objetos como listas o diccionarios

def enviar_dato_bin(d):
   obj=dumps(d)
   return obj

def recibir_bin_dato(obj):
   d=loads(obj)
   return d


def enviar_mensaje(conn,mensaje):
      conn.send(bytes(mensaje,"utf-8"))



def enviar_objeto(conn,objeto):
    objeto=enviar_dato_bin(objeto)
    conn.send(objeto)


def recibir_mensaje(conn):
    msg=conn.recv(2048).decode('utf-8')
    return msg


def recibir_objeto(conn):
    objeto=conn.recv(2048)
    d=recibir_bin_dato(objeto)
    return d

