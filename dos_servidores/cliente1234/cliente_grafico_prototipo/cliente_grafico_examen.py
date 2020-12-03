import tkinter as tk
from tkinter import ttk
from cliente_preguntas import preguntas 
from cliente_configuracion import *
from muestra_aleatoria import muestra_aleatoria
import time
from tkinter import messagebox




def hora_actual():
    localtime = time.strftime("%H:%M:%S")
    lbl2['text'] = localtime
    # Se ejecuta cada segundo 1000ms (1s)
    elframe.after(1000, hora_actual)

def contador_regresivo(hora=HORAS, min=MINUTOS, sec=SEGUNDOS):
   c=':'
   while hora > -1:
       while min > -1:
           while sec > 0:
               sec=sec-1
               time.sleep(1)
               sec1 = ('%02.f' % sec)  # format
               min1 = ('%02.f' % min)
               hora1 = ('%02.f' % hora)
               #sys.stdout.write('\r' + str(hora1) + c + str(min1) + c + str(sec1))
               #print('\r' + str(hora1) + c + str(min1) + c + str(sec1))
               #lbl4.configure(text='\r' + str(hora1) + c + str(min1) + c + str(sec1))
               texto= str(hora1) + c + str(min1) + c + str(sec1)
               lbl4['text']= str(hora1) + c + str(min1) + c + str(sec1)
               lbl4.update()
               if hora1=='00' and min1=='00' and sec1=='00':
                  procesar()  
                  messagebox.showinfo(message="Examen finalizado", title="Fin del Examen")
           min=min-1
           sec=60
       hora=hora-1
       min=59





def procesar():
   #for  v in vi: 
   #print("El valor de las respuestas es: ",v.get())
   r={}
   indice=0
   for p in l: 
     r[p]=vi[indice].get()
     indice += 1 
   print(r) 
    
   t=0
   for e in r:
      if r[e]==preguntas[e][5]:
         t += 1
    
   msg="Numero total de respuestas correctas: "+ str(t) + "/" + str(NUMERO_PREGUNTAS_ESCOGER)  
   print(msg) 
   messagebox.showinfo(message=msg, title="Resultados")
   ventana.destroy() 
        




def center(win):  #Procedimiento para centrar la ventana
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (width // 2)-400
    y = (win.winfo_screenheight() // 2) - (height // 2)-350
    width=900
    height=900
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))

ventana=tk.Tk()
center(ventana)
ventana.resizable(0,0) # No debe permitir redimensionamiento de la ventana
ventana.title("Examen de Admision")
scrollbar=tk.Scrollbar(ventana)



canvas=tk.Canvas(ventana,yscrollcommand=scrollbar.set)
scrollbar.config(command=canvas.yview)
scrollbar.pack(side=tk.RIGHT,fill=tk.Y)

elframe=tk.Frame(canvas)
canvas.pack(side="left",fill="both",expand=True, padx=20, pady=20)
canvas.create_window(0,0,window=elframe,anchor='nw')

 
font = ('Times New Roman', 15)

lbl1 = tk.Label(elframe, font=font, fg='blue')
lbl2 = tk.Label(elframe, font=font, fg='blue')
lbl3 = tk.Label(elframe, font=font, fg='blue')
lbl4 = tk.Label(elframe, font=font, fg='blue')

lbl1.configure(text='Hora actual: ')
lbl2.configure(text='13:56:47')
lbl3.configure(text='Tiempo restante: ')
lbl4.configure(text='00:27:35')

lbl1.pack()
lbl2.pack()
lbl3.pack()
lbl4.pack()




l=muestra_aleatoria() #Lista de numeros de  preguntas generados aleatoriamente
vi=[] #Lista de variables enteras de Tkinter por cada pregunta, generada dinamicamente para cada grupo de radiobutton
indice=0
for p in l:    
   text=str(indice+1)+') '
   tk.Label(elframe, wraplength=500, text=text+preguntas[p][0]).pack(padx=20,pady=10,anchor=tk.E)
   vi.append(tk.IntVar())
   ttk.Radiobutton(elframe, text=preguntas[p][1], variable=vi[indice], value=1).pack(padx=20,anchor=tk.W)
   ttk.Radiobutton(elframe, text=preguntas[p][2], variable=vi[indice], value=2).pack(padx=20,anchor=tk.W)
   ttk.Radiobutton(elframe, text=preguntas[p][3], variable=vi[indice], value=3).pack(padx=20,anchor=tk.W)
   ttk.Radiobutton(elframe, text=preguntas[p][4], variable=vi[indice], value=4).pack(padx=20,anchor=tk.W)
   indice +=1




boton_enviar=tk.Button(canvas,text="Enviar Respuestas", command=procesar)
boton_enviar.pack()


hora_actual()                              #Ejecutarlo como un thread
contador_regresivo(HORAS,MINUTOS,SEGUNDOS)

ventana.mainloop()
