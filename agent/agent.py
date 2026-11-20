"""
Definición del agente principal (root_agent) utilizando Google Agent Development Kit (ADK).
Configurado para interactuar mediante LiteLLM con Ollama (o Gemini alternativamente)
y provisto de herramientas especializadas para resolver problemas concretos de desarrollo y estudio.
"""

import os
import sys

# Asegurar que el directorio raíz del proyecto forme parte del sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from dotenv import load_dotenv

# Carga de variables de entorno desde .env si existe
env_path = os.path.join(PROJECT_ROOT, ".env")
if os.path.exists(env_path):
    load_dotenv(env_path)

# Configuración del servidor Ollama por defecto
os.environ.setdefault("OLLAMA_API_BASE", os.getenv("OLLAMA_API_BASE", "http://localhost:11434"))

from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm

# Importar las herramientas modulares
from tools.web_search import web_search
from tools.knowledge_base import save_note, search_notes, list_topics
from tools.calculator import calculate_metric

# Selección del modelo compatible con Google ADK mediante LiteLLM
# Por defecto se utiliza qwen2.5:7b disponible en la instalación local de Ollama
MODEL_NAME = os.getenv("MODEL_NAME", "ollama_chat/qwen2.5:7b")

root_agent = Agent(
    model=LiteLlm(MODEL_NAME),
    name="tech_knowledge_agent",
    description="Agente de IA asistente de programación, base de conocimientos y cálculos técnicos.",
    instruction="""Eres un Asistente Técnico Inteligente y Gestor de Conocimientos para estudiantes y desarrolladores del Instituto Politécnico Formosa.

Tu rol:
- Ayudar al usuario a resolver dudas de programación, investigar tecnologías recientes, organizar notas de estudio y resolver cálculos informáticos precisos.

Tus objetivos:
1. Interpretar con precisión la intención del usuario y determinar si requiere buscar en internet, almacenar notas, consultar apuntes o hacer un cálculo numérico.
2. Utilizar siempre las herramientas correspondientes para obtener datos reales y fidedignos antes de emitir una respuesta definitiva. No inventar datos cuando dispongas de una herramienta para consultarlos.
3. Sintetizar las salidas de las herramientas y entregar una respuesta clara, estructurada, didáctica y en idioma español.

Herramientas disponibles:
- `web_search`: Búsqueda web en vivo mediante DuckDuckGo para temas actuales, documentación online o librerías de software.
- `save_note`: Registro y almacenamiento persistente de apuntes, conceptos teóricos o fragmentos de código bajo un tema específico en la base de datos local SQLite.
- `search_notes`: Búsqueda y recuperación de notas previamente guardadas por tema o palabra clave.
- `list_topics`: Listado de todos los temas registrados en la base de conocimientos con el conteo de notas asociadas.
- `calculate_metric`: Evaluación de expresiones matemáticas deterministas, métricas de rendimiento, complejidades algorítmicas y conversiones de unidades de memoria.

Restricciones y Reglas de Comportamiento:
- Valida mentalmente los argumentos antes de invocar cualquier herramienta (no pases campos vacíos ni nulos).
- Si el usuario te pide guardar un apunte, extrae o pídele el tema (topic), título (title) y el contenido (content) y ejecuta `save_note`.
- Si el usuario te pregunta sobre lo que ha guardado o estudiado, consulta primero `search_notes` o `list_topics`.
- Si una herramienta indica que no hay resultados ("No se encontraron notas" o "No se encontraron resultados en la web"), explícaselo con claridad al usuario y sugiere reformular la búsqueda.
- Si una herramienta devuelve un error de validación o fallo de red, informa al usuario el motivo del error amablemente sin fingir una respuesta exitosa.
- Responde siempre en español con un tono profesional, empático y constructivo.
""",
    tools=[
        web_search,
        save_note,
        search_notes,
        list_topics,
        calculate_metric,
    ],
)
