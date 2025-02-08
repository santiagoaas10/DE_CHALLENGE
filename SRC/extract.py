import os
import requests
import json
from datetime import datetime, timedelta
import logging

# Configuración de los logs
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# URL de la API (solo la base) y dirección de donde se guardarán los archivos .json correspondientes a cada día
BASE_URL = "http://api.tvmaze.com/schedule/web"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_FOLDER = os.path.join(BASE_DIR, "..", "JSON")


def fetch_tv_shows(date: str) -> list:
    """
    Obtiene todas las series emitidas en una fecha específica desde la API de TVMaze.

    :argumento date: STRING de Fecha en formato YYYY-MM-DD.
    :return: Lista de diccionarios con la información de las series.
    """
    url = f"{BASE_URL}?date={date}"
    try:
        response = requests.get(url, timeout=10)  # petición GET a la API
        response.raise_for_status()
        logging.info(f"Datos obtenidos correctamente para la fecha {date}")
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error al obtener datos de la API: {e}")
        return []


def save_json(data: list, date: str, JSON_FOLDER: str) -> str:
    """
    Guarda los datos en un archivo JSON.

    :argumento data: Datos a guardar, respuesta JSON de la API.
    :argumento date: Fecha para nombrar el archivo.
    :argumento folder: Ruta donde se guardará el archivo.
    :return: Ruta del archivo guardado, o string vacío en caso de que no se guarde satisfactoriamente.
    """
    os.makedirs(JSON_FOLDER, exist_ok=True)
    file_path = os.path.join(JSON_FOLDER, f"tv_shows_{date}.json")
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        logging.info(f"Archivo guardado: {file_path}")
        return file_path
    except Exception as e:
        logging.error(f"Error al guardar JSON: {e}")
        return ""


if __name__ == "__main__":
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 1, 31)
    for i in range((end_date - start_date).days + 1):
        date_str = (start_date.replace(day=1) + timedelta(days=i)).strftime("%Y-%m-%d")
        shows = fetch_tv_shows(date_str)
        if shows:
            save_json(shows, date_str, JSON_FOLDER)
