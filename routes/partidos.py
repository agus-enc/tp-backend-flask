from flask import Blueprint, jsonify, request
from db import get_connection
from paginacion import generar_links_paginacion

partidos_bp = Blueprint("partidos", __name__)

@partidos_bp.route("", methods=["GET"])
def listar_partidos():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        limite = request.args.get('_limit', 10, type=int)  # Tomo los argumentos para la paginacion
        offset = request.args.get('_offset', 0, type=int)

        cursor.execute("""
            SELECT id, equipo_local, equipo_visitante, fecha, fase
            FROM partidos
            LIMIT %s OFFSET %s;
        """, (limite, offset))
        partidos = cursor.fetchall()

        cursor.execute("""
            SELECT COUNT(*) AS total FROM partidos;
        """)
        resultado = cursor.fetchone()
        total_registros = resultado['total']

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
            
@partidos_bp.route("/<int:id>", methods=["PUT"])
def modificar_partidos(id):
    datos = request.get_json()
    equipo_local = datos.get("equipo_local")
    equipo_visitante = datos.get("equipo_visitante")
    fecha = datos.get("fecha")
    if not equipo_local or not equipo_visitante or not fecha:
        return jsonify({"error" : "Faltan datos obligatorios"}), 400
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """UPDATE partidos
            SET equipo_local = %s, equipo_visitante = %s, fecha = %s
            WHERE id = %s
            """, (equipo_local, equipo_visitante, fecha, id)
        )
        
        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            return jsonify({"error" : "Partido no encontrado"}), 404
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"mensaje" : "Partido actualizado correctamente"}), 200
    
    except Exception as e:
        return jsonify({"error" : str(e)}), 500
    

@partidos_bp.route("/patidos/<int:id>/resultado", methods=['PUT'])
def actualizar_resultado(id):
    data = request.get_json()
    goles_local = data.get("local")
    goles_visitante = data.get("visitante")

    if goles_local is None or goles_visitante is None:
        return jsonify({"error":"Datos incompletos"}), 400
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """UPDATE partidos
            SET goles_local = %s, goles_visitante = %s
            WHERE id = %s
            """, (goles_local,goles_visitante,id)
        )
        
        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            return jsonify ({"error":"Partido no encontrado"}), 404
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"mensaje":"Resultados actualizados con exito"}), 200
    except Exception as e:
        return jsonify({"error":str(e)}), 500



