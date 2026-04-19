# Proyecto backend IDS
Este proyecto consiste en una API Rest desarrollada en **Python** utilizando **Flask** para la gestion de un Fixture y un sistema de pronósticos deportivos (Prode) para el mundial 2026.

Trabajo práctico para la materia **Introducción al desarrollo de Software**
## Descripción y Requerimientos
La API permite administrar los registros del mundial, registrar los resultados y gestionar las predicciones de los usuarios con un sistema de ranking automatizado.
## Tecnologias utilizadas
Cada integrante del grupo usó un entorno virtual para gestionar la creación del proyecto.  
-**Lenguaje**: Python 3.12

-**Framework**: Flask

-**Base de datos**: MySQL

## Estructura del proyecto


```text
tp-backend-flask/
├── routes/             # Blueprints con la lógica de los endpoints
│   ├── partidos.py     # Gestión de partidos y resultados
│   ├── ranking.py      # Lógica de calculo de posiciones
│   └── usuarios.py     # CRUD de usuarios y predicciones
├── git.ignore          # Archivos que git debe ignorar
├── app.py              # Servidor Flask
├── db.py               # Configuracion de conexion a la base de datos MySQL
├── funciones.py        # Funciones auxiliares
├── datos.py            # Llena la base de datos
├── init_db.py          # Inicializa la base de datos
├── init_db.sql         # Crea tablas dentro de la base de datos
└── start.sh            # Levanta el servidor
```
**-app.py**: Define las rutas (endpoints) de la API. Punto de entada que levanta el servidor.
**-funciones.py**: Contiene función de formateo de errores, función que genera links de paginación, función que verifica si la fecha ingresada por el usuario contiene el formato ocrrecto y una función que actualiza la paginación.

### Requisitos previos
Para ejecutar esta API se debe tener instalado Python.

## Instalación y Configuración
Para ejecutar la API en su entorno virtual se debe hacer lo siguiente:
### 1. Clonar el repositorio
```text
git clone <https://github.com/agus-enc/tp-backend-flask.git>
cd tp-backend-flask
```
### 2. Crear un entorno virtual
```text
python -m venv venv
source venv/bin/activate
```
### 3. Configurar la base de datos
```text
· Crear una base de datos en MySQL
· Ejecutar el script init_db.sql
· Configurar las credenciales en el archivo venv
```
### 4. Correr la API
Con el entorno virtual activo, ejecutá:
```
python app.py
```
Verás un mensaje en la consola indicando que el servidor está corriendo en ```http://127.0.0.1:5000```. Deja esta terminal abierta mientras usás la API.

## Endpoints disponibles
| Verbo HTTPS | Endpoint | Descripción | 
| :--- | :--- | :--- |
| **GET** | `/partidos`| Listar partidos |
| **POST** | `/partidos`| Crea un partido |
| **GET** | `/partidos/{id}`| Obtener un partido por id |
| **PUT** | `/partidos/{id}`| Reemplazar partidos |
| **PATCH** | `/partidos/{id}`| Actualizar parcialmente un partido |
| **DELETE** | `/partidos/{id}`| Eliminar partido |
| **PUT** | `/partidos/{id}/resultado`|Actualizar resultado |
| **POST** | `/partidos/{id}/prediccion`| Registrar una prediccion para un partido |
| **GET** | `/usuarios`| Listar usuarios |
| **POST** | `/usuarios`| Crear usuario |
| **GET** | `/usuarios/{id}`|Obtener usuario por id |
| **PUT** | `/usuarios/{id}`| Reemplazar un usuario |
| **DELETE** | `/usuarios/{id}`| Eliminar usuario |
| **GET** | `/Ranking`| Obtener el ranking de usuarios |

   
