# Plantilla de Proyecto de Ciencia de Datos

Esta plantilla está diseñada para impulsar proyectos de ciencia de datos proporcionando una configuración básica para conexiones de base de datos, procesamiento de datos, y desarrollo de modelos de aprendizaje automático. Incluye una organización estructurada de carpetas para tus conjuntos de datos y un conjunto de paquetes de Python predefinidos necesarios para la mayoría de las tareas de ciencia de datos.

## Estructura

El proyecto está organizado de la siguiente manera:

- **`src/app.py`** → Script principal de Python donde correrá tu proyecto.
- **`src/explore.ipynb`** → Notebook para exploración y pruebas. Una vez finalizada la exploración, migra el código limpio a `app.py`.
- **`src/utils.py`** → Funciones auxiliares, como conexión a bases de datos.
- **`requirements.txt`** → Lista de paquetes de Python necesarios.
- **`models/`** → Contendrá tus clases de modelos SQLAlchemy.
- **`data/`** → Almacena los datasets en diferentes etapas:
  - **`data/raw/`** → Datos sin procesar.
  - **`data/interim/`** → Datos transformados temporalmente.
  - **`data/processed/`** → Datos listos para análisis.


## ⚡ Configuración Inicial en Codespaces (Recomendado)

No es necesario realizar ninguna configuración manual, ya que **Codespaces se configura automáticamente** con los archivos predefinidos que ha creado la academia para ti. Simplemente sigue estos pasos:

1. **Espera a que el entorno se configure automáticamente**.
   - Todos los paquetes necesarios y la base de datos se instalarán por sí mismos.
   - El `username` y `db_name` creados automáticamente están en el archivo **`.env`** en la raíz del proyecto.
2. **Una vez que Codespaces esté listo, puedes comenzar a trabajar inmediatamente**.


## 💻 Configuración en Local (Solo si no puedes usar Codespaces)

**Prerrequisitos**

Asegúrate de tener Python 3.11+ instalado en tu máquina. También necesitarás pip para instalar los paquetes de Python.

**Instalación**

Clona el repositorio del proyecto en tu máquina local.

Navega hasta el directorio del proyecto e instala los paquetes de Python requeridos:

```bash
pip install -r requirements.txt
```

**Crear una base de datos (si es necesario)**

Crea una nueva base de datos dentro del motor Postgres personalizando y ejecutando el siguiente comando: 

```bash
$ psql -U postgres -c "DO \$\$ BEGIN 
    CREATE USER mi_usuario WITH PASSWORD 'mi_contraseña'; 
    CREATE DATABASE mi_base_de_datos OWNER mi_usuario; 
END \$\$;"
```
Conéctate al motor Postgres para usar tu base de datos, manipular tablas y datos: 

```bash
$ psql -U mi_usuario -d mi_base_de_datos
```

¡Una vez que estés dentro de PSQL podrás crear tablas, hacer consultas, insertar, actualizar o eliminar datos y mucho más!

**Variables de entorno**

Crea un archivo .env en el directorio raíz del proyecto para almacenar tus variables de entorno, como tu cadena de conexión a la base de datos:

```makefile
DATABASE_URL="postgresql://<USUARIO>:<CONTRASEÑA>@<HOST>:<PUERTO>/<NOMBRE_BD>"

#example
DATABASE_URL="postgresql://mi_usuario:mi_contraseña@localhost:5432/mi_base_de_datos"
```

## Ejecutando la Aplicación

Para ejecutar la aplicación, ejecuta el script app.py desde la raíz del directorio del proyecto:

```bash
python src/app.py
```

## Añadiendo Modelos

Para añadir clases de modelos SQLAlchemy, crea nuevos archivos de script de Python dentro del directorio models/. Estas clases deben ser definidas de acuerdo a tu esquema de base de datos.

Definición del modelo de ejemplo (`models/example_model.py`):

