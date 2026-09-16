#!/usr/bin/env python3
"""Self-check de las funciones puras de ig_gestor (sin navegador).

Uso:  python test_ig_gestor.py
"""

import os
import string
import tempfile

import ig_gestor


def test_generadores():
    nombre, apellido = ig_gestor.generar_nombre()
    assert nombre and apellido
    assert all(c in string.ascii_letters for c in nombre + apellido)

    usuario = ig_gestor.generar_usuario(nombre, apellido)
    assert usuario.startswith(f"{nombre.lower()}.{apellido.lower()}")
    assert any(c.isdigit() for c in usuario)

    password = ig_gestor.generar_password()
    assert len(password) == 16
    permitidos = string.ascii_letters + string.digits + "!@#$%&*"
    assert all(c in permitidos for c in password)


def test_numero_cuenta():
    assert ig_gestor._numero_cuenta("Cuenta 7") == 7
    assert ig_gestor._numero_cuenta("Cuenta 1") == 1
    assert ig_gestor._numero_cuenta("sin prefijo") == 0
    assert ig_gestor._numero_cuenta("Cuenta abc") == 0


def test_cuentas_roundtrip():
    with tempfile.TemporaryDirectory() as tmp:
        ig_gestor.ARCHIVO_CUENTAS = os.path.join(tmp, "cuentas.json")
        ig_gestor.ARCHIVO_TXT = os.path.join(tmp, "cuentas.txt")

        # Archivo inexistente → diccionario vacío
        assert ig_gestor.cargar_cuentas() == {}

        # La numeración es correlativa aunque se mezclen claves ajenas
        ig_gestor.guardar_cuenta("usuario1", "clave1")
        ig_gestor.guardar_cuenta("usuario2", "clave2")

        cuentas = ig_gestor.cargar_cuentas()
        assert len(cuentas) == 2
        assert cuentas["Cuenta 1"]["usuario"] == "usuario1"
        assert cuentas["Cuenta 2"]["contrasena"] == "clave2"

        # La exportación a TXT se genera sin error
        ig_gestor.exportar_cuentas_txt()
        assert os.path.exists(ig_gestor.ARCHIVO_TXT)

        # JSON corrupto → diccionario vacío, nunca una excepción
        with open(ig_gestor.ARCHIVO_CUENTAS, "w") as f:
            f.write("{no válido")
        assert ig_gestor.cargar_cuentas() == {}


if __name__ == "__main__":
    for nombre, fn in sorted(globals().items()):
        if nombre.startswith("test_") and callable(fn):
            fn()
            print(f"✓ {nombre}")
    print("\nTodos los checks pasaron.")
