#!/bin/bash

# 1. Crear las tablas en MySQL (Si no existen)
echo "Ejecutando init_db.py para crear la estructura..."
python init_db.py

# 2. Llenar la base con Dummy Data
echo "Ejecutando datos.py para cargar datos de prueba..."
python datos.py

# 3. Levantar la API de Flask
echo "Levantando el servidor Flask..."
export FLASK_APP=app.py
export FLASK_ENV=development # Para tener hot-reload si cambias algo
flask run