# Agent ADK - Asistente Técnico y Base de Conocimientos

**Autor:** Facundo Giuricich  
**Institución:** Instituto Politécnico Formosa  
**Materia:** Fundamentos de Agentes de Inteligencia Artificial  
**Tecnologías:** Python 3.12+, Google Agent Development Kit (ADK), LiteLLM, Ollama, SQLite, DuckDuckGo (`ddgs`).

---

## 📋 Descripción del Proyecto

Este proyecto consiste en el desarrollo de un **Agente de Inteligencia Artificial** autónomo basado en el framework **Google Agent Development Kit (ADK)** y coordinado mediante **LiteLLM**. 

El agente está diseñado para resolver un problema concreto de ingeniería y estudio: actuar como un **Asistente Técnico y Gestor de Conocimientos** para desarrolladores y estudiantes de programación. El agente interpreta solicitudes en lenguaje natural, razona sobre qué acciones tomar, invoca las herramientas correspondientes de forma autónoma, valida las entradas/salidas y formula respuestas precisas basadas en evidencia y datos reales.

> **Importante:** No es un simple chatbot conversacional; cuenta con acceso a herramientas externas de búsqueda en internet en vivo, persistencia en base de datos local y evaluación aritmética/técnica determinista.

---

## 🎯 Arquitectura del Agente

### 1. Modelo de IA
- **Proveedor:** Ollama local conectado a través de **LiteLLM**.
- **Modelo por defecto:** `ollama_chat/qwen2.5:7b` (o compatible como `gemma4:31b-cloud`, `llama3`, etc.).
- **Compatibilidad con Gemini:** También permite utilizar Gemini (`gemini-2.5-flash`) simplemente configurando `GEMINI_API_KEY` en el archivo `.env`.

### 2. Instrucciones del Agente
- **Rol:** Asistente técnico inteligente y gestor de notas de estudio.
- **Objetivo:** Resolver dudas conceptuales y prácticas, buscar documentación en internet, persistir apuntes técnicos y evaluar métricas de rendimiento o conversiones informáticas.
- **Restricciones:**
  - No generar información técnica inventada o desactualizada cuando se disponga de herramientas para verificarla.
  - Validar argumentos antes de llamar a las herramientas (no permitir campos vacíos ni llamadas maliciosas).
  - Tratar adecuadamente fallos de red o búsquedas sin resultados, sugiriendo alternativas al usuario.
  - Comunicarse siempre en español de manera didáctica, estructurada y profesional.

---

## 🛠️ Herramientas Desarrolladas

El agente cuenta con herramientas con responsabilidades claramente diferenciadas:

| Herramienta | Archivo | Responsabilidad |
| :--- | :--- | :--- |
| **`web_search`** | `tools/web_search.py` | Búsqueda en internet en vivo mediante DuckDuckGo (`ddgs`) para consultar documentación oficial, novedades de librerías y errores de software. |
| **`save_note`** | `tools/knowledge_base.py` | Almacenamiento estructurado y persistente de apuntes, fragmentos de código y conceptos teóricos en una base SQLite local (`data/knowledge_base.db`). |
| **`search_notes`** | `tools/knowledge_base.py` | Búsqueda y recuperación de notas guardadas por coincidencia parcial en tema, título o palabra clave. |
| **`list_topics`** | `tools/knowledge_base.py` | Consulta y listado de los temas registrados en la base de conocimientos con el total de notas por tema. |
| **`calculate_metric`** | `tools/calculator.py` | Cálculo matemático determinista y seguro (vía AST de Python) para estimar complejidades ($2^{16}$), conversiones de unidades (bytes a MB/GB) y divisiones sin riesgo de ejecución de código. |

---

## 🛡️ Robustez y Validación

Cada herramienta cuenta con mecanismos exhaustivos de control:
1. **Validación de tipos y argumentos vacíos:**
   - Si se envía un término de búsqueda en blanco a `web_search`, la herramienta rechaza la ejecución y devuelve un mensaje explicativo.
   - Si `save_note` recibe un tema o contenido vacío, notifica los campos faltantes sin corromper la base de datos.
2. **Control de resultados vacíos:**
   - Si una consulta web o una búsqueda en la base de datos no arroja resultados, el agente no inventa; informa amablemente al usuario y sugiere reformular la consulta.
