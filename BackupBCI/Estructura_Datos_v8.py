# -*- coding: utf-8 -*-
"""
Mapeador Dependencia Procesos

Requisitos:
1) Tener este script en el repositorio donde estan todos los procesos que se desea mapear
2) La estructura de carpetas debe ser PROCESO/SUBPROCESO/TAREA/SCRIPT(.SQL/.PY)

Comentarios:
El algoritmo busca todas las ubicaciones de los archivos .sql y .py en la carpeta que se ubica.
Lee cada script buscando un create table y almacenando las tablas intermedias hasta el cirre con primary key.
Guarda la informacion con el formato de dataframe [Proceso, Subproceso, Tarea, Script, Tabla Creada, Proceso Input, Tablas Input, Ubicacion Input]

IMPORTANTE: En caso de que la estructura de carpetas no sea la descrita es posible que el campo de proceso sea ocupado por la carpeta contenedora del proceso.
Crear carpetas auxiliares con el nombre del proceso en caso de que ocurra esto.
"""

import os
import pandas as pd

### Agregar lista de querys en una carpeta

bteq_files=[]

rootDir = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))  #Encuentra Ubicacion Carpetas


for dirName, subdirList, fileList in os.walk(rootDir):
    for fname in fileList:    
        if ".sql" in (fname+dirName).lower():
                bteq_files.append(os.path.join(dirName,fname))
        #if ".py" in (fname+dirName).lower() and "Estructura_Datos" not in fname+dirName: #corrige que se lea a si mismo
         #       bteq_files.append(os.path.join(dirName, fname))


#Declaracion Carpetas Proceso

Proceso= []
Ubicacion = []
SubProceso = []
Tarea = []
Script = []
Tabla_Creada = []
Tablas_Input = []
Proceso_Input= []
Sub_Proceso_Input= []
Tipo_Dependencia = []
go = False
comentario = False
aux = []
Estructura = [0,0]


