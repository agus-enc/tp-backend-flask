from flask import Blueprint, jsonify, request
from db import get_connection
from paginacion import generar_links_paginacion

partidos_bp = Blueprint("partidos", __name__)

@partidos_bp.route("", methods=["GET"])
def listar_partidos():
    try:
        conn = get_connection()   # Creo la conexion
        cursor = conn.cursor(dictionary=True)   # Creo el cursor que ejecuta los comandos dentro de la bd
        limite = request.args.get('_limit', 10, type=int)  # Tomo los argumentos para la paginacion
        offset = request.args.get('_offset', 0, type=int)
        equipo = request.args.get('equipo')  # Parametros opcionales sin default
        fecha = request.args.get('fecha')
        fase = request.args.get('fase')

        # Armo los queries base a los que agrego dinamicamente los demas parametros luego si existen
        query_general_base = "SELECT id, equipo_local, equipo_visitante, fecha, fase FROM partidos" # Toma los campos que necesita de la bd de la tabla de partidos
        query_count_base = "SELECT COUNT(*) AS total FROM partidos" # Cuenta todos los partidos

        condiciones = []   # Armo lista para guardar los comandos sql par aluego sumarlas al query base y armar el query final
        parametros = []  # Aca guardo las condiciones que vengan en la url, si es que vienen

        if equipo:
            condiciones.append("(equipo_local = %s OR equipo_visitante = %s)")
            parametros.append(equipo)
            parametros.append(equipo)  # Lo agrego dos veces porque hay dos %s y el conector lo lee en orden, matcheando 1 a 1

        if fecha: # Si existe el parametro fecha en la url, agrega la condicion a la lista de comandos sql a ejecutar dentro del where y el parametro en si a la lista de parametros a remplazar en los %s
            condiciones.append("DATE(fecha) = %s")
            parametros.append(fecha)

        if fase:
            condiciones.append("fase = %s")
            parametros.append(fase)

        if condiciones: # Si la lista de condiciones tiene al menos un filtro, lo suma al query base para armar el final
            clausula_where = " WHERE " + " AND ".join(condiciones)
            query_general_base += clausula_where
            query_count_base += clausula_where

        query_final = query_general_base + " LIMIT %s OFFSET %s"
        parametros_con_paginacion = parametros + [limite, offset]

        cursor.execute(query_final, tuple(parametros_con_paginacion))  # Los transformo a tuplas por posibles errores de tipo
        partidos = cursor.fetchall()

        cursor.execute(query_count_base, tuple(parametros))  # Calculo la cantidad total de partidos para usarlos en el last de la paginacion
        resultado = cursor.fetchone()
        total_registros = resultado['total']

        links = generar_links_paginacion(   # Usando la funcion de paginacion genero un diccionario con los links
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