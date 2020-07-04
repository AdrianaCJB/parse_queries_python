import re
import os.path
import pandas as pd

#SETEO DE VARIABLES
textoArchivo = ''
textoComentarios= ''
textoComentarioLimpio= ''
txtCodigo = ''
txtCodigoLimpio = ''
listaCodigo = []
listaCodigoFinal = []
listaBdComentarios = []
listaBdComentarios2 = []
listaBdComentadas = []
listaBdCodigo = []
nombreProceso = ''
proceso = []

#Estructura que va a tener el dataframe
estructura = {'Nombre Proceso':[],'BD No Comentadas':[],'BD Comentadas':[]}

#nombres de bases de datos que va a buscar en el proceso, se definieron en duro porque muchas veces detecta texto
#con el mismo patron que el que tiene una base de datos.
nombreBD = ['bcimkt','campanas_pyme','edc_journey_vw','edc_mdd_vw','edc_suc_vw','edm_dmempresa_vw','edm_dminvers_vw','edw_dmanalic_vw','edw_dmtarjeta_vw','edw_semlay_vw','edw_tempusu','edw_vw','mkt_crm_analytics_tb','mkt_explorer_tb','mkt_journey_tb','sys_calendar']

#SE RECORRE CARDA ARCHIVO DEL DIRECTORIO ESPECIFICADO

filename = input("Escribe el nombre del archivo: ")
while not os.path.exists(filename):
  filename = input("No se encontro el archivo, Por favor escribe el nombre del archivo nuevamente: ")
