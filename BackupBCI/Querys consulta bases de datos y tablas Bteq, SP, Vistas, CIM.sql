

/*******  CONSULTAS INDIVIDUALES *******/


select tipo_archivo, archivo, TO_NUMBER(numero_paso), sentencia_dml, esquema_output, tabla_output, esquema_input, tabla_input
from edw_tempusu.LAC_LEVANTAMIENTO_TABLAS_BTEQ 
order by 1,2,3;

select tipo_archivo, archivo, TO_NUMBER(numero_paso), sentencia_dml, esquema_output, tabla_output, esquema_input, tabla_input
from edw_tempusu.LAC_LEVANTAMIENTO_TABLAS_SP 
order by 1,2,3;

select tipo_archivo, archivo, sentencia_dml, esquema_output, tabla_output, esquema_input, tabla_input
from edw_tempusu.LAC_LEVANTAMIENTO_TABLAS_VISTAS 
order by 1,2;



/*******  CONSULTAS BASES DE DATOS POR TIPO DE ARCHIVO *******/


SELECT distinct esquema, tipo_archivo
FROM(
	SELECT  distinct esquema_output as esquema, 'VISTA' as tipo_archivo
	FROM edw_tempusu.LAC_LEVANTAMIENTO_TABLAS_VISTAS
	UNION ALL 
	SELECT distinct esquema_input as esquema, 'VISTA' as tipo_archivo
	FROM edw_tempusu.LAC_LEVANTAMIENTO_TABLAS_VISTAS
UNION ALL 
	SELECT  distinct esquema_output as esquema, 'SP' as tipo_archivo
	FROM edw_tempusu.LAC_LEVANTAMIENTO_TABLAS_SP
	UNION ALL 
	SELECT distinct esquema_input as esquema, 'SP' as tipo_archivo
	FROM edw_tempusu.LAC_LEVANTAMIENTO_TABLAS_SP
UNION ALL 
	SELECT  distinct esquema_output as esquema, 'BTEQ' as tipo_archivo
	FROM edw_tempusu.LAC_LEVANTAMIENTO_TABLAS_BTEQ
	UNION ALL 
	SELECT distinct esquema_input as esquema, 'BTEQ' as tipo_archivo
	FROM edw_tempusu.LAC_LEVANTAMIENTO_TABLAS_BTEQ
) TABLAS
where esquema <> 'Parametros: No tiene condicion'
and esquema not like '%TEMP%'
order by 2,1;


/*******  CONSULTAS TABLAS POR TIPO DE ARCHIVO *******/



SELECT distinct esquema, tabla, tipo_archivo
FROM(
	SELECT  distinct esquema_output as esquema, tabla_output as tabla, 'VISTA' as tipo_archivo
	FROM edw_tempusu.LAC_LEVANTAMIENTO_TABLAS_VISTAS
	UNION ALL 
	SELECT distinct esquema_input as esquema, tabla_input as tabla, 'VISTA' as tipo_archivo
	FROM edw_tempusu.LAC_LEVANTAMIENTO_TABLAS_VISTAS
UNION ALL 
	SELECT  distinct esquema_output as esquema, tabla_output as tabla, 'SP' as tipo_archivo
	FROM edw_tempusu.LAC_LEVANTAMIENTO_TABLAS_SP
	UNION ALL 
	SELECT distinct esquema_input as esquema, tabla_input as tabla, 'SP' as tipo_archivo
	FROM edw_tempusu.LAC_LEVANTAMIENTO_TABLAS_SP
UNION ALL 
	SELECT  distinct esquema_output as esquema, tabla_output as tabla,'BTEQ' as tipo_archivo
	FROM edw_tempusu.LAC_LEVANTAMIENTO_TABLAS_BTEQ
	UNION ALL 
	SELECT distinct esquema_input as esquema, tabla_input as tabla, 'BTEQ' as tipo_archivo
	FROM edw_tempusu.LAC_LEVANTAMIENTO_TABLAS_BTEQ
) TABLAS
where esquema <> 'Parametros: No tiene condicion'
and esquema not like '%TEMP%'
order by 3,1,2;






/*******  CONSULTAS COMUNICACIONES DE CIM  *******/


select distinct nombre_comunicacion 
from edw_tempusu.LAC_LEVANTAMIENTO_TABLAS_CIM 
order by 1;


/*******  CONSULTAS SEGMENTACIONES DE CIM  *******/

select nombre_comunicacion, nombre_segmento, esquema_input, tabla_input
from edw_tempusu.LAC_LEVANTAMIENTO_TABLAS_CIM 
order by 1,2;


