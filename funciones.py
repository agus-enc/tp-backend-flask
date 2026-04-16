from urllib.parse import urlencode
from flask import jsonify
from datetime import datetime

def construir_url(base_url, args_actuales, limite, nuevo_offset):
    """
    Toma los parámetros actuales de la URL, actualiza la paginación,
    y devuelve la URL completa y segura.
    """
    params = args_actuales.copy()
    params['_limit'] = limite
    params['_offset'] = nuevo_offset
    return f"{base_url}?{urlencode(params)}"

def generar_links_paginacion(base_url, limite, desplazamiento, total_registros, args_actuales):
    """
    Calcula y devuelve un diccionario con los enlaces HATEOAS para la paginación.
    """
    enlaces = {}

    # 1. Primera página
    enlaces["_first"] = {"href": construir_url(base_url, args_actuales, limite, 0)}

    # 2. Página anterior
    if desplazamiento > 0:
        offset_prev = max(0, desplazamiento - limite)
        enlaces["_prev"] = {"href": construir_url(base_url, args_actuales, limite, offset_prev)}

    # 3. Página siguiente
    if desplazamiento + limite < total_registros:
        offset_next = desplazamiento + limite
        enlaces["_next"] = {"href": construir_url(base_url, args_actuales, limite, offset_next)}

    # 4. Última página
    if total_registros > 0:
        offset_last = ((total_registros - 1) // limite) * limite
    else:
        offset_last = 0

    enlaces["_last"] = {"href": construir_url(base_url, args_actuales, limite, offset_last)}

    return enlaces

def formatear_errores(codigo, titulo, descripcion):
    """
    Recibe los detalles de un error y devuelve el mensaje en formato JSON
    """
    error = {
        "errors": [
            {
                "code": codigo,
                "message": f"Erorr {codigo}: {titulo}",
                "level": "error",
                "description": descripcion
            }
        ]
    }

    return jsonify(error)

def es_fecha_valida(cadena_fecha):
    """
    Verifica si un string tiene el formato de fecha correcto (YYYY-MM-DD)
    y si es una fecha real en el calendario.
    """
    try:
        # Intenta convertir el texto a fecha con el formato exacto
        datetime.strptime(cadena_fecha, '%Y-%m-%d')
        return True
    except ValueError:
        # Si falla (ya sea por formato o porque mandan 30 de febrero), devuelve False
        return False