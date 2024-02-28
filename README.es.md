# Plantilla de Proyecto de Ciencia de Datos

Esta plantilla está diseñada para impulsar proyectos de ciencia de datos proporcionando una configuración básica para conexiones de base de datos, procesamiento de datos, y desarrollo de modelos de aprendizaje automático. Incluye una organización estructurada de carpetas para tus conjuntos de datos y un conjunto de paquetes de Python predefinidos necesarios para la mayoría de las tareas de ciencia de datos.

## Estructura

El proyecto está organizado de la siguiente manera:

- `app.py` - El script principal de Python que ejecutas para tu proyecto.
- `explore.py` - Un notebook para que puedas hacer tus exploraciones, idealmente el codigo de este notebook se migra hacia app.py para subir a produccion.
- `utils.py` - Este archivo contiene código de utilidad para operaciones como conexiones de base de datos.
- `requirements.txt` - Este archivo contiene la lista de paquetes de Python necesarios.
- `models/` - Este directorio debería contener tus clases de modelos SQLAlchemy.
- `data/` - Este directorio contiene los siguientes subdirectorios:
  - `interim/` - Para datos intermedios que han sido transformados.
  - `processed/` - Para los datos finales a utilizar para el modelado.
  - `raw/` - Para datos brutos sin ningún procesamiento.

## Configuración

**Prerrequisitos**

Asegúrate de tener Python 3.11+ instalado en tu máquina. También necesitarás pip para instalar los paquetes de Python.

**Instalación**

Clona el repositorio del proyecto en tu máquina local.

Navega hasta el directorio del proyecto e instala los paquetes de Python requeridos:

```bash
pip install -r requirements.txt
```

**Crear una base de datos (si es necesario)**

Crea una nueva base de datos dentro del motor Postgres personalizando y ejecutando el siguiente comando: `$ createdb -h localhost -U <username> <db_name>`
Conéctate al motor Postgres para usar tu base de datos, manipular tablas y datos: `$ psql -h localhost -U <username> <db_name>`
NOTA: Recuerda revisar la información del archivo ./.env para obtener el nombre de usuario y db_name.

¡Una vez que estés dentro de PSQL podrás crear tablas, hacer consultas, insertar, actualizar o eliminar datos y mucho más!

**Variables de entorno**

Crea un archivo .env en el directorio raíz del proyecto para almacenar tus variables de entorno, como tu cadena de conexión a la base de datos:

```makefile
DATABASE_URL="your_database_connection_url_here"
```

## Ejecutando la Aplicación

Para ejecutar la aplicación, ejecuta el script app.py desde la raíz del directorio del proyecto:

```bash
python app.py
```

## Añadiendo Modelos

Para añadir clases de modelos SQLAlchemy, crea nuevos archivos de script de Python dentro del directorio models/. Estas clases deben ser definidas de acuerdo a tu esquema de base de datos.

Definición del modelo de ejemplo (`models/example_model.py`):

```py
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class ExampleModel(Base):
    __tablename__ = 'example_table'
    id = Column(Integer, primary_key=True)
    name = Column(String)

```

## Trabajando con Datos

Puedes colocar tus conjuntos de datos brutos en el directorio data/raw, conjuntos de datos intermedios en data/interim, y los conjuntos de datos procesados listos para el análisis en data/processed.

Para procesar datos, puedes modificar el script app.py para incluir tus pasos de procesamiento de datos, utilizando pandas para la manipulación y análisis de datos.

## Contribuyentes

Esta plantilla fue construida como parte del [Data Science and Machine Learning Bootcamp](https://4geeksacademy.com/us/coding-bootcamps/datascience-machine-learning) de 4Geeks Academy por [Alejandro Sanchez](https://twitter.com/alesanchezr) y muchos otros contribuyentes. Descubre más sobre [los programas BootCamp de 4Geeks Academy](https://4geeksacademy.com/us/programs) aquí.

Otras plantillas y recursos como este se pueden encontrar en la página de GitHub de la escuela.