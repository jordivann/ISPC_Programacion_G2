import mysql.connector
import os
from dotenv import load_dotenv  # Asegúrate de tener un archivo .env con las variables de conexión
from mysql.connector import Error

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
            port=3306
        )
        return conexion

    except Error as error:
        print(f"Error al conectar con MySQL: {error}")
        return None


