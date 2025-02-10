import os
import pandas as pd
import ast  # Para convertir cadenas en listas reales
import logging


"""
Script para limpiar los datos de los episodios y shows a partir de las sugerencias incluidas
en el análisis.

Se eliminarán columnas innecesarias, se creará un nuevo dataframe llamado genres para
normalizar la información, se crearán 3 nuevos dataframes y se guardarán tanto en CSV como en formato parquet.
"""

# Configuración de logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# directorios y rutas base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(BASE_DIR, "..", "DATA")
os.makedirs(DATA_FOLDER, exist_ok=True)
episodes_path = os.path.join(DATA_FOLDER, "episodes.csv")
shows_path = os.path.join(DATA_FOLDER, "shows.csv")


def load_data(episodes_path, shows_path):
    """
    Carga los dataframes de los archivos CSV en la carpeta DATA.
    :argumento episodes_path: STRING con la ruta del archivo de episodio.
    :argumento shows_path: STRING con la ruta del archivo de shows.
    :return: DATAFRAMES de episodios y shows editados.
    """
    episodes_df = pd.read_csv(episodes_path)
    shows_df = pd.read_csv(shows_path)
    return episodes_df, shows_df


def delete_unnecessary_columns(episodes_df, shows_df):
    """
    Elimina columnas innecesarias de los dataframes de episodios y shows.
    :argumento episodes_df: DATAFRAME de episodios.
    :argumento shows_df: DATAFRAME de shows.
    :return: DATAFRAME de episodios y shows sin columnas innecesarias.
    """
    episodes_df = episodes_df.drop(columns=["rating"], errors="ignore")
    shows_df = shows_df.drop(
        columns=["rating", "runtime", "dvd_country", "externals_tvrage"],
        errors="ignore",
    )
    return episodes_df, shows_df


def genres_creation(shows_df):
    """
    Extrae la información de los géneros de las series y crea un nuevo dataframe con la información normalizada.
    :argumento shows_df: DATAFRAME de shows.
    :return: DATAFRAME de géneros
    :return: DATAFRAME de shows sin columna genre (normalizado).
    """
    # convierto la cadena en listas, para luego hacerles un explode
    shows_df["genres"] = shows_df["genres"].apply(
        lambda x: ast.literal_eval(x) if isinstance(x, str) else x
    )
    shows_exploded = shows_df[["id", "genres"]].explode("genres").reset_index(drop=True)
    shows_df = shows_df.drop(
        columns=["genres"], errors="ignore"
    )  # Eliminar columna genres de shows_df

    genres_df = shows_exploded.rename(
        columns={"id": "show_id"}
    ).dropna()  # Renombrar columna 'id' a 'show_id'

    genres_df.insert(
        0, "id", range(1, len(genres_df) + 1)
    )  # Añadir columna 'id', autoincremental
    return genres_df, shows_df


def save_as_parquet(episodes_df, shows_df, genres_df):
    """
    Almacena 3 dataframes que han sido limpiados en formato parquet
    :argumento episodes_df: DATAFRAME de episodios.
    :argumento shows_df: DATAFRAME de shows.
    :argumento genres_df: DATAFRAME de géneros.
    :return: None
    """
    episodes_df.to_parquet(
        os.path.join(DATA_FOLDER, "episodes_cleaned.parquet"),
        index=False,
        compression="snappy",
    )
    shows_df.to_parquet(
        os.path.join(DATA_FOLDER, "shows_cleaned.parquet"),
        index=False,
        compression="snappy",
    )
    genres_df.to_parquet(
        os.path.join(DATA_FOLDER, "genres_cleaned.parquet"),
        index=False,
        compression="snappy",
    )
    logging.info("Dataframes guardados en formato parquet.")


if __name__ == "__main__":
    episodios, shows = load_data(episodes_path, shows_path)
    episodios_clean, shows_clean = delete_unnecessary_columns(episodios, shows)
    genres_clean, shows_clean = genres_creation(shows_clean)
    save_as_parquet(episodios_clean, shows_clean, genres_clean)
    logging.info("Proceso de limpieza finalizado.")
