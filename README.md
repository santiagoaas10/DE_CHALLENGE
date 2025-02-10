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