```py
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

Base = declarative_base()

class ExampleModel(Base):
    __tablename__ = 'example_table'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
```

## Trabajando con Datos

Puedes colocar tus conjuntos de datos brutos en el directorio data/raw, conjuntos de datos intermedios en data/interim, y los conjuntos de datos procesados listos para el análisis en data/processed.

Para procesar datos, puedes modificar el script app.py para incluir tus pasos de procesamiento de datos, utilizando pandas para la manipulación y análisis de datos.

## Contribuyentes

Esta plantilla fue construida como parte del [Data Science and Machine Learning Bootcamp](https://4geeksacademy.com/us/coding-bootcamps/datascience-machine-learning) de 4Geeks Academy por [Alejandro Sanchez](https://twitter.com/alesanchezr) y muchos otros contribuyentes. Descubre más sobre [los programas BootCamp de 4Geeks Academy](https://4geeksacademy.com/us/programs) aquí.

Otras plantillas y recursos como este se pueden encontrar en la página de GitHub de la escuela.

# Update

## Clasificación de perros y gatos con EfficientNet-B0

El objetivo de esta práctica es clasificar imágenes de perros y gatos. Se visualizaron las primeras nueve fotos de cada clase. Las imágenes originales eran a color y tenían distintas dimensiones y proporciones, por lo que se redimensionaron a 200 × 200 píxeles.

Las 25.000 imágenes etiquetadas se dividieron de forma estratificada en 20.000 para entrenamiento, 2.500 para validación y 2.500 para prueba. EfficientNet-B0 se entrenó desde cero. Se usó la pérdida de validación para seleccionar el mejor modelo y detener el entrenamiento cuando dejó de mejorar.

### Resultados

| Métrica | Resultado |
| --- | ---: |
| Mejor época según la pérdida de validación | 8 |
| Pérdida de validación en la mejor época | 0,2037 |
| Exactitud en prueba | 92,12 % |
| Pérdida en prueba | 0,2016 |
| Predicciones correctas en prueba | 2.303 de 2.500 |

El entrenamiento se detuvo en la época 13 tras cinco épocas consecutivas sin mejorar la pérdida de validación. Para obtener los resultados de prueba se recargó el modelo de la época 8.

### Cómo reproducir el entrenamiento

Desde la raíz del repositorio, con un entorno activo de Python 3.11:

```bash
python -m pip install "tensorflow>=2.16,<3" matplotlib pillow
python src/train_dogs_cats.py
```

El script guarda el mejor modelo en `models/dogs_vs_cats.keras`. En `data/processed/` guarda las dos cuadrículas de imágenes, `dogs_vs_cats_predictions.csv` y `dogs_vs_cats_metrics.json`.

## Agrupación de viviendas en California

Se usaron la latitud, la longitud y el ingreso mediano de 20.640 grupos de bloques censales. Se reservaron 16.512 registros para entrenamiento y 4.128 para prueba. Tras estandarizar las tres variables, se entrenó K-Means con seis clústeres y se asignó cada punto de prueba al centroide más cercano.

La silueta en prueba fue de **0,397**, lo que indica una separación moderada entre los grupos. Los clústeres 1 y 3 tienen centros geográficos cercanos, pero sus medianas de ingreso difieren (2,85 frente a 5,10 en las unidades del dataset). El gráfico usa solo longitud y latitud, por lo que parte de la separación por ingresos queda fuera de la vista.

El clasificador SVM lineal reprodujo las etiquetas de K-Means en **4.104 de 4.128** registros de prueba. Obtuvo **99,42 % de exactitud** y un **F1 macro de 0,992**. Estas métricas miden el acuerdo entre ambos modelos sobre los puntos de prueba.

El [gráfico de clústeres](california-housing/results/clusters.png) muestra los puntos de entrenamiento y de prueba. Las métricas y la matriz de confusión están en `california-housing/results/metrics.json`. Los dos modelos se guardaron en `california-housing/models/`.