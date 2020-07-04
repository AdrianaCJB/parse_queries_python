/*

SELECT HOLA
FROM campanas_pyme.ArithmeticError
WHERE id in (SELECT id from campanas_pyme.ArithmeticError)

*/


SELECT HOLA FROM campanas_pyme.ArithmeticError WHERE id in (SELECT id from campanas_pyme.loquesea);



CREATE TABLE pruebas.tablacreada
SELECT hola
FROM tablax;
