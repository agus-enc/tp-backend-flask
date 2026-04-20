# seed.py
from db import get_connection

def poblar_base_de_datos():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        print("Limpiando base de datos...")
        # Desactivamos temporalmente las llaves foráneas para poder vaciar las tablas
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        cursor.execute("TRUNCATE TABLE predicciones;")
        cursor.execute("TRUNCATE TABLE partidos;")
        cursor.execute("TRUNCATE TABLE usuarios;")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

        print("Insertando usuarios de prueba...")
        usuarios = [
            ("Jose Gonzalez", "jo.gonzalez@afa.com"),
            ("Juan Lopez", "jlopez@fi.uba.ar"),
            ("Pedro Valdéz", "pvaldez@fi.uba.ar"),
            ("Carla Simone", "csimone@fi.uba.ar"),
            ("Franco Lomba", "flomba@fi.uba.ar "),
            ("Juana Pola", "jpola@fi.uba.ar" ),
            ("Lucia Fernandez", "lfernandez@fi.uba.ar"),
        ]
        cursor.executemany("INSERT INTO usuarios (nombre, email) VALUES (%s, %s)", usuarios)

        print("Insertando partidos (Pasados y Futuros)...")
        partidos = [
            ("Argentina", "Francia", "2022-12-18 12:00:00", "Final", "Lusail", "Doha", 3, 3),
            ("Brasil", "Croacia", "2022-12-09 12:00:00", "Cuartos", "Education City", "Al Rayyan", 1, 1),
            ("España", "Alemania", "2026-07-10 16:00:00", "Semifinal", "MetLife", "New York", None, None),
            ("Uruguay", "Colombia", "2026-06-25 19:00:00", "Grupos", "Hard Rock", "Miami", None, None)
        ]
        cursor.executemany(
            "INSERT INTO partidos (equipo_local, equipo_visitante, fecha, fase, estadio, ciudad, goles_local, goles_visitante) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            partidos
        )

        print("Insertando predicciones de prueba...")
        predicciones = [
            (1, 1, 3, 3),
            (2, 3, 2, 1),
            (3, 2, 1, 3),
            (2, 4, 2, 1),
            (4, 1, 0, 1),
        ]
        cursor.executemany(
            "INSERT INTO predicciones (id_usuario, id_partido, goles_local, goles_visitante) VALUES (%s, %s, %s, %s)",
            predicciones
        )

        conn.commit()
        print("¡Base de datos poblada con éxito!")

    except Exception as e:
        print(f"❌ Error al poblar la base de datos: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

if __name__ == "__main__":
    poblar_base_de_datos()