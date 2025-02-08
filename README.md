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