###Alimentar lista con todas las bases de dato que usamos en los procesos, actualizar una vez al año o cuando aparezcan nuevos repositorios ultm actualizacion 26/05/17
Lista = ["usr_mkt_common","edw_bcidaily_tb","edm_dmsegto_tb","temp","edw_event_cmp_tb","edw_prospect_tb","edm_dmfinanc_tb","exdduen","armtmi","customer_service","edw_cuadratura_tb","conti","edm_dmactcom_vw","edw_vrisk","edw_event_tb","bci_prd","cthies","prod_tva","sysudtlib","usarmedw","tva_results","sysuif","edw_location_tb","armedw","edw_event_col_tb","edm_dmcto_vw","bciprod","edw_tareasolicitud_vw","mkt_pryser_tb","usrdlake","bo_bci","edw_bciwork_tb","edm_dmjourney_tb","tdqcd","edw_dm_bbee_tb","sys_calendar","locklogshredder","dg_testlab_tb","armout","edw_calidad_vw","edw_dm_bbee_vw","edw_governance_vw","bciwork","tva_views","edw_campaign_tb","edw_event_dav_tb","edm_dmactcom_tb","tva_dyn_sql","edm_dminvers_tb","edw_prospect_vw","edc_journey_vw","armcore","lmenesv","edw_param_and_others_tb","armviews","edm_dmcto_tb","reparacion","edw_bcidatam_tb","tva_balance","edw_onboarding_vw","edw_channel_tb","edm_mis_vw","pguties","usrcdbc","edc_suc_vw","sqlj","ebi_plmtc_vw","jcorti","edm_dmriesg_vw","arminp","mariasp","bciperso","edw_tareasolicitud_tb","edw_epiphany_tb","edw_product_tb","datam","armwork","jcparra","edw_event_tdm_tb","edw_party_asset_tb","edm_coreprspct_vw","edw_event_nova_tb","bci_vu","edw_vu","edm_dmjourney_vw","edw_dmtarjeta_tb","datalake_vw","recuperacion","tva_auth_v","edw_dmanalic_vw","edw_temp","tva_profit","dbc","edm_dminvers_vw","cjaraj","edw_finance_tb","edw_onboarding_tb","console","$netvault_catalog","mkt_journey_tb","edw_dmcbolsa_vw","vgarin","sysadmin","edw_sporadicbuy_tb","edm_tmp_dmr","td_sysfnlib","bcimes","edw_mc","edw_matrix_vw","rsamso","edw_event_trj_tb","bcispec","uanalyci","tva_archive","ahirane","qcd0","edw_event_bel_tb","tdstats","edw_epiphany_vw","edm_tmp_dmfc","edw_sp","exfdber","edw_dmbbp_vw","edw_party_tb","dbcmngr6","edm_coreprspct_tb","edw_cross_subject_areas_tb","ebi_plbyp_vw","edw_bciprod_tb","edc_journey_tb","edw_semlay_vw","ebi_plmtc_tb","edw_tempusu","edm_dmbdr_tb","mkt_explorer_tb","bci_mds","edw_semlab_vw","tdwm","edm_dmcore_vw","tva_amort","edw_event_fil_tb","tva_sor","edw_matrix_tb","edm_dmsegto_vw","sysspatial","edw_dmcbolsa_tb","edm_dmriesg_tb","edm_dmprspct_tb","edw_governance_tb","usrdmmkt","bcimkt","edm_dmnova_vw","cberrio","tva_work","usrgtcmp","ccid","edw_vw_pre_gov","edw_dmtarjeta_vw","bcigestion","edm_dmbdr_vw","edm_dmpyme_vw","cschule","edm_dmpyme_tb","tempusu","edm_mis_tb","tva_archive_v","tva_staging","edm_dmnova_tb","edc_suc_tb","sysbar","dm_control","edm_dmprspct_vw","edm_dmfinanc_vw","systemfe","rfuenzp","dataqual","syslib","demographics","edw_dmbbp_tb","td_sysxml","edm_dmcore_tb","edw_wrk","xx","bciadmin","tva_auth","csanche","edw_calidad_tb","armcust","viewpoint","edw_vw","edw_int_organization_tb","edw_event_ctb_tb","bcidemo_vm","edw_va","edw_agreement_tb","tva_rules","edw_dmriesgo_tb","ebi_plbyp_tb","edw_dmmkt_tb","edw_dmmkt_vw","dm_staging","emerlo","bcidaily","edw_dmriesgo_vw","sysjdbc","edw_estadistica_tb"]
Lista= map(lambda x:x.lower(),Lista) # minusculas
bteq_files = map(lambda x:x.lower(),bteq_files) # minusculas



for paths in bteq_files: #Para cada archivo
    archivo = open(paths, "r")
    print paths
    for linea in archivo.readlines(): #Para cada linea del archivo
        # Reglas de lectura
        linea = linea.lower() # Minusculas
        start = "create" in linea and "table" in linea  # Iniciador de Bloque (Boolean)
        end   = "with" in linea and "data" in linea and "index" in linea  # Finalizador de Bloque (Boolean)
        start_comment = "/*" in linea  # Iniciador de Bloque (Boolean)
        end_comment = "*/" in linea   # Finalizador de Bloque (Boolean)
        start_insert = "insert" in linea  # Iniciador de Bloque (Boolean)
        end_insert = ";" in linea or ");" in linea  # Finalizador de Bloque (Boolean)

        if start_comment: comentario = True
        if end_comment: comentario = False

        if comentario == False: #valida que no sea un campo comentariado lo que esta leyendo
            if start or start_insert:
                go = True
                Estructura[0] = 2


            # Regla para leer estructuras logicas
            if go and Estructura[0] > Estructura[1]:
                   A = []
                   A = linea.split()
                   for x,y in enumerate(Lista):
                       for v,w in enumerate(A):
                                   w = w.replace("(", "").replace(")", "").replace(";", "").lower()  # Parseo
                                   if y in w.split(".") and "--" not in w:
                                       if w not in aux: #Limita los inputs con tablas duplicadas en caso de joins recursivos
                                           Proceso.append(paths.split('\\')[len(rootDir.split('\\'))]) #obliga a tomar el nivel de la carpeta de proceso
                                           SubProceso.append(paths.split('\\')[len(rootDir.split('\\'))+1]) #obliga a tomar el nivel de la carpeta de subproceso
                                           Tarea.append(paths.split('\\')[-2])
                                           Script.append(paths.split('\\')[-1])
                                           aux.append(w)

            if ((end or end_insert) and go and len(aux)>1):
                aux1 = aux[0]
                aux2 = aux[1:]
                for x2 in range(len(aux2)):
                    Tabla_Creada.append(aux1)
                    Ubicacion.append(paths)
                for x2 in range(len(aux2)):
                    Tablas_Input.append(aux2[x2])
                Estructura = [0,0]
                aux=[]
                Proceso.pop()
                SubProceso.pop()
                Tarea.pop()
                Script.pop()
            if end or (end_insert and go):
                go = False
                Estructura[1] = 1


    archivo.close()

