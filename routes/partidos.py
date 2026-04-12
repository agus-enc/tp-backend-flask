from flask import Blueprint, jsonify, request
from db import get_connection
from paginacion import generar_links_paginacion

partidos_bp = Blueprint("partidos", __name__)

@partidos_bp.route("/", methods=["GET"])
def listar_partidos():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        limite = request.args.get('_limit', 10, type=int)
        offset = request.args.get('_offset', 0, type=int)

        cursor.execute("""
            SELECT id, equipo_local, equipo_visitante, fecha, fase
            FROM partidos
            LIMIT %s OFFSET %s;
        """, (limite, offset))
        partidos = cursor.fetchall()

        cursor.execute("""
            SELECT COUNT(*) FROM partidos;
        """)
        total_registros = cursor.fetchone()[0]

        links = generar_links_paginacion(
            base_url=request.base_url,
            limite=limite,
            desplazamiento=offset,
            total_registros=total_registros
        )

        return jsonify({
            "partidos": partidos,
            "_links": links
        }), 200

    except Exception as error:
        print(error)
        return jsonify({"error": "Error al obtener los partidos"}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()