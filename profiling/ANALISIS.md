# Análisis de Datos - Profiling Report

A partir de los datos obtenidos de la API, se generaron dos DataFrames principales:

1. **Episodios**: recopila la información de cada uno de los Episodios en la API
2. **Shows**: Contiene información sobre las series a las cuales pertenecen los episodios.

Ambos DataFrames pueden ser unidos mediante la clave 'show_id'.

## Columnas y Tipos de Datos

### DataFrame `episodes`

| Columna  | Tipo de Dato | Descripción                                                     |
| -------- | ------------ | --------------------------------------------------------------- |
| id       | int          | Identificador único del episodio.                               |
| name     | object       | Nombre del episodio.                                            |
| season   | int          | Número de la temporada a la que pertenece.                      |
| number   | float        | Número del episodio dentro de la temporada.                     |
| type     | object       | Tipo de episodio (`regular`, `special`, etc.).                  |
| airdate  | object       | Fecha de emisión del episodio en formato `YYYY-MM-DD`.          |
| airtime  | object       | Hora de emisión del episodio.                                   |
| airstamp | object       | Fecha y hora de emisión en formato de timestamp.                |
| runtime  | float        | Duración del episodio en minutos.                               |
| rating   | float        | Calificación promedio del episodio.                             |
| show_id  | int          | Identificador único de la serie a la que pertenece el episodio. |

### DataFrame `shows`

| Columna           | Tipo de Dato | Descripción                                         |
| ----------------- | ------------ | --------------------------------------------------- |
| id                | int          | Identificador único de la serie.                    |
| url               | object       | URL de la serie                                     |
| name              | object       | Nombre de la serie.                                 |
| type              | object       | Tipo de serie (`Scripted`, `Reality`, etc.).        |
| language          | object       | Idioma principal de la serie.                       |
| genres            | object       | Lista de géneros a los que pertenece la serie.      |
| status            | object       | Estado de la serie (`Running`, `Ended`, etc.).      |
| runtime           | float        | Duración típica de los episodios de la serie.       |
| averageRuntime    | float        | Duración promedio de los episodios.                 |
| premiered         | object       | Fecha de estreno de la serie.                       |
| ended             | object       | Fecha en que finalizó la serie (si aplica).         |
| officialSite      | object       | Sitio web oficial de la serie.                      |
| schedule_time     | object       | Hora en la que se transmite la serie.               |
| schedule_days     | object       | Días de la semana en los que se emite.              |
| rating            | float        | Calificación promedio de la serie en TVMaze.        |
| weight            | int          | Relevancia de la serie en la plataforma.            |
| summary           | object       | Breve descripción de la serie.                      |
| webChannel_name   | object       | Nombre de la plataforma de transmisión si aplica.   |
| webChannel_site   | object       | Sitio web de la plataforma de transmisión.          |
| dvd_country       | object       | País de origen del DVD de la serie.                 |
| externals_tvrage  | float        | Identificador de la serie en TVRage.                |
| externals_thetvdb | float        | Identificador de la serie en TheTVDB.               |
| externals_imdb    | object       | Identificador de la serie en IMDb.                  |
| updated           | int          | Última actualización de la información de la serie. |

## Análisis de Calidad de Datos

### 1. Valores Nulos

En el DataFrame de **Episodios**, el **14.1%** de los valores son nulos, estas son las columnas con mayor concentración de estos valores nulos:

- **rating**: 92.5% de valores nulos.
- **airtime**: 51.7% de valores nulos.
- **runtime**: 9.6% de valores nulos.
- **number**: 0.8% de valores nulos.

Por otro lado, en el DataFrame **Shows**, el **29,6%** de los valores son nulos y sus columnas con mayor concentración de valores nulos son:

- **dvd_country**: 99.6% de valores nulos.
- **externals_tvrage**: 96.8% de valores nulos.
- **rating**: 82.2% de valores nulos.
- **runtime**: 78.4% de valores nulos.
- **ended**: 75.0% de valores nulos.
- **schedule_time**: 67.8% de valores nulos.
- **externals_imdb**: 48.6% de valores nulos.
- **genres**: 35.7% de valores nulos.
- **schedule_days**: 30.6% de valores nulos.
- **externals_thetvdb**: 28.0% de valores nulos.
- **webChannel_site**: 26.6% de valores nulos.
- **summary**: 13.6% de valores nulos.
- **officialSite**: 11.3% de valores nulos.
- **averageRuntime**: 8.1% de valores nulos.
- **language**: 6.4% de valores nulos.
- **webChannel_name**: 2.8% de valores nulos.

Posibles acciones:

