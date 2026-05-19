import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()


def obtener_conexion():
    """
    Crea una conexión a MySQL usando las variables del archivo .env.
    """
    try:
        conexion = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=int(os.getenv("DB_PORT", 3306))
        )
        return conexion

    except Error as error:
        print(f"Error al conectar con MySQL: {error}")
        return None


def probar_conexion():
    """
    Prueba si la conexión a MySQL funciona correctamente.
    """
    conexion = obtener_conexion()

    if conexion is None:
        print("No se pudo conectar a la base de datos.")
        return False

    try:
        if conexion.is_connected():
            cursor = conexion.cursor()
            cursor.execute("SELECT DATABASE();")
            resultado = cursor.fetchone()

            print("Conexión exitosa a MySQL.")
            print(f"Base de datos conectada: {resultado[0]}")

            cursor.close()
            return True

    except Error as error:
        print(f"Error durante la prueba de conexión: {error}")
        return False

    finally:
        if conexion.is_connected():
            conexion.close()


def ejecutar_consulta(consulta, parametros=None):
    """
    Ejecuta una consulta SELECT y devuelve los resultados como lista de diccionarios.
    """
    conexion = obtener_conexion()

    if conexion is None:
        return []

    cursor = None

    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(consulta, parametros or ())
        resultados = cursor.fetchall()
        return resultados

    except Error as error:
        print(f"Error al ejecutar la consulta: {error}")
        return []

    finally:
        if cursor:
            cursor.close()

        if conexion.is_connected():
            conexion.close()


def imprimir_resultados(titulo, resultados):
    """
    Imprime los resultados de una consulta de forma legible.
    """
    print()
    print(titulo)
    print("=" * 70)

    if not resultados:
        print("No se encontraron resultados.")
        print("=" * 70)
        return

    for fila in resultados:
        for clave, valor in fila.items():
            print(f"{clave}: {valor}")
        print("-" * 70)