#Recursiva para encontrar donde se crea cada tabla e indexado a procesos Base, Intermedios y Dependientes

for j in range (len(Tabla_Creada)):
      if  Tablas_Input[j] in Tabla_Creada:
          Proceso_Input.append(Proceso[Tabla_Creada.index(Tablas_Input[j])]) #Si encuentra la tabla en un proceso indica que proceso es
          Sub_Proceso_Input.append(SubProceso[Tabla_Creada.index(Tablas_Input[j])])
      else:
          Proceso_Input.append("Tabla Base")
          Sub_Proceso_Input.append("Tabla Base")

#Recursiva para encontrar tipo dependencia

for i in range(len(Proceso_Input)):
      if Proceso_Input[i] == Proceso[i]:
          Tipo_Dependencia.append("Intermedia")
      elif Proceso_Input[i]=="Tabla Base":
          Tipo_Dependencia.append("Tabla Base")
      else:
          Tipo_Dependencia.append("Dependiente")


print(len(Proceso))
print(len(SubProceso))
print(len(Tarea))
print(len(Script))
print(len(Tabla_Creada))
print(len(Tablas_Input))
print(len(Proceso_Input))
print(len(Sub_Proceso_Input))
print(len(Tipo_Dependencia))

print((Proceso))
print((SubProceso))
print((Tarea))
print((Script))

print((Tabla_Creada))
print((Tablas_Input))
print((Proceso_Input))
print((Sub_Proceso_Input))
print((Tipo_Dependencia))


Map_Table= pd.DataFrame({"1.-Proceso":Proceso,"2.-Subproceso":SubProceso,"3.-Tarea":Tarea,"4.-Script":Script,"5.- Tabla_Creada":Tabla_Creada,"6.-Tabla_Input":Tablas_Input,"7.-Proceso_Input":Proceso_Input,"8.-SubProceso_Input":Sub_Proceso_Input,"9.-Tipo_Dependencia":Tipo_Dependencia})  ### DataFrame de mapeo
"""Map_Table= pd.DataFrame({"1.-Proceso":Proceso,"4.-Script":Script,"5.- Tabla_Creada":Tabla_Creada,"6.-Tabla_Input":Tablas_Input,"7.-Proceso_Input":Proceso_Input,"9.-Tipo_Dependencia":Tipo_Dependencia})  ### DataFrame de mapeo"""


# Corrige problema de formato
for column in Map_Table.columns:
    for idx in Map_Table[column].index:
        x = Map_Table.get_value(idx,column)
        try:
            x = unicode(x.encode('utf-8','ignore'),errors ='ignore') if type(x) == unicode else unicode(str(x),errors='ignore')
            Map_Table.set_value(idx,column,x)
        except Exception:
            print 'encoding error: {0} {1}'.format(idx,column)
            Map_Table.set_value(idx,column,'')
            continue

#Cargar en Tabla Historica en Teradata
# 0) Leer desde el Airflow las estructuras
# a) conectar teradata
# b) enmallar proceso

writer = pd.ExcelWriter('Resultantes_Proceso.xlsx')
Map_Table.to_excel(writer,'Sheet1')
writer.save()

