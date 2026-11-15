#!/usr/bin/env python3
"""Intérprete inicial del lenguaje CLEAR."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any


class ErrorClear(Exception):
    """Error comprensible producido por el intérprete CLEAR."""


SINONIMOS = {
    "mostrar": {"mostrar", "enseñar", "escribir", "imprimir", "presentar"},
    "crear": {"crear", "generar", "declarar", "definir"},
    "sumar": {"sumar", "agregar", "añadir", "incrementar", "aumentar"},
    "restar": {"restar", "disminuir", "reducir", "descontar"},
}

PATRON_ACCION = re.compile(r'^\s*accion\s*:\s*"([^"]+)"\s*$', re.IGNORECASE)


class InterpreteClear:
    def __init__(self) -> None:
        self.variables: dict[str, Any] = {}

    @staticmethod
    def normalizar(texto: str) -> str:
        return " ".join(texto.strip().lower().split())

    def identificar_verbo(self, texto: str) -> tuple[str, str]:
        texto = texto.strip()
        if not texto:
            raise ErrorClear("La acción está vacía.")

        palabras = texto.split(maxsplit=1)
        verbo = self.normalizar(palabras[0])
        resto = palabras[1] if len(palabras) > 1 else ""

        for canonico, sinonimos in SINONIMOS.items():
            if verbo in sinonimos:
                return canonico, resto

        raise ErrorClear(
            f"No reconozco la orden «{palabras[0]}». "
            "Prueba con mostrar, crear, sumar o restar."
        )

    def ejecutar_orden(self, orden: str) -> None:
        verbo, resto = self.identificar_verbo(orden)

        if verbo == "mostrar":
            self._mostrar(resto)
        elif verbo == "crear":
            self._crear(resto)
        elif verbo == "sumar":
            self._operar(resto, "+")
        elif verbo == "restar":
            self._operar(resto, "-")

    def _mostrar(self, contenido: str) -> None:
        contenido = contenido.strip()
        if not contenido:
            raise ErrorClear("Indica qué quieres mostrar.")

        coincidencia = re.fullmatch(
            r"(?:el\s+valor\s+de\s+)?([A-Za-z_áéíóúÁÉÍÓÚñÑ][\wáéíóúÁÉÍÓÚñÑ]*)",
            contenido,
            re.IGNORECASE,
        )
        if coincidencia:
            nombre = coincidencia.group(1)
            if nombre in self.variables:
                print(self.variables[nombre])
                return

        print(contenido)

    def _crear(self, contenido: str) -> None:
        coincidencia = re.fullmatch(
            r"([A-Za-z_áéíóúÁÉÍÓÚñÑ][\wáéíóúÁÉÍÓÚñÑ]*)"
            r"\s+con\s+valor\s+(-?\d+(?:\.\d+)?)",
            contenido.strip(),
            re.IGNORECASE,
        )
        if not coincidencia:
            raise ErrorClear(
                'Formato esperado: "Crear nombre con valor 100".'
            )

        nombre, valor_texto = coincidencia.groups()
        self.variables[nombre] = self._numero(valor_texto)
        print(f"Variable «{nombre}» creada.")

    def _operar(self, contenido: str, operador: str) -> None:
        coincidencia = re.fullmatch(
            r"(-?\d+(?:\.\d+)?)\s+(?:a|en)\s+"
            r"([A-Za-z_áéíóúÁÉÍÓÚñÑ][\wáéíóúÁÉÍÓÚñÑ]*)",
            contenido.strip(),
            re.IGNORECASE,
        )
        if not coincidencia:
            accion = "Sumar" if operador == "+" else "Restar"
            raise ErrorClear(
                f'Formato esperado: "{accion} 50 a monedas".'
            )

        cantidad_texto, nombre = coincidencia.groups()
        if nombre not in self.variables:
            raise ErrorClear(f"La variable «{nombre}» no existe.")

        actual = self.variables[nombre]
        if not isinstance(actual, (int, float)):
            raise ErrorClear(f"La variable «{nombre}» no contiene un número.")

        cantidad = self._numero(cantidad_texto)
        self.variables[nombre] = (
            actual + cantidad if operador == "+" else actual - cantidad
        )

    @staticmethod
    def _numero(texto: str) -> int | float:
        numero = float(texto)
        return int(numero) if numero.is_integer() else numero

    def ejecutar_texto(self, codigo: str) -> None:
        encontro_accion = False

        for numero_linea, linea in enumerate(codigo.splitlines(), start=1):
            linea = linea.strip()
            if not linea or linea.startswith("#"):
                continue

            coincidencia = PATRON_ACCION.fullmatch(linea)
            if not coincidencia:
                raise ErrorClear(
                    f"Línea {numero_linea}: toda instrucción debe usar "
                    'Accion: "orden".'
                )

            encontro_accion = True
            orden = coincidencia.group(1)
            try:
                self.ejecutar_orden(orden)
            except ErrorClear as error:
                raise ErrorClear(f"Línea {numero_linea}: {error}") from error

        if not encontro_accion:
            raise ErrorClear("El programa no contiene ninguna acción CLEAR.")


def ejecutar_archivo(ruta: str) -> int:
    archivo = Path(ruta)
    if not archivo.is_file():
        print(f"Error CLEAR: no se encontró el archivo «{ruta}».", file=sys.stderr)
        return 1

    try:
        codigo = archivo.read_text(encoding="utf-8")
        InterpreteClear().ejecutar_texto(codigo)
    except (OSError, UnicodeError) as error:
        print(f"Error al leer el archivo: {error}", file=sys.stderr)
        return 1
    except ErrorClear as error:
        print(f"Error CLEAR: {error}", file=sys.stderr)
        return 1

    return 0


def main() -> int:
    if len(sys.argv) != 2:
        print("Uso: python main.py programa.clear")
        return 2
    return ejecutar_archivo(sys.argv[1])


if __name__ == "__main__":
    raise SystemExit(main())
