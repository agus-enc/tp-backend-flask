from flask import Blueprint, jsonify, request
from db import get_connection
from funciones import generar_links_paginacion, formatear_errores, es_fecha_valida
from datetime import datetime
from mysql.connector.errors import IntegrityError

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

@partidos_bp.route("", methods=["POST"])
def crear_partido():
    datos = request.get_json()
    equipo_local = datos.get("equipo_local")
    equipo_visitante = datos.get("equipo_visitante")
    fecha = datos.get("fecha")
    fase = datos.get("fase")

    if not all([equipo_local, equipo_visitante, fecha, fase]):
        return formatear_errores(400, "Bad Request", "Faltan datos obligatorios"), 400

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO partidos (equipo_local, equipo_visitante, fecha, fase)
            VALUES (%s, %s, %s, %s)
        """, (equipo_local, equipo_visitante, fecha, fase))
        
        conn.commit()
        return jsonify({"mensaje": "Partido creado exitosamente"}), 201

    except Exception as error:
        print(error)
        return formatear_errores(500, "Internal Server Error", "Problema inesperado en el servidor"), 500

    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

@partidos_bp.route('/<int:id>', methods=['GET'])
def obtener_partido(id):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        sql = "SELECT * FROM partidos WHERE id = %s"
        cursor.execute(sql, (id,))
        partido = cursor.fetchone()

        partido['fecha'] = partido['fecha'].strftime('%Y-%m-%d')

        if not partido:
            return formatear_errores(404, "Not Found", f"No se encontró el partido con ID {id}"), 404
        return jsonify(partido), 200

    except Exception as error:
        print(error)
        return formatear_errores(500, "Internal Server Error", "Problema inesperado en el servidor"), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


@partidos_bp.route("/<int:id>", methods=["PUT"])
def modificar_partidos(id):
    conn = None
    cursor = None

    datos = request.get_json()
    equipo_local = datos.get("equipo_local")
    equipo_visitante = datos.get("equipo_visitante")
    fecha = datos.get("fecha")

    if not equipo_local or not equipo_visitante or not fecha:
        return formatear_errores(400, "Bad Request", "Faltan datos obligatorios"), 400

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            UPDATE partidos
            SET equipo_local = %s, equipo_visitante = %s, fecha = %s
            WHERE id = %s
            """, (equipo_local, equipo_visitante, fecha, id)
        )
        
        if cursor.rowcount == 0:
            return formatear_errores(404, "Not Found", "Partido no encontrado"), 404
        conn.commit()

        return jsonify({"mensaje" : "Partido actualizado correctamente"}), 200
    
    except Exception as e:
        print(e)
        return formatear_errores(500, "Internal Server Error", "Problema inesperado en el servidor"), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@partidos_bp.route("/<int:id>/resultado", methods=['PUT'])
def actualizar_resultado(id):
    conn = None
    cursor = None

    data = request.get_json()
    goles_local = data.get("local")
    goles_visitante = data.get("visitante")

    if goles_local is None or goles_visitante is None:
        return formatear_errores(400, "Bad Request", "Datos Incompletos"), 400
    
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
            return formatear_errores(404, "Not Found", "Partido no encontrado"), 404

        conn.commit()
        
        return jsonify({"mensaje":"Resultados actualizados con exito"}), 200

    except Exception as e:
        print(e)
        return formatear_errores(500, "Internal Server Error", "Problema inesperado en el servidor"), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@partidos_bp.route("/<int:id>", methods=["PATCH"])
def actualizar_partido(id):
    conn = None
    cursor = None

    data = request.get_json()
    
    equipo_local = data.get("equipo_local")
    equipo_visitante = data.get("equipo_visitante")
    fecha = data.get("fecha")
    fase = data.get("fase")

    if equipo_local is None and equipo_visitante is None and fecha is None and fase is None:
        return formatear_errores(400, "Bad Request", "No se enviaron datos para actualizar"), 400
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        if equipo_local:
            cursor.execute("UPDATE partidos SET equipo_local = %s WHERE id = %s", (equipo_local, id))
            
        if equipo_visitante:
            cursor.execute("UPDATE partidos SET equipo_visitante = %s WHERE id = %s", (equipo_visitante, id))
            
        if fecha:
            cursor.execute("UPDATE partidos SET fecha = %s WHERE id = %s", (fecha, id))
            
        if fase:
            cursor.execute("UPDATE partidos SET fase = %s WHERE id = %s", (fase, id))

        conn.commit()

        if cursor.rowcount == 0:
            cursor.execute("SELECT id FROM partidos WHERE id = %s", (id,))
            if not cursor.fetchone():
                return formatear_errores(404, "Not Found", "Partido no encontrado"), 404
        
        return jsonify({"mensaje": "Partido actualizado con éxito"}), 200
        
    except Exception as e:
        print(e)
        return formatear_errores(500, "Internal Server Error", "Problema inesperado en el servidor"), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@partidos_bp.route("/<int:id>/prediccion", methods=["POST"])
def registrar_prediccion(id):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        datos = request.get_json(silent=True)

        if not datos:
            return formatear_errores(400, "Bad Request", "El cuerpo de la petición debe ser un JSON válido."), 400

        id_usuario = datos.get('id_usuario')
        goles_local = datos.get('local')
        goles_visitante = datos.get('visitante')

        if id_usuario is None or goles_local is None or goles_visitante is None:
            return formatear_errores(400, "Bad Request","Falta uno o mas campos obligatorios."), 400

        if not isinstance(id_usuario, int):
            return formatear_errores(400, "Bad Request", "El id del usuario debe ser un número."), 400

        if not isinstance(goles_local, int) or not isinstance(goles_visitante, int) or goles_local < 0 or goles_visitante < 0:
            return formatear_errores(400, "Bad Request", "Los goles deben ser números enteros positivos o cero."), 400

        cursor.execute("SELECT fecha FROM partidos WHERE id = %s", (id,))
        partido = cursor.fetchone()

        if not partido:
            return formatear_errores(404, "Not Found", "El partido no existe."), 404

        if partido['fecha'] <= datetime.now():
            return formatear_errores(400, "Bad Request","El partido ya se jugó o ya comenzó. No se admiten predicciones."), 400

        cursor.execute(
            """
            SELECT COUNT(*) AS total_predicciones
            FROM predicciones
            WHERE id_usuario = %s AND id_partido = %s
            """, (id_usuario, id)
        )
        resultado = cursor.fetchone()

        if resultado['total_predicciones'] > 0:
            return formatear_errores(400, "Bad Request", "El usuario ya realizó una predicción para este partido."), 409

        cursor.execute(
            """
            INSERT into predicciones (id_usuario, id_partido, goles_local, goles_visitante) VALUES (%s, %s, %s, %s)
            """, (id_usuario, id, goles_local, goles_visitante)
        )
        conn.commit()
        return "", 201

    except IntegrityError as error:
        # Si el error es por la llave foránea del usuario
        return formatear_errores(400, "Bad Request", "El usuario especificado no existe."), 400

    except Exception as error:
        print(error)
        return formatear_errores(500, "Internal Server Error", "Problema inesperado en el servidor"), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@partidos_bp.route('/<int:id>', methods=['DELETE'])
def borrar_partido(id):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("DELETE FROM partidos WHERE id = %s", (id,))

        if cursor.rowcount == 0:
            return formatear_errores(404, "Not Found", "El partido no existe."), 404

        conn.commit()

        return '', 204

    except Exception as error:
        print(error)
        return formatear_errores(500, "Internal Server Error", "Problema inesperado en el servidor"), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()