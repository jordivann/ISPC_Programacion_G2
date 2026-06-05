from database.conexion import conectar
import pymysql.cursors

def ejecutar_select(consulta, parametros=None):
    """
    Ejecuta una consulta SELECT y devuelve los resultados como diccionarios.
    """

    conexion = conectar()

    cursor = conexion.cursor(pymysql.cursors.DictCursor)

    cursor.execute(consulta, parametros or ())

    resultados = cursor.fetchall()

    cursor.close()
    conexion.close()

    return resultados


def ejecutar_modificacion(consulta, parametros=None):
    """
    Ejecuta INSERT, UPDATE o DELETE.
    Realiza commit porque modifica datos.
    """
    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute(consulta, parametros or ())

    conexion.commit()

    filas_afectadas = cursor.rowcount
    ultimo_id = cursor.lastrowid

    cursor.close()
    conexion.close()

    return filas_afectadas, ultimo_id