if os.path.exists(filename):
  archivo = open(filename)
  textoArchivo = archivo.read()
  
  #SE GUARDA EN textoComentarios TEXTO LEIDO QUE SOLO CONTENGA COMENTARIOS
  textoComentarios = re.findall("\-\-(.*?)\n|\/\*(.*?)\*\/", textoArchivo, flags = re.M|re.U|re.S)
  
  #SE GUARDA EN LISTACODIGO TROZOS DE CODIGO QUE NO CONTENGAN COMENTARIOS  
  listaCodigo = re.split('\-\-.*?\n|\/\*.*?\*\/', textoArchivo,flags = re.M|re.U|re.S)
  
  #SE GUARDA EL NOMBRE DEL PROCESO  
  nombreProceso = filename

  archivo.close()

  #BLOQUE PARA EXTRAER TODAS LAS BASES+TABLAS EJ:(BASEDEDATOS.TABLA1) EN LOS COMENTARIOS
  
  #RECORREMOS CADA PALABRA EN textoComentarios Y CONCATENAMOS SU CONTENIDO EN UNA NUEVA VARIABLE
  #YA QUE LA FUNCION re.findall DEJA EL CODIGO EN UN FORMATO QUE NO NOS INTERESA.
  
  for elemento in textoComentarios:
    textoComentarioLimpio = textoComentarioLimpio + ''.join(elemento)

  #COLOCAMOS TODO EL CONTENIDO EN MINISCULAS.
  textoComentarioLimpio  = textoComentarioLimpio.lower()
  
  #DE LA VARIABLE textoComentarioLimpio LA CONVERTIMOS EN UNA LISTA PARA ELLO LE APLICAMOS LA FUNCION SPLIT
  #PARA QUE CADA ELEMENTO DE LA LISTA SEA CADA PALABRA SEPARADA POR UN ESPACIO
  
  listaBdComentarios = textoComentarioLimpio.split()

 #BUSCAMOS EN LA LISTA QUE ACABAMOS DE CREAR SI CONTIENE ALGUNA DE LOS NOMBRES DE LAS BASES DE DATOS DEFNIDAS EN LA VARIABLE nombreBD
 #ESTA LISTA QUEDARA ALMACENADA EN LA VARIABLE TIPO LISTA  listaComentarioLimpio2
  for linea in listaBdComentarios:
    for db in nombreBD:
      if db in linea:
        limpiaComent = re.findall("([A-Z-a-z\_]{2,}[\.][A-Z-a-z\_\d]{1,})", linea)
        listaBdComentarios2.append(limpiaComent[0]) 
        
  #ELIMINAMOS DUPLICADOS
  listaBdComentarios2 = list(set(listaBdComentarios2)) 
  
  
  #HASTA ESTE PUNTO YA TENEMOS TODOS LOS NOMBRES DE LAS BASES DE DATOS QUE APARECEN EN EL CODIGO COMENTADO DEL ARCHIVO.
  #AHORA HAY QUE REPETIR EL PROCESO PARA EL CODIGO NO COMENTADO DEL ARCHIVO.
   

  #CONVERTIMOS EL TEXTO DEL ARCHIVO QUE CONTIENE SOLO CODIGO(NO COMENTADO) PARA LIMPIAR EL FORMATO EN EL QUE NOS LO TRAEMOS
  #LO GUARDAMOS EN UNA VARIABLE DE TIPO STRING Y LO PASAMOS A MINUSCULAS.
  for ele in listaCodigo:
    txtCodigo = txtCodigo + ele.lower()

  #FORMATEAMOS LA VARIABLE txtCodigo Y LA GUARDAMOS EN txtCodigoLimpio
  txtCodigoLimpio= txtCodigo.split()    


  #BUSCAMOS EN txtCodigoLimpio SI CONTIENE ALGUNA DE LOS NOMBRES DE LAS BASES DE DATOS DEFNIDAS EN LA VARIABLE nombreBD
  #ESTA LISTA QUEDARA ALMACENADA EN LA VARIABLE TIPO LISTA
  for linea in txtCodigoLimpio:
    for db in nombreBD:
      if db in linea:
        base = re.findall("([A-Z-a-z\_]{2,}[\.][A-Z-a-z\_\d]{1,})", linea)
        listaCodigoFinal.append(base[0]) 

  #ELIMINAMOS DUPLICADOS
  listaCodigoFinal = list(set(listaCodigoFinal))

  #ELIMINAMOS TODAS LOS NOMBRES DE TABLAS DE LAS ENCONTRADAS Y NOS QUEDAMOS SOLO CON LOS NOMBRES DE LA BASE DE DATOS
  listaBdCodigo = [x.split('.')[0] for x in listaCodigoFinal]
  #ELIMINAMOS DUPLICADOS
  listaBdCodigo = list(set(listaBdCodigo))
  
  #ELIMINAMOS TODAS LOS NOMBRES DE TABLAS DE LAS ENCONTRADAS Y NOS QUEDAMOS SOLO CON LOS NOMBRES DE LA BASE DE DATOS
  listaBdComentadas = [x.split('.')[0] for x in listaBdComentarios2]
  
  #ELIMINAMOS DUPLICADOS
  listaBdComentadas = list(set(listaBdComentadas))

  #BLOQUE PARA ARMAR ESTRUCTURA DE DATAFRAME


  #SE DETERMINA EL LARGO MAYOR ENTRE  LAS SIGUENTES LISTAS:
  #NOMBRE PROCESO, LISTA DE NOMBRE DE BASES DE DATOS DE CODIGO NO COMENTADO (listaCodigoFinal) Y LISTA DE NOMBRES DE BASES DE DATOS
  #DE CODIGO COMENTADO (listaBdComentadas)
  
  #SE DETEMRINA CUAL TIENE EL LA LONGITUD DE SU LISTA MAS LARGA DEBIDO A QUE TODAS ESAS 3 COLUMNAS TIENEN QUE TENER EL MISMO LARGO
  #A MODO DE PODER ARMAR EL DATAFRAME, POR ESTA RAZON A LAS LISTAS CON MENOR LONGITUD SE VAN A RELLENAR CON ESPACIOS VACIOS PARA
  #PODER IGUALAR LA LONGITU DE LA LISTA DE MAYOR LONGITUD
  
  #SE DETERMINAN EL LARGO DE CADA LISTA
  lenProceso = len(proceso)
  lenCodigo = len(listaBdCodigo)
  lenComentario = len(listaBdComentadas)
  
  #SE ORDENA EN UNA TUPLA PARA QUE EL DE MAYOR LONGITUD SE PONGA DE PRIMERO
  lenList = [lenProceso,lenCodigo,lenComentario]
  lenList.sort(reverse=True)
  lenMayor = lenList[0]
  
  #SE RESTA EL MAYOR CONTRA LAS DEMAS LISTAS PARA SABER LA DIFERENCIA A RELLENAR DE ESPACIOS EN BLANCO
  lenProceso1 = lenMayor - lenProceso
  lenCodigo2 = lenMayor - lenCodigo
  lenComentario2 = lenMayor - lenComentario
        
  #SE RELLENAN ESPACIOS EN BLANCO                    
  for i in range (0,lenProceso1):
    proceso.append(nombreProceso)

  for i in range(0,lenCodigo2):
    listaBdCodigo.append('')

  for i in range(0,lenComentario2):
    listaBdComentadas.append('')  

  #SE INSERTAN ELEMENTOS DE LAS LISTAS A LA ESTRUCTURA DEFINIDA EN LAS VARIABLES DE AMBIENTE (DATAFRAME)
  for elemento in proceso:
    estructura['Nombre Proceso'].append(elemento)
  for elemento in listaBdCodigo:
    estructura['BD No Comentadas'].append(elemento)
  for elemento in listaBdComentadas:
    estructura['BD Comentadas'].append(elemento)
else:
  print("No se encontro el proceso")
    
#BLOQUE PARA VOLVER A INICIALIZAR LAS VARIABLES AUXILIARES
textoArchivo = ''
textoComentarios= ''
textoComentarioLimpio= ''
txtCodigo = ''
txtCodigoLimpio = ''
listaCodigo = []
listaCodigoFinal = []
listaBdComentarios = []
listaBdComentarios2 = []
proceso = []
listaBdComentadas = []
listaBdCodigo = []

df = pd.DataFrame(estructura)
print(df)

fin = input("")