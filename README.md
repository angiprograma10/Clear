# CLEAR

Lenguaje de programación simple en español.

CLEAR busca que programar sea más sencillo mediante órdenes escritas en español. Su primera versión utiliza un intérprete propio escrito en Python; los programas del usuario se escriben en archivos `.clear`.

## Regla principal

Toda instrucción ejecutable debe declararse mediante `Accion:` y su orden debe estar entre comillas:

```clear
Accion: "Mostrar Hola mundo"
```

Las palabras `Accion` y las órdenes no distinguen entre mayúsculas y minúsculas. CLEAR reconoce sinónimos iniciales para algunas operaciones.

## Funciones iniciales

```clear
Accion: "Mostrar Hola mundo"
Accion: "Crear monedas con valor 100"
Accion: "Sumar 50 a monedas"
Accion: "Mostrar el valor de monedas"
```

Sinónimos iniciales:
- Mostrar: mostrar, enseñar, escribir, imprimir, presentar.
- Crear: crear, generar, declarar, definir.
- Sumar: sumar, agregar, añadir, incrementar, aumentar.
- Restar: restar, disminuir, reducir, descontar.

## Requisitos

- Python 3.10 o superior.
- No requiere instalar paquetes externos.

## Ejecutar un programa

Desde la carpeta principal del repositorio:

```bash
python main.py ejemplos/hola_mundo.clear
python main.py ejemplos/monedas.clear
```

En Windows también puedes usar `py main.py ejemplos/hola_mundo.clear`.

## Ejecutar las pruebas

```bash
python -m unittest discover -s pruebas -v
```

## Estado

CLEAR 0.1 es un prototipo inicial. El intérprete reconoce órdenes sencillas y ejecuta mostrar, crear variables numéricas, sumar y restar. Las condiciones, ciclos, funciones y una gramática más completa todavía están pendientes.
