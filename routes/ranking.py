from flask import Blueprint, jsonify, request
from db import get_connection
from funciones import generar_links_paginacion, formatear_errores

ranking_bp = Blueprint("ranking", __name__)

@ranking_bp.route('', methods=['GET'])
def get_ranking():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True) 

        limite_str = request.args.get('_limit')
        offset_str = request.args.get('_offset')

        if limite_str: 
            if limite_str.isdigit() and int(limite_str) > 0: 
                limit = int(limite_str)
            else:
                return formatear_errores(400, "Bad Request", "El parámetro _limit debe ser un número entero positivo."), 400
        else: limit = 10 

        if offset_str: 
            if offset_str.isdigit(): 
                offset = int(offset_str) 
            else: 
                return formatear_errores(400, "Bad Request", "El parámetro _offset debe ser un número entero positivo."), 400 
        else: offset = 0 

        # Cantidad de personas en el ranking para generar_links_paginacion
        cursor.execute("SELECT COUNT(DISTINCT id_usuario) as total FROM predicciones") 
        resultado_total = cursor.fetchone() 
        total_usuarios = resultado_total['total'] if resultado_total else 0

        sql = """
            SELECT u.id_usuario, 
                SUM(
                    CASE 
                        WHEN p.goles_local=pr.goles_local AND p.goles_visitante=pr.goles_visitante THEN 3
                        WHEN SIGN(p.goles_local-p.goles_visitante)=SIGN(pr.goles_local-pr.goles_visitante) THEN 1
                        ELSE 0 
                    END
                ) AS puntos
            FROM usuarios u 
            JOIN predicciones pr ON u.id_usuario=pr.id_usuario
            JOIN partidos p ON pr.id_partido=p.id_partido
            WHERE p.goles_local IS NOT NULL AND p.goles_visitante IS NOT NULL
            GROUP BY u.id_usuario
            ORDER BY puntos DESC 
            LIMIT %s OFFSET %s
            """
            
        cursor.execute(sql, (limit, offset))
        ranking_data = cursor.fetchall()

        links = generar_links_paginacion(
            base_url=request.base_url,
            limite=limit,
            desplazamiento=offset,
            total_registros=total_usuarios,
            args_actuales=request.args.to_dict()
        )

        return jsonify({
            "data": ranking_data,
            "_links": links
        }), 200

    except Exception as error:
        print(error)
        return formatear_errores(500, "Internal Server Error", "Problema inesperado en el servidor"), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()