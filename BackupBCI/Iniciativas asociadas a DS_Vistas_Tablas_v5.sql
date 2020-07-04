/* 
   Consulta para determinar objetos  asociados a una Iniciaiva, Atributo, Data Source, Tabla ó Vista.
   Formato de variable = NOMBRE (Atributo/DS/Tabla/Vista) con comillas simples
   		Ej.: 'ARMINP.RME_CAMPANAHIPOTECARIO' o 'DS_CRM_INPUT_CON_INTEGRACION' 
*/
LOCK ROW FOR ACCESS
 -- SEGMENTACIÓN
SELECT 
	  comunicacion.NAME AS nombre_comunicacion
	, ATT.Attribute_Desc AS ATRIBUTO
	, DDS.NAME AS DATA_SOURCE
	, E.NAME AS BASE_DATOS
	, T.NAME AS TABLAS_VISTAS
FROM ARMCORE.CM_COMMUNICATION comunicacion

INNER JOIN ARMCORE .SM_SEGMENT_PLAN segment_plan
ON comunicacion.Segment_Plan_Id = segment_plan.Segment_Plan_Id

INNER JOIN ARMCORE.SM_LOGICAL_SEGMENT logical_segment 
ON segment_plan.Segment_Plan_Id = logical_segment.Segment_Plan_Id 

INNER JOIN ARMCORE.SM_SEGMENT SEG
ON logical_segment.Segment_Id = SEG.Segment_Id

INNER JOIN ARMCORE.SM_SELECTION_PLAN selection_plan
ON selection_plan.Selection_Plan_Id = SEG.Selection_Plan_Id

INNER JOIN ARMCORE.SM_SELECTION SSE
ON selection_plan.Selection_Plan_Id = SSE.Selection_Plan_Id

INNER JOIN ARMCORE.SM_SELECTION_CRITERIA_SET SCS
ON SSE.Selection_Plan_Id = SCS.Selection_Plan_Id

INNER JOIN ARMCORE.SM_SELECTION_CRITERIA SSA
ON SSA.Selection_Plan_Id = SSE.Selection_Plan_Id
AND SSA.Criteria_Set_Id = SCS.Criteria_Set_Id
AND SSA.Criteria_Id = SSE.Criteria_Id

LEFT JOIN (
    SELECT MAS.Attribute_Schema_Id , MAS.Attribute_Id, MAT.Description Attribute_Desc
    FROM ARMCORE.MD_ATTRIBUTE_SCHEMA   MAS
    INNER JOIN ARMCORE.MD_ATTRIBUTE MAT
    ON MAS.Attribute_Id = MAT.Attribute_Id
) ATT
ON ATT.Attribute_Schema_Id = SSE.Attribute_Schema_Id

LEFT JOIN ARMCORE.MD_ATTRIBUTE_COLUMN AC
ON ATT.attribute_id = AC.attribute_id

LEFT JOIN ARMCORE.MD_TABLE T
ON T.table_id = AC.Table_id

LEFT JOIN  ARMCORE.MD_DATABASE E
ON T.Database_Id = E.Database_Id

LEFT JOIN ARMCORE.DS_DATA_SOURCE DDS
ON DDS.Data_Source_Id = SSE.Data_Source_Id

LEFT JOIN ARMCORE.CR_TEXT_STORAGE_DATA  TSD
ON DDS.Sql_Statement_Id = TSD.text_storage_id   
/* -- Comunicaciones Productivas
JOIN ARMCUST.CRM_BATCH_CAMPAIGN CBC
ON comunicacion.NAME = CBC.Description
*/

WHERE ( DDS.NAME IN (SEL NAME FROM  ARMCORE.DS_DATA_SOURCE DDS
					LEFT JOIN ARMCORE.CR_TEXT_STORAGE_DATA  TSD
					ON DDS.Sql_Statement_Id = TSD.text_storage_id  
					WHERE TSD.TEXT_VAL LIKE '%'||?var||'%' 	)
					
OR T.NAME(VARCHAR(128)) IN (SELECT TABLENAME(VARCHAR(128))  FROM DBC.TABLESv
						WHERE TableKind = 'V' AND requesttext LIKE '%'||?var||'%'
						AND DATABASENAME NOT LIKE 'DS_%' )	
						
OR T.NAME(VARCHAR(128)) IN (SEL T.TABLENAME FROM DBC.TABLESV T
							INNER JOIN (SELECT TABLENAME FROM DBC.TABLESv
											WHERE TableKind = 'V' AND requesttext LIKE '%'||?var||'%'
											AND DATABASENAME NOT LIKE 'DS_%'
										) DEV
							ON INDEX(T.REQUESTTEXT, DEV.TABLENAME ) > 1
							WHERE T.DATABASENAME NOT LIKE 'DS_%')
			
OR DDS.NAME IN (SEL NAME FROM  ARMCORE.DS_DATA_SOURCE DDS
				LEFT JOIN ARMCORE.CR_TEXT_STORAGE_DATA  TSD
				ON DDS.Sql_Statement_Id = TSD.text_storage_id  
				INNER JOIN (SELECT TABLENAME(VARCHAR(128))  FROM DBC.TABLESv
						WHERE TableKind = 'V' AND requesttext LIKE '%'||?var||'%' ) TBL
				ON INDEX(TSD.TEXT_VAL, TABLENAME)> 1
			)

OR DDS.NAME = ?var 
)
AND (INSTR(UPPER(comunicacion.NAME), 'TEST') = 0  AND INSTR(UPPER(comunicacion.NAME), 'BKP') = 0 )	
GROUP BY 1,2,3,4,5

