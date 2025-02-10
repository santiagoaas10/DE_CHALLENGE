import os
import pandas as pd
import logging
import sqlite3

"""
Script para responder las preguntas planteadas en la prueba.

De acuerdo a los datos extraídos y procesados, se realizarán consultas:
a. Runtime promedio (averageRuntime).
b. Conteo de shows de TV por género.
c. Listar los dominios únicos (web) del sitio oficial de los shows.
"""

# Configuración de logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Definir la ruta de la base de datos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FOLDER = os.path.join(BASE_DIR, "..", "db")
DB_PATH = os.path.join(DB_FOLDER, "entretenimiento.db")


def connect_db():
    """
    Intenta conectar a la base de datos y maneja errores en caso de falla.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        logging.info("Conexión a la base de datos establecida correctamente.")
        return conn
    except sqlite3.Error as e:
        logging.error(f"Error al conectar con la base de datos: {e}")
        return None


def execute_query(conn, query):
    """
    Ejecuta una consulta SQL y maneja errores en caso de que falle.
    """
    try:
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        logging.error(f"Error al ejecutar la consulta: {query}\n{e}")
        return None


def read_db():
    """
    Realiza la lectura de la base de datos y ejecuta consultas.
    """
    conn = connect_db()
    if not conn:
        logging.error(
            "No se pudo establecer conexión con la base de datos. Saliendo del script."
        )
        return

    queries = {
        "Shows con promedio de runtime": "SELECT name, averageRuntime FROM shows LIMIT 10;",
        "Cantidad de shows por género": "SELECT genres AS genero, COUNT(id) AS cantidad_shows FROM genres GROUP BY genres LIMIT 10;",
        "Sitios oficiales de algunos shows": "SELECT officialSite FROM shows LIMIT 10;",
    }

    for desc, query in queries.items():
        logging.info(f"Ejecutando consulta: {desc}")
        result = execute_query(conn, query)
        if result is not None:
            print(f"\n{desc}:")
            print(result)
        else:
            logging.warning(f"No se pudo obtener resultados para: {desc}")

    conn.close()
    logging.info("Conexión a la base de datos cerrada.")


if __name__ == "__main__":
    read_db()
