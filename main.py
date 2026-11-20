"""
Script interactivo para probar el agente por consola (CLI)
o verificar la selección y ejecución de herramientas de forma automatizada.
"""

import os
import sys

# Asegurar importación del paquete
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from agent.agent import root_agent
from google.adk.runners import Runner


def run_interactive_cli():
    """Ejecuta una sesión interactiva en la terminal con el agente."""
    print("=" * 65)
    print(" Agente ADK: Asistente Tecnico y Base de Conocimientos")
    print(f" Modelo configurado: {root_agent.model}")
    print(" Escribe 'salir' o 'exit' para terminar la sesion.")
    print("=" * 65)

    runner = Runner(agent=root_agent)

    while True:
        try:
            user_input = input("\n[Usuario] > ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("salir", "exit", "quit"):
                print("\nFinalizando sesion. ¡Hasta luego!")
                break

            print("\n[Agente procesando...]")
            # Ejecución a través del runner de ADK
            response = runner.run(user_input)
            print(f"\n[Agente]:\n{response}")

        except KeyboardInterrupt:
            print("\nSesion interrumpida por el usuario.")
            break
        except Exception as exc:
            print(f"\n[Error durante la ejecucion]: {exc}")


if __name__ == "__main__":
    run_interactive_cli()
