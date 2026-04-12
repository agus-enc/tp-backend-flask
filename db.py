from mysql.connector import connect

def get_connection():
    return connect(
        host="localhost",
        user="root",
        password="root",
        database="BD_FIFA"
    )