# 📊 Lulo Bank - Prueba Técnica Data Engineer

Este proyecto resuelve la prueba técnica de Lulo Bank para el rol de Data Engineer. Su objetivo es extraer, transformar, analizar y almacenar información de series de TV emitidas en Enero de 2024, utilizando Python y buenas prácticas de ingeniería de datos.

Se realiza una extracción desde la API de TVMaze, seguida de transformaciones, análisis de calidad de datos, almacenamiento en Parquet y una base de datos SQLite. Finalmente, se generan agregaciones y estadísticas relevantes.

## 🛠️ Tecnologías Utilizadas

- **Lenguaje:** Python 3.8+
- **ETL:** `pandas`, `requests`, `matplotlib`
- **Almacenamiento:** Archivos JSON, Parquet con compresión Snappy, SQLite
- **Análisis de Datos:** `ydata-profiling`, `pandas`, `profiling`
- **Testing:** `pytest`
- **ORM:** `SQLAlchemy`

📡 API → 🗄️ JSON → 📊 DataFrames → 🔍 Profiling → 🛠️ Limpieza → 📁 Parquet → 🏛️ SQLite → 📈

### 1️⃣ clonar el repositorio

Ejecuta el siguiente comando en tu sistema

```
git clone https://github.com/santiagoaas10/DE_CHALLENGE.git
```

### 2️⃣ Crear un entorno virtual

Ejecuta el siguiente comando según tu sistema operativo:

#### **En Windows **

```bash
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4️⃣ Extraer los datos desde la API y cargar en .json

Se ejecuta este Script y se obtiene la carpeta JSON con los archivos leidos desde la API para cada día

```bash
python src/extract.py
```

### 5️⃣ Crear Dataframes de Shows y Episodios, obtener el profiling de los datos como HTML y análisis de estos

Cuando se ejecute el script dfs_creation.py se obtendrán los dataframes creados con pandas a partir de la lectura de los objetos JSON, también se generarán dos archivos que son episodes_report.html y shows_report.html que se pueden abrir en el navegador y dan unas métricas estadísticas de los datos y análisis exploratorio de los mismos. Adicionalmente se agregí el archivo ANALISIS.md que contiene el análisis propio y aterrizado de estre profiling.
Los Dataframes quedan cargados inicialmente como CSVs en la carpeta DATA

```bash
python src/dfs_creation.py
```

### 6️⃣ Hacer la limpieza de datos, de acuerdo a lo mencionado en el análisis y cargar en formato parquet

Cuando se ejecute el script clean.py se obtendrán los 3 dataframes almacenados en formato parquet, el de shows (normalizado y sin columnas redundantes), episodes (sin columnas redundantes) y también el nuevo de genres

Estos dataframes quedarán en la carpeta DATA con los siguientes nombres:

- episodes_cleaned.parquet
- shows_cleaned.parquet
- genres_cleaned.parquet

```bash
python src/clean.py
```

### 7️⃣ Lectura de archivos parquet, almacenamiento en base de datos entretenimiento.db, creación de modelo de datos y posterior carga de datos a tablas definidas en el modelo

Cuando se ejecuta el script load.py, se obtendrá una base de datos lamada entretenimiento en la carpeta db, allí habrán 3 tablas que se crearán a partir de la lectura de los 3 DataFrames almacenados en formato parquet, correspondientes al modelo explicado a través del diagrama de entidad disponible en model/model.png

```bash
python src/load.py
```

### 8️⃣ Lectura de base de datos para responder a las preguntas sobre los datos.

Al ejecutar el script read.py se obtiene la información correspondiente a las preguntas realizadas sobre los datos:

a. Runtime promedio (averageRuntime).
b. Conteo de shows de tv por género.
c. Listar los dominios únicos (web) del sitio oficial de los shows.

```bash
python src/read.py
```
