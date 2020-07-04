import os.path

#SCRIPT QUE INDICA LA CANTIDAD DE LINEAS QUE TIENE UN PROCESO

counter = 1 #VARIABLE QUE ACTUA COMO CONTADOR DE LAS LINEAS DEL ARCHIVO

#PIDE EL NOMBRE DEL ARCHIVO, SI LO ENCUENTRA PROCEDE A CONTAR CUANTAS LINEAS TIENE EL PROCESO
#SI NO LO ENCUENTRA VUELVE A PEDIR OTRO NOMBRE DE ARCHIVO
fileName = input("Escribe el nombre del archivo: ")
while not os.path.exists(fileName):
  fileName = input("No se encontro el archivo. Por favor escriba el nombre del archivo nuevamente: ")

archivo = open(fileName,'r')
for lines in archivo.readlines():
  counter = counter +1
archivo.close()

print("El script "+ fileName + " tiene "+str(counter)+" linea(s)")