3. **Manejo de excepciones:**
   - Errores de red o timeout en DuckDuckGo son capturados limpiamente.
   - La calculadora intercepta divisiones por cero (`ZeroDivisionError`), sintaxis no válida (`SyntaxError`) e intentos de inyección o invocación de código (`ValueError`), garantizando total seguridad.

---

## 📁 Estructura del Repositorio

```text
agent_adk_facundo_giuricich/
├── agent/
│   ├── __init__.py           # Exportación del root_agent
│   └── agent.py              # Definición de root_agent (ADK + LiteLlm + Tools)
├── tools/
│   ├── __init__.py           # Exportación unificada de herramientas
│   ├── web_search.py         # Herramienta de búsqueda en internet con DuckDuckGo
│   ├── knowledge_base.py     # Herramientas de base de datos SQLite (guardar, buscar, listar)
│   └── calculator.py         # Herramienta de cálculo seguro mediante AST
├── tests/
│   ├── __init__.py
│   └── test_tools.py         # 11 pruebas unitarias automatizadas (validación, errores, casos felices)
├── data/
│   └── .gitkeep              # Directorio donde se almacena knowledge_base.db en runtime
├── main.py                   # Interfaz de prueba por terminal (CLI Runner)
├── requirements.txt          # Dependencias del proyecto
├── .env.example              # Plantilla de variables de entorno
├── .gitignore                # Reglas de exclusión para Git
└── README.md                 # Documentación completa del proyecto
```

---

## 🚀 Instalación y Puesta en Marcha

### 1. Clonar el repositorio y acceder a la carpeta
```bash
git clone https://github.com/facundogiuricich/agent_adk_facundo_giuricich.git
cd agent_adk_facundo_giuricich
```

### 2. Crear y activar el entorno virtual

**En Windows (PowerShell / CMD):**
```bash
uv venv env
.\env\Scripts\activate
```
*(O usando `python -m venv env`)*

**En Linux / macOS:**
```bash
uv venv env
source env/bin/activate
```

### 3. Instalar dependencias
```bash
uv pip install -r requirements.txt
```
*(O mediante `pip install -r requirements.txt`)*

### 4. Configurar el modelo (Ollama / Gemini)
Asegurarse de tener Ollama activo con el modelo deseado:
```bash
ollama serve
ollama list
```
*(Opcional)* Si se desea modificar el puerto o el modelo, copiar `.env.example` a `.env`:
```bash
cp .env.example .env
```

---

## 🧪 Pruebas y Validación

### Ejecutar las pruebas unitarias:
Para verificar que todas las herramientas y sus validaciones funcionan adecuadamente:
```bash
python -m unittest discover -s tests
```

---

## 🖥️ Interfaz de Prueba

### Opción A: Interfaz Web Oficial de Google ADK (Recomendada)
Para iniciar el servidor con la interfaz visual interactiva de Google ADK:

```bash
adk web .
```

Abre tu navegador en:
👉 **`http://localhost:8000`**

Desde allí podrás interactuar con el agente en el chat visual, observar en tiempo real los eventos (*Events*), los trazos de ejecución (*Traces*) y verificar cómo el agente selecciona y ejecuta cada herramienta.

### Opción B: Interfaz por Consola (CLI)
Para interactuar directamente desde la terminal:

```bash
python main.py
```

---

## 💡 Ejemplos de Pruebas de Selección de Herramientas

1. **Prueba de Búsqueda Web:**
   > *"¿Cuáles son las últimas novedades de Python 3.13 lanzadas recientemente?"*  
   > *(El agente seleccionará `web_search` para consultar en vivo).*

2. **Prueba de Almacenamiento en Base de Conocimientos:**
   > *"Guardá una nota en el tema Algoritmos con el título 'Complejidad de QuickSort' y el contenido 'El caso promedio de QuickSort es O(n log n) y el peor caso O(n^2)'."*  
   > *(El agente seleccionará `save_note` y confirmará el guardado con ID).*

3. **Prueba de Consulta de Conocimientos:**
   > *"¿Qué notas tengo guardadas sobre Algoritmos?"* o *"Listame los temas disponibles"*  
   > *(El agente seleccionará `search_notes` o `list_topics`).*

4. **Prueba de Cálculo Técnico Seguro:**
   > *"¿Cuántos bytes son exactamente 4 * 1024 * 1024 y cuánto es 2 elevado a la 16?"*  
   > *(El agente seleccionará `calculate_metric` y procesará el cálculo exacto).*
