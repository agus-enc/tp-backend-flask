from flask import Blueprint, jsonify, request
from db import get_connection
from paginacion import generar_links_paginacion

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