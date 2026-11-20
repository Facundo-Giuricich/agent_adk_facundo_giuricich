"""
Herramienta de búsqueda en la web utilizando ddgs (DuckDuckGo).
Permite al agente consultar información técnica actualizada en internet.
Incluye validaciones de argumentos, control de errores y tratamiento de respuestas vacías.
"""

from typing import Optional
from ddgs import DDGS


def web_search(query: str, max_results: int = 5) -> str:
    """Busca informacion tecnica y actualizada en internet utilizando DuckDuckGo.

    Utilizar esta herramienta cuando se necesite responder preguntas sobre
    librerias recientes, noticias tecnologicas, sintaxis actualizada o cuando
    la informacion solicitada no se encuentre en la base de conocimientos local.

    Args:
        query: Consulta o termino a buscar en internet. No debe estar vacio.
        max_results: Cantidad maxima de resultados a retornar (entero entre 1 y 10).

    Returns:
        str: Texto formateado con los titulos, resumenes y enlaces encontrados,
             o un mensaje descriptivo de error/sin resultados.
    """
    # 1. Validación de argumentos de entrada
    if not isinstance(query, str) or not query.strip():
        return (
            "Error de validacion en web_search: El termino de busqueda 'query' "
            "no puede estar vacio ni ser nulo."
        )

    try:
        max_results_int = int(max_results)
    except (ValueError, TypeError):
        return (
            "Error de validacion en web_search: El argumento 'max_results' "
            "debe ser un numero entero valido."
        )

    if max_results_int < 1:
        max_results_int = 1
    elif max_results_int > 10:
        max_results_int = 10

    query_clean = query.strip()

    # 2. Ejecución protegida de la búsqueda
    try:
        ddgs = DDGS()
        raw_results = list(ddgs.text(query_clean, max_results=max_results_int))

        # 3. Control de resultados vacíos
        if not raw_results:
            return (
                f"No se encontraron resultados en la web para la consulta: '{query_clean}'. "
                "Sugerencia: Intente reformular la busqueda con palabras clave mas generales."
            )

        # 4. Formateo legible para el LLM y el usuario
        formatted_results = [
            f"Resultados de busqueda web para '{query_clean}' ({len(raw_results)} encontrados):"
        ]
        for idx, item in enumerate(raw_results, 1):
            title = item.get("title", "Sin titulo")
            body = item.get("body", "Sin descripcion")
            href = item.get("href", "")
            formatted_results.append(
                f"\n[{idx}] {title}\n"
                f"    Resumen: {body}\n"
                f"    Fuente: {href}"
            )

        return "\n".join(formatted_results)

    except Exception as exc:
        # Control de excepciones (errores de red, timeout, etc.)
        return (
            f"Error al ejecutar la busqueda web para '{query_clean}': {type(exc).__name__}: {str(exc)}. "
            "Verifique la conexion a internet e intente nuevamente."
        )
