import os 
import re
	
filename = input("Escribe el nombre del archivo: ")
while not os.path.exists(filename):
  filename = input("No se encontro el archivo, Por favor escribe el nombre del archivo nuevamente: ")
if os.path.exists(filename):
  archivo = open(filename)
  textoArchivo = archivo.read()
  
  querys = re.findall(r'\((.*?)\)',textoArchivo)
  print(querys)

