"""Mensajes de retroalimentación sin anticipar la respuesta completa."""

from __future__ import annotations


def feedback_for_attempt(correct: bool, attempt_number: int) -> str:
    if correct:
        return "El resultado es consistente. Puedes continuar con el siguiente paso."
    if attempt_number == 1:
        return "El resultado todavía no coincide. Revisa el procedimiento y vuelve a intentarlo."
    return (
        "El resultado aún presenta diferencias. Comprueba los valores, índices y operaciones; "
        "si lo necesitas, consulta la orientación del paso."
    )
