from flask import Blueprint, jsonify, request
from db import get_connection
from funciones import generar_links_paginacion, formatear_errores

usuarios_bp = Blueprint("usuarios", __name__)

@usuarios_bp.route("", methods=["GET"])
def listar_usuarios():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True) 
        # Contrato Swagger:
        limite = request.args.get('_limit', 10, type=int)
        offset = request.args.get('_offset', 0, type=int)

        cursor.execute("""
            SELECT id, nombre, email 
            FROM usuarios
            LIMIT %s OFFSET %s;
        """, (limite, offset))
        usuarios = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) AS total FROM usuarios;")
        total_registros = cursor.fetchone()['total']

        links = generar_links_paginacion(
            base_url=request.base_url,
            limite=limite,
            desplazamiento=offset,
            total_registros=total_registros,
            args_actuales = request.args.to_dict()
        )

        return jsonify({
            "usuarios": usuarios,
            "_links": links
        }), 200

    except Exception as error:
        print(error)
        return formatear_errores(500, "Internal Server Error", "Problema inesperado en el servidor"), 500

    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

@usuarios_bp.route("", methods=["POST"])
def crear_usuario():
    datos = request.get_json(silent=True)
    if not datos:
        return formatear_errores(400, "Bad Request", "Faltan datos obligatorios"), 400

    nombre = datos.get("nombre")
    email = datos.get("email")

    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO usuarios (nombre, email)
            VALUES (%s, %s)
        """, (nombre, email))
        
        conn.commit()
        nuevo_id = cursor.lastrowid # para conocer el nuevo ID creado 
        
        return jsonify({
            "id_usuario": nuevo_id,
            "mensaje": "Usuario creado exitosamente"
        }), 201

    except Exception as error:
        print(error)
        return formatear_errores(500, "Internal Server Error", "Problema inesperado en el servidor"), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@usuarios_bp.route("/<int:id>", methods=["GET"])
def obtener_usuario(id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, nombre, email FROM usuarios WHERE id = %s", (id,))
        usuario = cursor.fetchone() # Traigo uno solo
        
        cursor.close()
        conn.close()

        if usuario:
            return jsonify({
                "id": usuario[0],
                "nombre": usuario[1],
                "email": usuario[2]
            }), 200
        else:
            # Si fetchone() dio None, es porque no existe ese ID
            return formatear_errores(404, "Not Found", "Usuario no encontrado"), 404

    except Exception as e:
        print(e)
        return formatear_errores(500, "Internal Server Error", "Problema inesperado en el servidor"), 500

@usuarios_bp.route("/<int:id>", methods=["DELETE"])
def eliminar_usuario(id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        #verifica si existe el id
        cursor.execute("SELECT id FROM usuarios WHERE id = %s", (id,))
        usuario = cursor.fetchone()

        if not usuario:
            return formatear_errores(404, "Not Found", "Usuario no encontrado"), 404
        
        #borrar usuario
        cursor.execute("DELETE from usuarios WHERE id = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()

        return '', 200
    
    except Exception as e:
        print(e)
        return formatear_errores(500, "Internal Server Error", "Problema inesperado en el servidor"), 500

@usuarios_bp.route("/usuarios/<int:id>", methods=["PUT"])
def reemplazar_usuario(id):
    data = request.get_json()
    nombre = data.get("nombre")
    email = data.get("email")

    if nombre is None or email is None:
        return formatear_errores(400, "Bad Request", "Datos incompletos. Se requiere nombre y email"), 400
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """UPDATE usuarios
            SET nombre = %s, email = %s
            WHERE id = %s
            """, (nombre, email, id)
        )
        
        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            return formatear_errores(404, "Not Found", "Usuario no encontrado"), 404
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"mensaje": "Usuario actualizado con éxito"}), 200
        
    except Exception as e:
        print(e)
        return formatear_errores(500, "Internal Server Error", "Problema inesperado en el servidor"), 500