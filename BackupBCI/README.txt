######################################################################################## 
########################################################################################
## PROYECTO : LEVANTAMIENTO GESTOR DE CAMPANAS TERADATA
## ------------------------------------------------------------------------------------------------------------------
## Extracción de lógica de levantamiento de vistas SQL
## ------------------------------------------------------------------------------------------------------------------
##  VERSION  DESARROLLADOR        FECHA             DESCRIPCION
## ------------------------------------------------------------------------------------------------------------------
##  1.0      Adriana Jiménez    30-01-2020          Versión Inicial
## ------------------------------------------------------------------------------------------------------------------
######################################################################################## 
########################################################################################


**************************************************************
***************   LIBRERIAS PYTHON A INSTALAR *****************

1. pandas 
2. sql_metadata 
3. giraffez
4. sqlparse



***************************************************************
***************   ARCHIVO A EJECUTAR **************************


>> Jupyter Notebook = LAC_Codigo.ipynb



***************************************************************
***************   RESULTADO DE LA EJECUCION  ******************

Archivo "archivos_no_procesados.txt" : Indica archivos que no se hayan procesado por diversos motivos:
Errores, procesos que no tienen tablas como input, procesos que hacen llamadas a ejecutables, etc

Archivo LAC_Levantamiento_Bteq.csv
Archivo LAC_Levantamiento_StoredProcedures.csv
Archivo LAC_Levantamiento_Vistas.csv
Archivo LAC_Levantamiento_CIM.csv
Archivo LAC_Levantamiento_Resumen.csv



***************************************************************
***************   INSERCIÓN A TABLAS DE TERADATA  *************


Archivo LAC_Levantamiento_Bteq.csv              --->   EDW_TEMPUSU.LAC_LEVANTAMIENTO_TABLAS_BTEQ
Archivo LAC_Levantamiento_StoredProcedures.csv  --->   EDW_TEMPUSU.LAC_LEVANTAMIENTO_TABLAS_SP
Archivo LAC_Levantamiento_Vistas.csv            --->   EDW_TEMPUSU.LAC_LEVANTAMIENTO_TABLAS_VISTAS
Archivo LAC_Levantamiento_CIM.csv               --->   EDW_TEMPUSU.LAC_LEVANTAMIENTO_TABLAS_CIM
Archivo LAC_Levantamiento_Resumen.csv           --->   EDW_TEMPUSU.LAC_LEVANTAMIENTO_TABLAS_RESUMEN



******************************************************************
*************  EXPLICACIÓN DE LA EJECUCIÓN POR PASOS *************


1.
2.
3.
4.
5.
6.

















