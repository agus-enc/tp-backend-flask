from flask import Blueprint, jsonify, request
from db import get_connection
from funciones import generar_links_paginacion, formatear_errores, es_fecha_valida

partidos_bp = Blueprint("partidos", __name__)

@partidos_bp.route("", methods=["GET"])
def listar_partidos():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        limite_str = request.args.get('_limit')
        offset_str = request.args.get('_offset')

        if limite_str:
            if limite_str.isdigit() and int(limite_str) > 0:
                limite = int(limite_str)
            else:
                return formatear_errores(400, "Bad Request", "El parámetro _limit debe ser un número entero positivo."), 400
        else:
            limite = 10

        if offset_str:
            if offset_str.isdigit():
                offset = int(offset_str)
            else:
                return formatear_errores(400, "Bad Request", "El parámetro _offset debe ser un número entero positivo."), 400
        else:
            offset = 0

        equipo = request.args.get('equipo')  # Parametros opcionales sin default
        fecha = request.args.get('fecha')
        fase = request.args.get('fase')

        query_general_base = "SELECT id, equipo_local, equipo_visitante, fecha, fase FROM partidos"
        query_count_base = "SELECT COUNT(*) AS total FROM partidos"

        condiciones = []
        parametros = []

        if equipo:
            condiciones.append("(equipo_local = %s OR equipo_visitante = %s)")
            parametros.append(equipo)
            parametros.append(equipo)  # Lo agrego dos veces porque hay dos %s y el conector lo lee en orden, matcheando 1 a 1

        if fecha:
            if es_fecha_valida(fecha):
                condiciones.append("DATE(fecha) = %s")
                parametros.append(fecha)
            else:
                return formatear_errores(400, "Bad Request", "La fecha debe tener el formato YYYY-MM-DD y ser válida."), 400

        if fase:
            condiciones.append("fase = %s")
            parametros.append(fase)

        if condiciones:
            clausula_where = " WHERE " + " AND ".join(condiciones)
            query_general_base += clausula_where
            query_count_base += clausula_where

        query_final = query_general_base + " LIMIT %s OFFSET %s"
        parametros_con_paginacion = parametros + [limite, offset]

        cursor.execute(query_count_base, tuple(parametros))
        resultado = cursor.fetchone()
        total_registros = resultado['total']

        if offset > total_registros:
            return formatear_errores(404, "Not Found", "Pagina fuera de rango"), 404

        cursor.execute(query_final, tuple(parametros_con_paginacion))
        partidos = cursor.fetchall()

        if not partidos:
            return "", 204

        for partido in partidos:
            partido['fecha'] = partido['fecha'].strftime('%Y-%m-%d')

        links = generar_links_paginacion(
            base_url = request.base_url,
            limite = limite,
            desplazamiento = offset,
            total_registros = total_registros,
            args_actuales = request.args.to_dict()
        )

        return jsonify({
            "partidos": partidos,
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