- La columna `rating` tiene demasiados valores nulos, por lo que podría eliminarse, sin embargo antes de eliminar una columna es muy importante revisar los efectos que tendría a la hora de hacerlo ya que puede que se necesite para posteriores análisis.
- `number` tiene pocos valores nulos y, en algunos casos, puede inferirse a partir del nombre del episodio.
- `runtime` tiene un porcentaje moderado de valores nulos, por lo que podría imputarse con la media o la mediana.
- `airtime` también tiene un alto porcentaje de valores faltantes, lo que dificulta su imputación.
- Se observa que `dvd_country` y `externals_tvrage` tienen un porcentaje muy alto de valores nulos y podrían eliminarse de no requerirse para posteriores procesos de análisis.
- `ended` y `schedule_time` tienen más del 50% de valores nulos, por lo que habría que analizar como se procesan.
- `genres` será requerida para próximos procesos de análisis, sin embargo es una lista dentro de una celda, lo que viola la 1NF (Primera Forma Normal). Se extraerá en un nuevo DataFrame para normalizar la relación.
- `language` y `webChannel_name` tienen menos del 10% de valores nulos, por lo que podrían imputarse con su valor más frecuente sin afectar demasiado la calidad de los datos.



### 2. Distribución de datos

- La columna **type** está **fuertemente desbalanceada**, ya que casi el 99% de los valores son "regular".
- Algunas columnas numéricas como `season` y `runtime` presentan coeficientes de variación un porcentaje bastante alto (cercanos o mayores al 100%) lo cual permite evidenciar que no hay un patrón identificable para este tipo de variables y que sus datos están altamente dispersos
- Para los datos de tipo date o time no se encontraron valores extremos como fechas mayores a la actual ni nada que evidencie un posible error
- Se observa una gran cantidad de contenido en inglés, aproximadamente el 39% de los shows

Posibles acciones:

- Se pueden revisar a detalle algunos de esos outliers que causaron una gran dispersión en los datos, ya que en ocasiones este tipo de análisis permite detectar errores o patrones inesperados.
- `rating` tiene muchos valores nulos, su distribución no lleva un patrón definido y no se va a requerir en el análisis, por lo que eliminarla sería una buena alternativa

### 3.colinealidad

- A la hora de revisar la matriz de correlaciones se puede ver que hay un alto valor (0,993) entre runtime y el averageRuntime para el dataframe de Shows, esto a futuro puede representar problemas en modelos de Machine Learning y en otros análisis estadísticos ya que hace que las variables aporten información redundante

Posibles acciones:

- A futuro se puede eliminar alguna de estas dos variables porque la información que aportan es redundante, preferiblemente runtime, por su alto porcentaje de valores nulos

### 4. cardinalidad

- Hay columnas de baja cardinalidad, con pocos valores únicos como lo es la columna `status`, ya que solo posee 3 tipos de valores, "Running", "Ended" o "Canceled. También se puede identificar valores de una Alta cardinalidad como lo son las URLs, ID y nombres
- Para la columna genre no fue posible el análisis de cardinalidad ya que contiene combinaciones en formato lista, lo que limitó su análisis

### 5. conclusiones

Se pudo evidenciar un conjunto de datos con información bastante detallada de show y episodios de la plataforma, tal vez a futuro con un mayor volumen de datos y un proceso elaborado de Extracción, Transformación y Carga sirva de gran utilidad para construir reportes para el equipo de mantenimiento de la plataforma, creación de modelos de Machine Learning con estrategias de recomendación de contenido para mejorar la experiencia de usuario, entre otros.

También se pudo ver que es muy importante tener en cuenta variables como la correlación, varianza y otros coeficientes estadísticos, ya que dan un panorama muy claro de cómo están distribuidos los datos, adicional a esto tomar decisiones basados en el análisis, con el objetivo de optimizar el manejo de memoria con información que no sea redudndante y que a futuro pueda ser procesada para obtener insights valiosos para diferentes públicos.

Se sugieren acciones para facilitar el procesamiento futuro de los datos, basados en cantidad de valores nulos, cardinalidad de los datos, colinealidad y su importancia para responder preguntas requeridas:

- Eliminar la columna `rating` de ambos dataframes
- `genres` será extraída a un nuevo DataFrame para normalizar su relación con `shows` y responder futuras preguntas.
- Eliminar la columna runtime del DataFrame Shows por su alto porcentaje de valores nulos y su colinealidad con la columna averageRuntime
- Eliminar las columnas dvd_country y externals_tvrage, ya que tienen más del 95% de valores nulos y no se requieren en el análisis actual.
