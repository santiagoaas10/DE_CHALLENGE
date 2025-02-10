import os
import json
import pandas as pd
import logging
from ydata_profiling import ProfileReport

# Configuración de logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Definir la carpeta donde están los JSON para leerlos y general los DatagFrames
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_FOLDER = os.path.join(BASE_DIR, "..", "JSON")
DATA_FOLDER = os.path.join(BASE_DIR, "..", "DATA")
PROFILING_FOLDER = os.path.join(BASE_DIR, "..", "profiling")


def load_json_files(json_folder: str) -> list:
    """
    Carga todos los archivos JSON en una lista.
    :argumento json_folder: STRING con la ruta de la carpeta que contiene los archivos JSON.
    :return: LISTA con los datos combinados de todos los archivos JSON.
    """
    all_data = []
    for file_name in os.listdir(json_folder):  # Recorre archivos en la carpeta
        if file_name.endswith(".json"):  # asegurarnos de que sea un archivo JSON
            file_path = os.path.join(json_folder, file_name)
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)  # Cargar el JSON
                all_data.extend(data)  # Agregar los datos a la lista principal
    return all_data


def transform_data(json_data: list) -> tuple:
    """
    Transforma los datos JSON en DataFrames normalizados para episodios y shows.

    :argumento json_data: LISTA de diccionarios con los datos extraídos de los archivos JSON.
    :return: TUPLA de dos DataFrames (episodes_df, shows_df).
    """

    episodes_list = []  # Lista para episodios
    shows_dict = {}  # Diccionario para series (evita duplicados)

    for item in json_data:
        show_data = item.get("_embedded", {}).get(
            "show", {}
        )  # Extraer info del show (serie)

        # Extraer ID del show
        show_id = show_data.get("id")

        # Guardar información de la serie si aún no está
        if show_id and show_id not in shows_dict:
            shows_dict[show_id] = {
                "id": show_id,
                "url": show_data.get("url", pd.NA),
                "name": show_data.get("name", pd.NA),
                "type": show_data.get("type", pd.NA),
                "language": show_data.get("language", pd.NA),
                "genres": show_data.get("genres") if show_data.get("genres") else pd.NA,
                "status": show_data.get("status", pd.NA),
                "runtime": show_data.get("runtime", pd.NA),
                "averageRuntime": show_data.get("averageRuntime", pd.NA),
                "premiered": show_data.get("premiered", pd.NA),
                "ended": show_data.get("ended", pd.NA),
                "officialSite": show_data.get("officialSite", pd.NA),
                "schedule_time": show_data.get("schedule", {}).get("time", pd.NA),
                "schedule_days": (
                    show_data.get("schedule", {}).get("days")
                    if show_data.get("schedule", {}).get("days")
                    else pd.NA
                ),
                "rating": show_data.get("rating", {}).get("average", pd.NA),
                "weight": show_data.get("weight", pd.NA),
                "summary": show_data.get("summary", pd.NA),
                "webChannel_name": (show_data.get("webChannel") or {}).get(
                    "name", pd.NA
                ),
                "webChannel_site": (show_data.get("webChannel") or {}).get(
                    "officialSite", pd.NA
                ),
                "dvd_country": show_data.get("dvdCountry", pd.NA),
                "externals_tvrage": (show_data.get("externals") or {}).get(
                    "tvrage", pd.NA
                ),
                "externals_thetvdb": (show_data.get("externals") or {}).get(
                    "thetvdb", pd.NA
                ),
                "externals_imdb": (show_data.get("externals") or {}).get("imdb", pd.NA),
                "updated": show_data.get("updated", pd.NA),
            }

        # Guardar episodio con referencia al show
        episodes_list.append(
            {
                "id": item.get("id", pd.NA),
                "name": item.get("name", pd.NA),
                "season": item.get("season", pd.NA),
                "number": item.get("number", pd.NA),
                "type": item.get("type", pd.NA),
                "airdate": item.get("airdate", pd.NA),
                "airtime": item.get("airtime", pd.NA),
                "airstamp": item.get("airstamp", pd.NA),
                "runtime": item.get("runtime", pd.NA),
                "rating": item.get("rating", {}).get("average", pd.NA),
                "show_id": show_id,  # Clave foránea para relacionarlo con la serie
            }
        )

    # Convertimos datos procesados a dataframes
    episodes_df = pd.DataFrame(episodes_list)
    shows_df = pd.DataFrame(shows_dict.values())

    return episodes_df, shows_df


def load_dfs(episodes_df, shows_df) -> None:
    """
    Guarda los DataFrames en archivos CSV dentro de la carpeta DATA especificada.
    :argumento episodes_df: DATAFRAME con la información de los episodios.
    :param shows_df: DATAFRAME con la información de las shows.
    :argumento DATA_FOLDER: STRING con la ruta de la carpeta donde se guardarán los CSV.
    :return: None
    """
    os.makedirs(DATA_FOLDER, exist_ok=True)
    episodes_df.to_csv(os.path.join(DATA_FOLDER, "episodes.csv"), index=False)
    shows_df.to_csv(os.path.join(DATA_FOLDER, "shows.csv"), index=False)


def profiling(episodes_df, shows_df) -> None:
    """
    Genera reportes de profiling en formato HTML para los DataFrames de episodios y shows.

    :argumento episodes_df: DATAFRAME con la información de los episodios.
    :argumento shows_df: DATAFRAME con la información de las shows.
    :return: None
    """

    episodes_profile = ProfileReport(
        episodes_df, title="Episodes Data Profiling", explorative=True
    )
    shows_profile = ProfileReport(
        shows_df, title="Shows Data Profiling", explorative=True
    )

    # Crear carpeta 'profiling' si no existe
    os.makedirs(PROFILING_FOLDER, exist_ok=True)

    # Guardar los reportes en archivos HTML
    episodes_report_path = os.path.join(PROFILING_FOLDER, "episodes_report.html")
    shows_report_path = os.path.join(PROFILING_FOLDER, "shows_report.html")

    episodes_profile.to_file(episodes_report_path)
    shows_profile.to_file(shows_report_path)
    logging.info("Profiling completado. Revisa los archivos en la carpeta 'profiling'.")


if __name__ == "__main__":
    json_data = load_json_files(JSON_FOLDER)  # Cargar JSONs
    episodes_df, shows_df = transform_data(json_data)  # Transformar datos

    load_dfs(episodes_df, shows_df)

    profiling(episodes_df, shows_df)

