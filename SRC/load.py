import os
import pandas as pd
import logging
import sqlite3

"""
Script para crear una base de datos SQLite con los datos de los episodios, shows y géneros, así como 
agregaciones para visualizar alguna información requerida"""

# Configuración de logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(BASE_DIR, "..", "DATA")
DB_FOLDER = os.path.join(BASE_DIR, "..", "db")
os.makedirs(DB_FOLDER, exist_ok=True)
DB_PATH = os.path.join(DB_FOLDER, "entretenimiento.db")
episodes_path = os.path.join(DATA_FOLDER, "episodes_cleaned.parquet")
shows_path = os.path.join(DATA_FOLDER, "shows_cleaned.parquet")
genres_path = os.path.join(DATA_FOLDER, "genres_cleaned.parquet")


def load_data(episodes_path, shows_path, genres_path):
    """
    Carga los dataframes de los archivos parquet en la carpeta DATA.
    :argumento episodes_path: STRING con la ruta del archivo de episodio.
    :argumento shows_path: STRING con la ruta del archivo de shows.
    :argumento genres_path: STRING con la ruta del archivo de genres.
    :return: DATAFRAMES de episodios, shows y genres editados o None en caso de error.
    """
    try:
        episodes_df = pd.read_parquet(episodes_path)
        shows_df = pd.read_parquet(shows_path)
        genres_df = pd.read_parquet(genres_path)
        return episodes_df, shows_df, genres_df
    except Exception as e:
        logging.error(f"Error cargando los datos: {e}")
        return None


def create_tables():
    """
    Crea las tablas en la base de datos SQLite.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.executescript(
            """
            DROP TABLE IF EXISTS episodes;
            DROP TABLE IF EXISTS shows;
            DROP TABLE IF EXISTS genres;

            CREATE TABLE shows (
                id INTEGER PRIMARY KEY,
                url TEXT,
                name TEXT,
                type TEXT,
                language TEXT,
                status TEXT,
                averageRuntime REAL,
                premiered DATE,
                ended DATE,
                officialSite TEXT,
                schedule_time TIME,
                schedule_days TEXT,
                weight REAL,
                summary TEXT,
                webChannel_name TEXT,
                webChannel_site TEXT,
                externals_thetvdb TEXT,
                externals_imdb TEXT,                                 
                updated TEXT
            );

            CREATE TABLE episodes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                season INTEGER,
                number INTEGER,
                type TEXT,
                airdate DATE, 
                airtime TIME,
                airstamp TIMESTAMP,
                runtime REAL,                
                show_id INTEGER,
                FOREIGN KEY (show_id) REFERENCES shows (id) ON DELETE CASCADE
            );

            CREATE TABLE genres (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                show_id INTEGER,
                genres TEXT,
                FOREIGN KEY (show_id) REFERENCES shows (id) ON DELETE CASCADE
            );
            """
        )
        conn.commit()
        conn.close()
        logging.info("Tablas creadas en la base de datos.")
        return True
    except Exception as e:
        logging.error(f"Error creando las tablas: {e}")
        return False


def load_dfs_to_tables(episodes, shows, genres):
    """
    Carga los dataframes en las tablas de la base de datos.
    :argumento episodes: DATAFRAME de episodios.
    :argumento shows: DATAFRAME de shows.
    :argumento genres: DATAFRAME de géneros.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        episodes.to_sql("episodes", conn, if_exists="replace", index=False)
        shows.to_sql("shows", conn, if_exists="replace", index=False)
        genres.to_sql("genres", conn, if_exists="replace", index=False)
        conn.commit()
        conn.close()
        logging.info("Dataframes cargados en la base de datos.")
        return True
    except Exception as e:
        logging.error(f"Error cargando los dataframes en la base de datos: {e}")
        return False


if __name__ == "__main__":
    episodes, shows, genres = load_data(episodes_path, shows_path, genres_path)
    if episodes is None or shows is None or genres is None:
        logging.error("No se pudo cargar los archivos Parquet. Proceso detenido.")
    else:
        if create_tables():
            load_dfs_to_tables(episodes, shows, genres)