UNION

 -- SALIDAS
 (
SELECT  
         COMM.NAME AS Communication_Name
		,ATT.Attribute_Desc AS ATRIBUTO
        ,F.NAME AS DATA_SOURCE
        ,CASE WHEN F.NAME IS NULL THEN E.NAME ELSE NULL END BASE_DATOS
        ,CASE WHEN F.NAME IS NULL THEN D.NAME ELSE NULL END TABLAS_VISTAS
    FROM ARMCORE.CM_COMMUNICATION COMM
    JOIN (
              SELECT Communication_Id, Presentation_Template_Id
             FROM ARMCORE.CM_COMM_PACKAGE_PRESENTATION 
             GROUP BY 1,2
     ) CPP
     ON COMM.Communication_Id = CPP.Communication_Id
	 

    LEFT JOIN ARMCORE.OM_PRESENTATION_TEMPLATE TPT
    ON CPP.Presentation_Template_Id = TPT.Presentation_Template_Id           
     
    JOIN ARMCORE.OM_EXTRACT_ELEMENT A
    ON A.Extract_Format_Id = TPT.Extract_Format_Id
	
	LEFT JOIN (
	    SELECT MAS.Attribute_Schema_Id , MAS.Attribute_Id, MAT.Description Attribute_Desc
	    FROM ARMCORE.MD_ATTRIBUTE_SCHEMA   MAS
	    INNER JOIN ARMCORE.MD_ATTRIBUTE MAT
	    ON MAS.Attribute_Id = MAT.Attribute_Id
	) ATT
	ON ATT.Attribute_Id = A.Attribute_Id
	
	LEFT JOIN ARMCORE.MD_ATTRIBUTE_COLUMN AC
    ON ATT.attribute_id = AC.attribute_id

    LEFT JOIN ARMCORE.MD_COLUMN C
    ON AC.Column_Id = C.Column_Id

    LEFT JOIN  ARMCORE.MD_TABLE D
    ON C.Table_Id = D.Table_Id

    LEFT JOIN  ARMCORE.MD_DATABASE E
    ON D.Database_Id = E.Database_Id
	

    LEFT JOIN ARMCORE.DS_DATA_SOURCE F
    ON A.Data_Source_Id = F.Data_Source_Id

    LEFT JOIN ARMCORE.DS_DATA_SOURCE_COLUMN G
    ON F.Data_Source_Id = G.Data_Source_id
    AND g.Data_Source_Column_Id = a.Data_Source_Column_Id 
	
	
	/* -- Comunicaciones Productivas
	JOIN ARMCUST.CRM_BATCH_CAMPAIGN CBC
	ON COMM.NAME = CBC.Description
	*/
    WHERE ( (F.NAME IN (SEL NAME FROM  ARMCORE.DS_DATA_SOURCE DDS
				LEFT JOIN ARMCORE.CR_TEXT_STORAGE_DATA  TSD
				ON DDS.Sql_Statement_Id = TSD.text_storage_id  
				WHERE TSD.TEXT_VAL LIKE '%'||?var||'%' )
		)
		OR D.NAME(VARCHAR(128)) IN (SELECT TABLENAME(VARCHAR(128))  FROM DBC.TABLESv
						WHERE TableKind = 'V' AND requesttext LIKE '%'||?var||'%'
						AND DATABASENAME NOT LIKE 'DS_%' )
						
		OR ( E.NAME, D.NAME) IN ( SELECT  A.DATABASENAME AS BD_PADRE
										 ,A.TABLENAME AS VIEW_PADRE
									FROM DBC.TABLESv A
									INNER JOIN  (
												SELECT DATABASENAME, TABLENAME(VARCHAR(128))  FROM DBC.TABLESv
												WHERE TableKind = 'V' AND requesttext LIKE '%'||?var||'%'
												) B
									ON INSTR(A.requesttext , B.TABLENAME ) > 1 
									AND A.DATABASENAME = B.DATABASENAME )
		OR F.NAME = ?var )
	AND (INSTR(UPPER(COMM.NAME), 'TEST') = 0  AND INSTR(UPPER(COMM.NAME), 'BKP') = 0)	
GROUP BY 1,2,3,4,5

UNION 
-- Tablas de Paso
SELECT  
         COMM.NAME AS Communication_Name
		,' ' AS ATRIBUTO
        ,' ' AS DATA_SOURCE
        ,'ARMOUT' AS BASE_DATOS
        ,TPT.Table_Name_Txt AS TABLAS_VISTAS

    FROM ARMCORE.CM_COMMUNICATION COMM
    JOIN (
              SELECT Communication_Id, Presentation_Template_Id
             FROM ARMCORE.CM_COMM_PACKAGE_PRESENTATION 
             GROUP BY 1,2
     ) CPP
    ON COMM.Communication_Id = CPP.Communication_Id

    JOIN ARMCORE.OM_PRESENTATION_TEMPLATE TPT
    ON CPP.Presentation_Template_Id = TPT.Presentation_Template_Id     

	/* -- Comunicaciones Productivas
	JOIN ARMCUST.CRM_BATCH_CAMPAIGN CBC
	ON COMM.NAME = CBC.Description
	*/
    WHERE INSTR('ARMOUT.'||TPT.Table_Name_Txt, ?var ) > 0 OR TPT.Table_Name_Txt = ?var	
	AND (INSTR(UPPER(COMM.NAME), 'TEST') = 0  AND INSTR(UPPER(COMM.NAME), 'BKP') = 0)	
GROUP BY 1,2,3,4,5
)
;



