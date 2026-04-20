CREATE DATABASE IF NOT EXISTS BD_FIFA;
USE BD_FIFA;

CREATE TABLE IF NOT EXISTS usuarios (
ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
nombre VARCHAR(100) NOT NULL,
email VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS partidos (
ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
equipo_local VARCHAR(100) NOT NULL,
equipo_visitante VARCHAR(100) NOT NULL,
fecha DATETIME NOT NULL,
fase VARCHAR(50) NOT NULL,
goles_local INT DEFAULT NULL, -- todavía no se jugó
goles_visitante INT DEFAULT NULL 
);

CREATE TABLE IF NOT EXISTS predicciones (
ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
id_usuario INT NOT NULL,
id_partido INT NOT NULL,
goles_local INT NOT NULL,
goles_visitante INT NOT NULL,
FOREIGN KEY (id_usuario) REFERENCES usuarios(id) ON DELETE CASCADE, -- no podes cargar una predicción para un id_usuario para un usuario que no existe 
FOREIGN KEY (id_partido) REFERENCES partidos(id) ON DELETE CASCADE, -- si se elimina un usuario, se elimina su predicción
UNIQUE KEY uq_unica_prediccion (id_usuario, id_partido) -- solo se permite una predicción por usuario por partido
);
