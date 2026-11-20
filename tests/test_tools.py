"""
Pruebas unitarias para las herramientas del agente ADK.
Verifica el funcionamiento correcto, validación de argumentos,
manejo de errores y control de resultados vacíos.
"""

import os
import sys
import unittest

# Asegurar que la raíz del proyecto está en el PYTHONPATH
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from tools.calculator import calculate_metric
from tools.knowledge_base import save_note, search_notes, list_topics
from tools.web_search import web_search


class TestCalculatorTool(unittest.TestCase):
    """Pruebas para la herramienta de cálculo seguro."""

    def test_basic_arithmetic(self):
        result = calculate_metric("1024 * 1024")
        self.assertIn("1048576", result)
        self.assertIn("Calculo exitoso", result)

    def test_complex_precedence_and_powers(self):
        result = calculate_metric("(2 ** 10) + (100 // 4)")
        self.assertIn("1049", result)

    def test_empty_expression_validation(self):
        result = calculate_metric("   ")
        self.assertIn("Error de validacion", result)

    def test_division_by_zero(self):
        result = calculate_metric("500 / 0")
        self.assertIn("Division por cero", result)

    def test_syntax_error(self):
        result = calculate_metric("10 + * 5")
        self.assertIn("Error de sintaxis", result)

    def test_security_disallowed_syntax(self):
        result = calculate_metric("__import__('os').system('dir')")
        self.assertTrue("Error de sintaxis" in result or "Error de validacion" in result or "Error" in result)


class TestKnowledgeBaseTool(unittest.TestCase):
    """Pruebas para la base de conocimientos persistente en SQLite."""

    def test_save_and_retrieve_note(self):
        # Guardar nota válida
        res_save = save_note(
            topic="Python",
            title="Decoradores",
            content="Un decorador es una funcion que recibe otra funcion y extiende su comportamiento."
        )
        self.assertIn("Nota guardada con exito", res_save)

        # Buscar nota por tema
        res_search = search_notes(topic="Python")
        self.assertIn("Decoradores", res_search)

        # Listar temas
        res_topics = list_topics()
        self.assertIn("Python", res_topics)

    def test_empty_arguments_validation(self):
        res_empty_topic = save_note(topic="", title="Titulo", content="Contenido")
        self.assertIn("Error de validacion", res_empty_topic)

        res_empty_content = save_note(topic="Algoritmos", title="BFS", content="  ")
        self.assertIn("Error de validacion", res_empty_content)

    def test_empty_search_results(self):
        res = search_notes(keyword="PalabraInexistente12345XYZ")
        self.assertIn("No se encontraron notas registradas", res)


class TestWebSearchTool(unittest.TestCase):
    """Pruebas para la herramienta de búsqueda web."""

    def test_empty_query_validation(self):
        result = web_search("   ")
        self.assertIn("Error de validacion", result)

    def test_invalid_max_results(self):
        result = web_search(query="Python", max_results="invalido")
        self.assertIn("Error de validacion", result)


if __name__ == "__main__":
    unittest.main()
