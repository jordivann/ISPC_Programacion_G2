import os
import mysql.connector

from dotenv import load_dotenv

# Cargar variables del .env
load_dotenv()

def conectar():

    conexion = mysql.connector.connect(

        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")

    )

    return conexion