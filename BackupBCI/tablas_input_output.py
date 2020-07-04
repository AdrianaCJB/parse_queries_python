import re
import os
import pandas as pd

#EL SCRIPT BUSCA DENTRO DEL CODIGO NO COMENTADO DEL PROCESO LAS TABLAS INPUT Y OUTPUT.

#CONCEPTO TABLA INPUT: TODAS AQUELLAS TABLAS QUE NO SE CREAN EN EL PROCESO, PERO QUE SE LLAMAN EN ALGUN FROM O JOIN

#CONCEPTO TABLA OUTPUT: TODAS AQUELLAS TABLAS QUE SE CREAN EN EL PROCESO PERO NO SE ELIMINAN EN ESTE, (OJO: INCLUYE TABLAS TEMPUSU SI ESTAS NO SE BORRAN EN EL PROCESO)

#CONCEPTO TABLA TEMPORAL: TODAS AQUELLAS TABLAS QUE SE CREAN Y SE BORRAN EN EL PROCESO

fileName = input("Escribe el nombre del proceso: ")
while not os.path.exists(fileName):
  fileName = input("No se encontró el proceso, escriba el nombre del proceso: ")

estadoTabla = None
estadoTablaInput = None
tablas =[]
tablasInput = []
tablasInputPrevia = []
tablasInputPrevia2 = []
tablasOutput = [] 
tablasTemporales = []
txtArchivo = ''
listaTxtArchivo = []
txtArchivoFinal = ''
nombreProceso = []

#Estructura que va a tener el dataframe
estructura = {'Nombre Proceso':[],'Tablas Input':[],'Tablas Output':[]}


#SE RECORRE EL ARCHIVO Y SE EXTRAE CODIGO NO COMENTADO

archivo = open(fileName,'r')
txtArchivo = archivo.read()
archivo.close()
nombreProceso.append(fileName)
#SE EXTRAE CODIGO SIN COMENTARIOS DE NINGUN TIPO
listaTxtArchivo = re.split('\-\-.*?\n|\/\*.*?\*\/', txtArchivo,flags = re.M|re.U|re.S)

#SE FORMATEA CONTENIDO EXTRAIDO DEL ARCHIVO
for linea in listaTxtArchivo:
  txtArchivoFinal = txtArchivoFinal+linea

#SE APLICA FUNCION PARA DEJAR EL CONTENIDO DEL ARCHIVO EN MINUSCULA.
txtArchivoFinal = txtArchivoFinal.lower()

#SE RECORRE CADA LINEA PARA GUARDAR LAS TABLAS QUE ENCUENTRE EN ELLA
tablas = re.findall("[(table)(join)(drop)(from)]{4,}[ ]{1,}([A-Z-a-z\_]{2,}[\.][A-Z-a-z\_\d]{1,})", txtArchivoFinal, flags = re.M|re.U|re.S|re.I)

#SE ELIMINAN DUPLICADOS
tablas = list(set(tablas))

#SE EVALUA EL ESTADO DE LA TABLA PARA CADA PROCESO PARA OBTENER LAS TABLAS OUTPUT
#YA TENIENDO CADA TABLA EN (tablas) CADA UNA DE ESTA RECORRE EL CONTENIDO DEL ARCHIVO
#BUSCANDO SI PASAN POR UN CREATE TABLE O UN DROP TABLE
#SI PASAN POR UN CREATE TABLE Y LUEGO DE ELLO NO SIGUE UN DROP TABLE SE CONSIDERA COMO TABLA OUTPUT
#DE LO CONTRARIO SE CONSIDERARA COMO TABLA TEMPORAL YA QUE SE CREA Y SE ELIMINA EN EL PROCESO
texto4 = txtArchivoFinal.split('\n') 

for linea in tablas:
  drop = "drop table[ ]*? "+ linea + "\s*?\;$"
  create = "create table[ ]*? "+ linea

  for items in texto4:
    if re.search(drop,items):      
      estadoTabla = False
    elif re.search(create,items):
      estadoTabla = True

  if estadoTabla == True:
    tablasOutput.append(linea)
    estadoTabla = None
  elif estadoTabla == False:
    tablasTemporales.append(linea)
    estadoTabla = None

