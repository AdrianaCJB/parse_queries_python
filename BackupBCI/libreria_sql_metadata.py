import sql_metadata as sql


queryString = "REPLACE VIEW ARMVIEWS.RMA_EPI_OPORTUNIDAD_A AS LOCK ROW FOR ACCESS SELECT Cliente_rut (INTEGER) AS RUT_NUM,1 AS Flg_epi_oportunidad FROM BCIMKT.IN_EPI_Oportunidad"
## EXTRAE QUERY
query1 = sql.get_query_tokens(queryString)
query2 = sql.get_query_tables(queryString)
query3 = sql.get_query_columns(queryString)


print("query = " + str(query1))
print("tables = " + str(query2))
print("columns = " + str(query3))




