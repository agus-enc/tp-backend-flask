def generar_links_paginacion(base_url, limite, desplazamiento, total_registros):
    """
    Calcula y devuelve un diccionario con los enlaces HATEOAS para la paginación.
    """
    enlaces = {}

    # 1. Primera página
    enlaces["_first"] = {"href": f"{base_url}?_limit={limite}&_offset=0"}

    # 2. Página anterior
    if desplazamiento > 0:
        offset_prev = max(0, desplazamiento - limite)
        enlaces["_prev"] = {"href": f"{base_url}?_limit={limite}&_offset={offset_prev}"}

    # 3. Página siguiente
    if desplazamiento + limite < total_registros:
        offset_next = desplazamiento + limite
        enlaces["_next"] = {"href": f"{base_url}?_limit={limite}&_offset={offset_next}"}

    # 4. Última página
    if total_registros > 0:
        offset_last = ((total_registros - 1) // limite) * limite
    else:
        offset_last = 0

    enlaces["_last"] = {"href": f"{base_url}?_limit={limite}&_offset={offset_last}"}

    return enlaces