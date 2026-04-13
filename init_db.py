import mysql.connector

with open("init_db.sql", encoding="utf-8") as file:    #el encoding es para evitar errores por caracteres especiales
    sql = file.read()

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root"
)

cursor = conn.cursor()

try:
    instrucciones = sql.split(";")
    for instruccion in instrucciones:
        instruccion = instruccion.strip()

        if instruccion:
            print(instruccion)
            cursor.execute(instruccion)

    conn.commit()
    print("Instrucción ejecutada")

except mysql.connector.Error as error:
    print(f"Error: {error}")
    conn.rollback()

finally:
    cursor.close()
    conn.close()