#HASTA ESTE PUNTO TENEMOS 3 LISTAS CON INFORMACION IMPORTANTE 
#tablas: QUE CONTIENE TODO EL LISTADO DE TABLAS ENCONTRADAS EN EL ARCHIVO
#tablasOutput:  CONTIENE TODAS LAS TABLAS QUE SE CREAN Y NO SE BORRAN
#tablasTemporales: CONTIENE TODAS LAS TABLAS QUE SE CREAN Y SE BORRAN EN EL PROCESO.

#PARA OBTENER LAS TABLAS INPUT PODEMOS DECIR QUE SON LAS TABLAS QUE SOBRAN DEL LISTADO DE TODAS LAS TABLAS
#SACANDO LAS TABLAS OUTPUT Y LAS TABLAS TEMPORALES (QUE YA LAS TENEMOS EN tablasOutput y tablasTemporales)


#SACAMOS DE tablas TODAS LAS TABLAS OUTPUT Y TABLAS TEMPORALES
tablasInputPrevia = [x for x in tablas if x not in tablasOutput]
tablasInputPrevia2 = [x for x in tablasInputPrevia if x not in tablasTemporales]

#OBTENEMOS TABLAS INPUT EVALUANDO SOLO AQUELLAS A LAS QUE SE LAS LLAMA MEDIANTE "FROM" O "JOIN"

for linea in tablasInputPrevia2:
  fromInput = "from\s*?"+ linea
  joinInput = "join\s*?"+ linea

  for items in texto4:
    if re.search(fromInput,items):      
      estadoTablaInput = True
      #print(linea +" "+ str(estadoTabla)) 
    elif re.search(joinInput,items):
      estadoTablaInput = True
      #print(linea +" "+  str(estadoTabla))

  if estadoTablaInput == True:
    tablasInput.append(linea)
    estadoTablaInput = None

#SE DETERMINA EL LARGO MAYOR ENTRE  LAS SIGUENTES LISTAS:
#NOMBRE PROCESO, LISTA DE NOMBRE DE BASES DE DATOS DE CODIGO NO COMENTADO (listaCodigoFinal) Y LISTA DE NOMBRES DE BASES DE DATOS
#DE CODIGO COMENTADO (listaBdComentadas)

#SE DETEMRINA CUAL TIENE EL LA LONGITUD DE SU LISTA MAS LARGA DEBIDO A QUE TODAS ESAS 3 COLUMNAS TIENEN QUE TENER EL MISMO LARGO
#A MODO DE PODER ARMAR EL DATAFRAME, POR ESTA RAZON A LAS LISTAS CON MENOR LONGITUD SE VAN A RELLENAR CON ESPACIOS VACIOS PARA
#PODER IGUALAR LA LONGITU DE LA LISTA DE MAYOR LONGITUD

#SE DETERMINAN EL LARGO DE CADA LISTA

lenProceso = len(nombreProceso)
lenTablasInput = len(tablasInput)
lenTablasOutput = len(tablasOutput)

#SE ORDENA EN UNA TUPLA PARA QUE EL DE MAYOR LONGITUD SE PONGA DE PRIMERO
lenList = [lenProceso,lenTablasInput,lenTablasOutput]
lenList.sort(reverse=True)
lenMayor = lenList[0]

#SE RESTA EL MAYOR CONTRA LAS DEMAS LISTAS PARA SABER LA DIFERENCIA A RELLENAR DE ESPACIOS EN BLANCO
lenProceso1 = lenMayor - lenProceso
lenTablasInput1 = lenMayor - lenTablasInput
lenTablasOutput1 = lenMayor - lenTablasOutput
      
#SE RELLENAN ESPACIOS EN BLANCO                    
for i in range (0,lenProceso1):
  nombreProceso.append(fileName)

for i in range(0,lenTablasInput1):
  tablasInput.append('')

for i in range(0,lenTablasOutput1):
  tablasOutput.append('')  

#SE INSERTAN ELEMENTOS DE LAS LISTAS A LA ESTRUCTURA DEFINIDA EN LAS VARIABLES DE AMBIENTE (DATAFRAME)
for elemento in nombreProceso:
  estructura['Nombre Proceso'].append(elemento)
for elemento in tablasInput:
  estructura['Tablas Input'].append(elemento)
for elemento in tablasOutput:
  estructura['Tablas Output'].append(elemento)

tablasOutput.sort()

pd.set_option('colheader_justify', 'left')
df = pd.DataFrame(estructura)

#SALIDA
print(df)
fin = input("")