"""
Herramienta de cálculo técnico y matemático seguro.
Permite realizar operaciones aritméticas, estimaciones algorítmicas y conversiones de unidades
utilizando el AST de Python de forma determinista y sin ejecución de código inseguro.
Incluye validación estricta de operadores, control de división por cero y manejo de errores sintácticos.
"""

import ast
import operator
from typing import Union

SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _safe_eval(node: ast.AST) -> Union[int, float]:
    """Evalúa recursivamente un nodo de sintaxis AST permitiendo solo operaciones numéricas básicas."""
    if isinstance(node, ast.Expression):
        return _safe_eval(node.body)

    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Tipo de valor no numerico: {type(node.value).__name__}")

    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type in SAFE_OPERATORS:
            operand = _safe_eval(node.operand)
            return SAFE_OPERATORS[op_type](operand)
        raise ValueError(f"Operador unario no permitido: {op_type.__name__}")

    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type in SAFE_OPERATORS:
            left = _safe_eval(node.left)
            right = _safe_eval(node.right)

            # Control de división por cero
            if op_type in (ast.Div, ast.FloorDiv, ast.Mod) and right == 0:
                raise ZeroDivisionError("Division por cero no permitida.")

            # Limitar tamaño de exponentes para evitar sobrecarga computacional
            if op_type == ast.Pow:
                if abs(right) > 1000:
                    raise ValueError("Exponente demasiado grande (maximo permitido: 1000).")

            return SAFE_OPERATORS[op_type](left, right)
        raise ValueError(f"Operador binario no permitido: {op_type.__name__}")

    raise ValueError(f"Expresion no permitida o sintaxis compleja: {type(node).__name__}")


def calculate_metric(expression: str) -> str:
    """Realiza calculos matematicos, conversiones tecnicas y metricas de rendimiento de forma segura.

    Utilizar esta herramienta cuando el usuario solicite calcular formulas,
    estimar complejidades (ej: 2**10, conversiones de bytes a MB/GB), porcentajes
    o cualquier operacion aritmetica precisa.

    Args:
        expression: Expresion matematica en formato texto (ej: '1024 * 1024', '(50 * 100) / 2', '2**16').

    Returns:
        str: Resultado del calculo o descripcion del error de validacion/sintaxis.
    """
    # 1. Validación de entrada no vacía
    if not isinstance(expression, str) or not expression.strip():
        return (
            "Error de validacion: La expresion matematica no puede estar vacia ni ser nula."
        )

    expr_clean = expression.strip()

    # 2. Parsing seguro y evaluación
    try:
        parsed_tree = ast.parse(expr_clean, mode="eval")
        result = _safe_eval(parsed_tree)

        # Si el resultado es float cerrado a entero, mostrarlo limpiamente
        if isinstance(result, float) and result.is_integer():
            result = int(result)

        return f"Calculo exitoso: {expr_clean} = {result}"

    except ZeroDivisionError:
        return f"Error matematico en '{expr_clean}': Division por cero no valida."
    except SyntaxError:
        return (
            f"Error de sintaxis en '{expr_clean}': Expresion matematica mal formada. "
            "Asegurese de utilizar solo numeros, parentesis y operadores (+, -, *, /, //, %, **)."
        )
    except ValueError as val_err:
        return f"Error de validacion en '{expr_clean}': {str(val_err)}"
    except Exception as exc:
        return f"Error al procesar la expresion '{expr_clean}': {type(exc).__name__}: {str(exc)}"
