"""
Herramientas de Base de Conocimientos local utilizando SQLite.
Permite almacenar apuntes, notas y fragmentos de código, además de listarlos y buscarlos.
Incluye validación exhaustiva de argumentos, control de errores y manejo de resultados vacíos.
"""

import os
import sqlite3
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "knowledge_base.db")


def _get_connection() -> sqlite3.Connection:
    """Crea el directorio de datos si no existe y retorna la conexión SQLite."""
    os.makedirs(DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
    return conn


def save_note(topic: str, title: str, content: str) -> str:
    """Guarda una nota tecnica, apunte de clase o fragmento de codigo en la base local.

    Utilizar esta herramienta cuando el usuario pida registrar, guardar, memorizar
    o anotar un concepto, solucion o fragmento de codigo.

    Args:
        topic: Categoria o tema general de la nota (ej: 'Python', 'Redes', 'Docker').
        title: Titulo descriptivo de la nota o apunte.
        content: Contenido detallado, explicacion o codigo a registrar.

    Returns:
        str: Mensaje de confirmacion con el ID asignado a la nota o mensaje de error.
    """
    # 1. Validación de argumentos obligatorios
    if not isinstance(topic, str) or not topic.strip():
        return "Error de validacion: El campo 'topic' es obligatorio y no puede estar vacio."
    if not isinstance(title, str) or not title.strip():
        return "Error de validacion: El campo 'title' es obligatorio y no puede estar vacio."
    if not isinstance(content, str) or not content.strip():
        return "Error de validacion: El campo 'content' es obligatorio y no puede estar vacio."

    topic_clean = topic.strip()
    title_clean = title.strip()
    content_clean = content.strip()
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 2. Inserción protegida en la base de datos
    try:
        conn = _get_connection()
        with conn:
            cursor = conn.execute(
                "INSERT INTO notes (topic, title, content, created_at) VALUES (?, ?, ?, ?)",
                (topic_clean, title_clean, content_clean, created_at),
            )
            note_id = cursor.lastrowid
        conn.close()
        return (
            f"Nota guardada con exito (ID: {note_id}).\n"
            f"Tema: {topic_clean}\n"
            f"Titulo: {title_clean}\n"
            f"Fecha: {created_at}"
        )
    except Exception as exc:
        return f"Error interno al guardar la nota en la base de datos: {type(exc).__name__}: {str(exc)}"


def search_notes(keyword: str = "", topic: str = "") -> str:
    """Busca y recupera notas almacenadas en la base de conocimientos local.

    Utilizar esta herramienta cuando el usuario pregunte por sus notas guardadas,
    apuntes previos, o busque informacion sobre un tema especifico registrado.

    Args:
        keyword: Palabra clave a buscar en el titulo o contenido de las notas.
        topic: Filtro opcional por tema o categoria (coincidencia parcial, insensible a mayusculas).

    Returns:
        str: Lista de notas encontradas con sus detalles, o aviso si no hay coincidencias.
    """
    keyword_clean = keyword.strip() if isinstance(keyword, str) else ""
    topic_clean = topic.strip() if isinstance(topic, str) else ""

    try:
        conn = _get_connection()
        query = "SELECT id, topic, title, content, created_at FROM notes WHERE 1=1"
        params = []

        if topic_clean:
            query += " AND LOWER(topic) LIKE ?"
            params.append(f"%{topic_clean.lower()}%")

        if keyword_clean:
            query += " AND (LOWER(title) LIKE ? OR LOWER(content) LIKE ?)"
            params.append(f"%{keyword_clean.lower()}%")
            params.append(f"%{keyword_clean.lower()}%")

        query += " ORDER BY id DESC LIMIT 10"

        cursor = conn.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        # Control de resultados vacíos
        if not rows:
            filter_info = []
            if topic_clean:
                filter_info.append(f"tema '{topic_clean}'")
            if keyword_clean:
                filter_info.append(f"palabra clave '{keyword_clean}'")
            detail = f" con {', '.join(filter_info)}" if filter_info else ""
            return (
                f"No se encontraron notas registradas{detail}.\n"
                "Sugerencia: Utilice 'list_topics' para ver que temas existen "
                "o verifique la ortografia de su busqueda."
            )

        results = [f"Se encontraron {len(rows)} nota(s) en la base de conocimientos:"]
        for row in rows:
            results.append(
                f"\n--- [ID: {row['id']}] {row['title']} ---\n"
                f"Tema: {row['topic']} | Fecha: {row['created_at']}\n"
                f"Contenido: {row['content']}"
            )

        return "\n".join(results)

    except Exception as exc:
        return f"Error al consultar la base de datos de notas: {type(exc).__name__}: {str(exc)}"


def list_topics() -> str:
    """Lista todos los temas o categorias registrados en la base de conocimientos y la cantidad de notas.

    Utilizar esta herramienta para conocer que temas existen actualmente en la
    base de notas antes de realizar una busqueda especifica.

    Returns:
        str: Resumen de temas disponibles y conteo de notas por tema.
    """
    try:
        conn = _get_connection()
        cursor = conn.execute("""
            SELECT topic, COUNT(*) as total
            FROM notes
            GROUP BY topic
            ORDER BY total DESC, topic ASC
        """)
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return (
                "La base de conocimientos esta vacia actualmente (no hay notas guardadas).\n"
                "Puede comenzar guardando notas con la herramienta 'save_note'."
            )

        total_notes = sum(row["total"] for row in rows)
        summary = [
            f"Base de conocimientos: {len(rows)} tema(s) registrado(s), {total_notes} nota(s) en total:"
        ]
        for row in rows:
            summary.append(f" - {row['topic']}: {row['total']} nota(s)")

        return "\n".join(summary)

    except Exception as exc:
        return f"Error al listar los temas de la base de datos: {type(exc).__name__}: {str(exc)}"
