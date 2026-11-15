import contextlib
import io
import unittest

from main import ErrorClear, InterpreteClear


class PruebasClear(unittest.TestCase):
    def ejecutar_y_capturar(self, codigo):
        salida = io.StringIO()
        interprete = InterpreteClear()
        with contextlib.redirect_stdout(salida):
            interprete.ejecutar_texto(codigo)
        return salida.getvalue(), interprete

    def test_mostrar_hola_mundo(self):
        salida, _ = self.ejecutar_y_capturar(
            'Accion: "Mostrar Hola mundo"'
        )
        self.assertEqual(salida, "Hola mundo\n")

    def test_sinonimo_ensenar(self):
        salida, _ = self.ejecutar_y_capturar(
            'Accion: "Enseñar Hola mundo"'
        )
        self.assertEqual(salida, "Hola mundo\n")

    def test_crear_sumar_y_mostrar(self):
        codigo = """
Accion: "Crear monedas con valor 100"
Accion: "Sumar 50 a monedas"
Accion: "Mostrar el valor de monedas"
"""
        salida, interprete = self.ejecutar_y_capturar(codigo)
        self.assertEqual(interprete.variables["monedas"], 150)
        self.assertEqual(salida.splitlines()[-1], "150")

    def test_accion_es_obligatoria(self):
        with self.assertRaisesRegex(ErrorClear, "toda instrucción debe usar"):
            InterpreteClear().ejecutar_texto('Mostrar "Hola"')

    def test_variable_inexistente(self):
        with self.assertRaisesRegex(ErrorClear, "no existe"):
            InterpreteClear().ejecutar_texto(
                'Accion: "Sumar 5 a monedas"'
            )

    def test_mayusculas_y_minusculas(self):
        salida, _ = self.ejecutar_y_capturar(
            'ACCION: "MOSTRAR Hola"'
        )
        self.assertEqual(salida, "Hola\n")


if __name__ == "__main__":
    unittest.main()
