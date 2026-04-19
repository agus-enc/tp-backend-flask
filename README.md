# Proyecto backend IDS
Este proyecto consiste en una API Rest desarrollada en **Python** utilizando **Flask** para la gestion de un Fixture y un sistema de pronósticos deportivos (Prode) para el mundial 2026.

Trabajo práctico para la materia **Introducción al desarrollo de Software**
## Descripción y Requerimientos
La API permite administrar los registros del mundial, registrar los resultados y gestionar las predicciones de los usuarios con un sistema de ranking automatizado.
## Tecnologias utilizadas
Cada integrante del grupo usó un entroeno virtual para gestionar el proyecto. Se 
-**Lenguaje** Python 3.12

-**Framework** Flask

-**Base de datos** MySQL

## Estructura del proyecto


```text
tp-backend-flask/
├── routes/             # Blueprints con la logica de los endpoints
│   ├── partidos.py     # Gestion de partidos y rresultados
│   ├── ranking.py      # Lógica de calculo de posiciones
│   └── usuarios.py     # CRUD de usuarios y predicciones
├── git.ignore          # Archivos que git debe ignorar
├── app.py              # Servidor Flask: define las rutas (endpoints) de la API. Punto de entrada  que levanta el servidor
├── db.py               # Configuracion de conexion a la base de datos MySQL
├── funciones.py        # Funciones auxiliares y formateo de errores
├── datos.py            # Llena la base de datos
├── init_db.py          # Inicializa la base de datos
├── init_db.sql         # Crea tablas dentro de la base de datos
└── start.sh            # levanta todo y llena la base de datos
```
### Requisitos previos
Para ejecutar esta API se debe tener instalado Python.

## Instalación y Configuración
Para ejecutar la API en su entorno virtual se debe hacer lo siguiente:
```text
git clone <
```

   
