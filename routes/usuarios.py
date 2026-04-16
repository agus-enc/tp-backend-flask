from flask import Blueprint, jsonify, request
from db import get_connection
from funciones import generar_links_paginacion

usuarios_bp = Blueprint("usuarios", __name__)

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
            return jsonify({"error": "Usuario no encontrado"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@usuarios_bp.route("/usuarios/<int:id>", methods=["DELETE"])
def eliminar_usuario(id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        #verifica si existe el id
        cursor.execute("SELECT id FROM usuarios WHERE id = %s, (id,)")
        usuario = cursor.fetchone()

        if not usuario:
            return jsonify({"error":"Usuario no encontrado"}), 404
        
        #borrar usuario
        cursor.execute("DELETE from usuarios WHERE id = %s, (id,)")
        conn.commit()
        cursor.close()
        conn.close()

        return '', 204
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

