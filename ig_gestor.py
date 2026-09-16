#!/usr/bin/env python3
"""Asistente de automatización de cuentas de Instagram.

Genera datos aleatorios para cuentas nuevas, las guarda localmente en JSON
y automatiza el registro y el inicio de sesión en instagram.com mediante
Playwright (Google Chrome).

Advertencia: las credenciales se almacenan en texto plano. Este script es
para uso educativo y personal; el registro automatizado puede vulnerar los
Términos de Uso de Instagram.
"""

import json
import os
import random
import secrets
import string

# ==========================================================
# CONFIGURACIÓN
# ==========================================================

DIA_NACIMIENTO = 15
MES_NACIMIENTO = 8
ANIO_NACIMIENTO = 2000

ARCHIVO_CUENTAS = "cuentas.json"
ARCHIVO_TXT = "cuentas.txt"

# Correo usado en el registro de nuevas cuentas
CORREO_REGISTRO = "razaharez.2020@gmail.com"

# Selectores probados en orden; el primero visible gana.
SELECTORES_USUARIO = [
    'input[name="email"]',
    'input[name="username"]',
    'input[autocomplete="username"]',
    'input[aria-label*="username" i]',
    'input[placeholder*="username" i]',
    'input[type="text"]',
]

SELECTORES_PASSWORD = [
    'input[name="pass"]',
    'input[name="password"]',
    'input[type="password"]',
    'input[autocomplete="current-password"]',
    'input[aria-label*="password" i]',
    'input[placeholder*="password" i]',
]


# ==========================================================
# UTILIDADES
# ==========================================================

def separador(titulo, ancho=60):
    """Imprime un título centrado entre dos reglas."""
    print("\n" + "=" * ancho)
    print(titulo.center(ancho))
    print("=" * ancho)


def capturar(page, nombre):
    """Guarda una captura de pantalla e informa su ruta absoluta."""
    try:
        page.screenshot(path=nombre, full_page=True)
        print("\nCaptura guardada:", os.path.abspath(nombre))
    except Exception:
        pass


def info_pagina(page):
    """Muestra la URL, el título y las pestañas abiertas."""
    print("URL:", page.url)
    print("Título:", page.title())
    for i, p in enumerate(page.context.pages):
        print(f"[{i}] URL={p.url} | título={p.title()}")


# ==========================================================
# SISTEMA DE CUENTAS
# ==========================================================

def cargar_cuentas():
    """Carga las cuentas desde JSON; devuelve {} si falta o está corrupto."""
    if not os.path.exists(ARCHIVO_CUENTAS):
        return {}

    try:
        with open(ARCHIVO_CUENTAS, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
            return datos if isinstance(datos, dict) else {}
    except (json.JSONDecodeError, OSError):
        return {}


def guardar_cuentas(cuentas):
    """Escribe el diccionario de cuentas en el archivo JSON."""
    with open(ARCHIVO_CUENTAS, "w", encoding="utf-8") as archivo:
        json.dump(cuentas, archivo, indent=4, ensure_ascii=False)


def _numero_cuenta(nombre):
    """Extrae el número de un nombre 'Cuenta N'; 0 si no tiene formato."""
    try:
        return int(nombre[len("Cuenta "):])
    except (ValueError, IndexError):
        return 0


def guardar_cuenta(usuario, password):
    """Añade una cuenta nueva con el siguiente número libre."""
    cuentas = cargar_cuentas()
    siguiente_numero = max((_numero_cuenta(n) for n in cuentas), default=0) + 1

    nombre_cuenta = f"Cuenta {siguiente_numero}"
    cuentas[nombre_cuenta] = {"usuario": usuario, "contrasena": password}
    guardar_cuentas(cuentas)

    print(f"\n✓ {nombre_cuenta} guardada correctamente.")


def borrar_todas_las_cuentas():
    """Borra todas las cuentas tras pedir confirmación explícita."""
    cuentas = cargar_cuentas()

    if not cuentas:
        print("\nNo hay cuentas guardadas para borrar.")
        return

    separador("BORRAR TODAS LAS CUENTAS")
    print(f"\nSe encontraron {len(cuentas)} cuenta(s).")

    if input("\nEscribe BORRAR para confirmar: ").strip() != "BORRAR":
        print("\n✗ Operación cancelada.")
        return

    try:
        guardar_cuentas({})
        print("\n✓ Todas las cuentas fueron eliminadas.")

        if os.path.exists(ARCHIVO_TXT):
            try:
                os.remove(ARCHIVO_TXT)
                print("✓ También se eliminó el archivo TXT.")
            except OSError as e:
                print("\n⚠ No se pudo eliminar el TXT:")
                print(e)

    except OSError as e:
        print("\n✗ No se pudieron borrar las cuentas.")
        print(e)


def exportar_cuentas_txt():
    """Exporta todas las cuentas a un archivo de texto con formato."""
    cuentas = cargar_cuentas()

    if not cuentas:
        print("\nNo hay cuentas guardadas.")
        return

    try:
        with open(ARCHIVO_TXT, "w", encoding="utf-8") as archivo:
            archivo.write("=" * 60 + "\n")
            archivo.write("              CUENTAS GUARDADAS\n")
            archivo.write("=" * 60 + "\n\n")

            for nombre, datos in cuentas.items():
                archivo.write(f"{nombre}\n")
                archivo.write(f"Usuario:     {datos.get('usuario', '')}\n")
                archivo.write(f"Contraseña:  {datos.get('contrasena', '')}\n")
                archivo.write("-" * 60 + "\n")

        print(f"\n✓ Todas las cuentas fueron exportadas a '{ARCHIVO_TXT}'.")

    except OSError as e:
        print("\n✗ No se pudo crear el archivo TXT.")
        print(e)


def mostrar_cuentas():
    """Muestra las cuentas guardadas por pantalla."""
    cuentas = cargar_cuentas()

    separador("CUENTAS GUARDADAS")

    if not cuentas:
        print("\nNo hay cuentas guardadas.")
        return

    for nombre, datos in cuentas.items():
        print(f"\n{nombre}")
        print(f"Usuario:     {datos.get('usuario', '')}")
        print(f"Contraseña:  {datos.get('contrasena', '')}")

    print("\n" + "=" * 60)


# ==========================================================
# GENERADORES
# ==========================================================

def generar_nombre():
    """Devuelve un par (nombre, apellido) aleatorios."""
    nombres = [
        "Alex", "Daniel", "Carlos", "David",
        "Miguel", "Luis", "Adrian", "Javier",
    ]
    apellidos = [
        "Garcia", "Rodriguez", "Martinez", "Lopez",
        "Hernandez", "Gonzalez", "Perez", "Sanchez",
    ]
    return random.choice(nombres), random.choice(apellidos)


def generar_usuario(nombre, apellido):
    """Genera un usuario estilo nombre.apellidoNNNN."""
    numero = random.randint(1000, 99999)
    return f"{nombre.lower()}.{apellido.lower()}{numero}"


def generar_password():
    """Genera una contraseña aleatoria de 16 caracteres con secrets."""
    caracteres = string.ascii_letters + string.digits + "!@#$%&*"
    return "".join(secrets.choice(caracteres) for _ in range(16))


# ==========================================================
# NAVEGADOR (Playwright se importa aquí: el resto funciona sin él)
# ==========================================================

def buscar_campo(page, selectores, timeout=5000):
    """Devuelve el primer campo visible que coincida con algún selector."""
    for selector in selectores:
        try:
            locator = page.locator(selector).first
            locator.wait_for(state="visible", timeout=timeout)
            return locator
        except Exception:
            continue
    return None


def seleccionar_opcion(page, combo, texto_buscar=None, indice=None):
    """Selecciona una opción de un combobox por texto o por índice."""
    combo.click()

    listbox = page.locator('[role="listbox"]:visible').last
    listbox.wait_for(state="visible", timeout=10000)

    opciones = listbox.locator('[role="option"]')
    cantidad = opciones.count()
    print(f"Opciones visibles: {cantidad}")

    if texto_buscar is not None:
        for i in range(cantidad):
            opcion = opciones.nth(i)
            try:
                if opcion.inner_text().strip() == str(texto_buscar):
                    opcion.click()
                    return
            except Exception:
                pass
        raise Exception(f"No se encontró la opción: {texto_buscar}")

    if indice is not None:
        if indice < 0 or indice >= cantidad:
            raise Exception(f"Índice {indice} fuera de rango.")
        opciones.nth(indice).click()
        return

    raise Exception("No se indicó texto ni índice.")


def seleccionar_fecha(page):
    """Completa la pantalla de fecha de nacimiento del registro."""
    print("\nBuscando controles de fecha...")

    mes = page.get_by_role("combobox", name="Select Month")
    dia = page.get_by_role("combobox", name="Select Day")
    anio = page.get_by_role("combobox", name="Select Year")

    for control in (mes, dia, anio):
        control.wait_for(state="visible", timeout=10000)

    print("✓ Controles de fecha encontrados.")

    print("\nSeleccionando mes...")
    seleccionar_opcion(page, mes, indice=MES_NACIMIENTO - 1)
    print(f"✓ Mes seleccionado: {MES_NACIMIENTO}")

    print("\nSeleccionando día...")
    seleccionar_opcion(page, dia, indice=DIA_NACIMIENTO - 1)
    print(f"✓ Día seleccionado: {DIA_NACIMIENTO}")

    print("\nSeleccionando año...")
    seleccionar_opcion(page, anio, texto_buscar=str(ANIO_NACIMIENTO))
    print(f"✓ Año seleccionado: {ANIO_NACIMIENTO}")


def enviar_formulario(page, submit, nombre="envío"):
    """Espera la validación del formulario y hace click en el botón.

    Devuelve True si el click se realizó, o False si el botón permaneció
    deshabilitado (en ese caso se diagnostica y se captura la pantalla).
    """
    print(f"\nBuscando botón de {nombre}...")
    submit.wait_for(state="visible", timeout=15000)
    print(f"✓ Botón de {nombre} encontrado.")

    page.wait_for_timeout(2000)  # la validación del formulario es asíncrona

    if not submit.is_enabled():
        print(f"⚠ El botón de {nombre} está deshabilitado. Esperando validación...")
        page.wait_for_timeout(3000)

    if not submit.is_enabled():
        print(f"\n✗ El botón de {nombre} continúa deshabilitado.")
        diagnosticar_botones(page)
        capturar(page, "submit_deshabilitado.png")
        return False

    print("✓ Botón habilitado.")
    print(f"\n✓ Haciendo CLICK automático en {nombre}...")
    submit.click(timeout=15000)
    print(f"✓ CLICK EN {nombre.upper()} REALIZADO.")

    page.wait_for_timeout(5000)
    info_pagina(page)
    return True


# ==========================================================
# DIAGNÓSTICOS
# ==========================================================

def diagnosticar_botones(page):
    """Lista los botones de la página con sus atributos principales."""
    print("\nBotones encontrados:")
    try:
        botones = page.locator("button, input[type='submit']")
        print(f"Cantidad: {botones.count()}")

        for i in range(botones.count()):
            try:
                elemento = botones.nth(i)
                texto = ""
                try:
                    texto = elemento.inner_text()
                except Exception:
                    pass

                print(f"\n[{i}]")
                print(f"  Tag: {elemento.evaluate('(e) => e.tagName')}")
                print(f"  Texto: {texto}")
                print(f"  Type: {elemento.get_attribute('type')}")
                print(f"  Disabled: {elemento.is_disabled()}")
            except Exception:
                pass
    except Exception as e:
        print("No se pudieron diagnosticar los botones:")
        print(e)


def diagnosticar_inputs(page):
    """Lista los campos de entrada de la página con sus atributos."""
    print("\nAnalizando campos disponibles...")
    try:
        inputs = page.locator("input")
        print(f"Inputs encontrados: {inputs.count()}")

        for i in range(inputs.count()):
            try:
                elemento = inputs.nth(i)
                print(f"\nInput [{i}]")
                print("  type:", elemento.get_attribute("type"))
                print("  name:", elemento.get_attribute("name"))
                print("  placeholder:", elemento.get_attribute("placeholder"))
                print("  aria-label:", elemento.get_attribute("aria-label"))
            except Exception:
                pass
    except Exception as e:
        print("No se pudieron analizar los inputs:", e)


# ==========================================================
# CREAR CUENTA
# ==========================================================

def crear_cuenta():
    """Genera datos, los guarda y automatiza el registro en Instagram."""
    from playwright.sync_api import sync_playwright

    separador("ASISTENTE DE REGISTRO")

    correo = CORREO_REGISTRO
    nombre, apellido = generar_nombre()
    nombre_completo = f"{nombre} {apellido}"
    usuario = generar_usuario(nombre, apellido)
    password = generar_password()

    print("\nDatos generados:")
    print("-" * 60)
    print(f"Nombre:      {nombre_completo}")
    print(f"Usuario:     {usuario}")
    print(f"Contraseña:  {password}")
    print(f"Nacimiento:  {DIA_NACIMIENTO:02d}/{MES_NACIMIENTO:02d}/{ANIO_NACIMIENTO}")
    print("-" * 60)

    guardar_cuenta(usuario, password)

    with sync_playwright() as p:
        print("\nAbriendo Google Chrome...")

        browser = p.chromium.launch(headless=False, channel="chrome")
        page = browser.new_page()

        try:
            print("Abriendo Instagram...")
            page.goto(
                "https://www.instagram.com/accounts/emailsignup/",
                wait_until="domcontentloaded",
                timeout=30000,
            )
            page.get_by_label("Mobile number or email").wait_for(
                state="visible", timeout=30000
            )
            print("\nFormulario encontrado.")

            page.get_by_label("Mobile number or email").fill(correo)
            print("✓ Correo")

            page.get_by_label("Password").fill(password)
            print("✓ Contraseña")

            page.get_by_label("Full name").fill(nombre_completo)
            print("✓ Nombre")

            page.get_by_label("Username").fill(usuario)
            print("✓ Usuario")

            print("\n✓ Primer formulario completado.")

            # Submit + pantalla de fecha
            submit = page.get_by_role("button", name="Submit")
            enviar_formulario(page, submit)

            print("\nComprobando resultado del Submit...")
            print(f"URL actual: {page.url}")

            try:
                page.get_by_role("combobox", name="Select Month").wait_for(
                    state="visible", timeout=30000
                )
                print("✓ Pantalla de fecha encontrada.")

                try:
                    seleccionar_fecha(page)
                    separador("✓ FECHA COMPLETADA CORRECTAMENTE")
                except Exception as e:
                    separador("✗ ERROR CON LA FECHA")
                    print(type(e).__name__)
                    print(e)

            except Exception:
                print("⚠ No apareció la pantalla de fecha.")
                print(f"URL actual: {page.url}")
                capturar(page, "resultado_submit.png")

            print("\nEl navegador permanecerá abierto.")
            print("Las verificaciones deben hacerse manualmente.")
            input("\nPulsa ENTER para cerrar Chrome...")

        except Exception as e:
            separador("✗ ERROR DURANTE EL REGISTRO")
            print(f"\nTipo: {type(e).__name__}")
            print(f"Mensaje: {e}")
            capturar(page, "error_registro.png")
            input("\nPulsa ENTER para cerrar Chrome...")

        finally:
            browser.close()


# ==========================================================
# INICIAR SESIÓN
# ==========================================================

def _seleccionar_cuenta(cuentas):
    """Pide al usuario una cuenta de la lista; devuelve (datos) o None."""
    separador("INICIAR SESIÓN")

    lista_cuentas = list(cuentas.items())
    for i, (nombre, datos) in enumerate(lista_cuentas, start=1):
        print(f"{i}. {nombre} - {datos.get('usuario', '')}")
    print("=" * 60)

    try:
        indice = int(input("\nSelecciona la cuenta: ").strip()) - 1
    except ValueError:
        print("\n✗ Debes introducir un número.")
        return None

    if indice < 0 or indice >= len(lista_cuentas):
        print("\n✗ Cuenta no válida.")
        return None

    return lista_cuentas[indice][1]


def iniciar_sesion():
    """Automatiza el inicio de sesión de una cuenta guardada."""
    from playwright.sync_api import sync_playwright

    cuentas = cargar_cuentas()

    if not cuentas:
        print("\nNo hay cuentas guardadas.")
        return

    datos = _seleccionar_cuenta(cuentas)
    if datos is None:
        return

    usuario = datos.get("usuario", "")
    password = datos.get("contrasena", "")

    if not usuario:
        print("\n✗ La cuenta no tiene usuario.")
        return
    if not password:
        print("\n✗ La cuenta no tiene contraseña.")
        return

    print("\n" + "-" * 60)
    print(f"Usuario: {usuario}")
    print("-" * 60)

    with sync_playwright() as p:
        print("\nAbriendo Google Chrome...")

        browser = p.chromium.launch(headless=False, channel="chrome")
        page = browser.new_context().new_page()

        try:
            print("Abriendo página de inicio de sesión...")
            page.goto(
                "https://www.instagram.com/accounts/login/",
                wait_until="domcontentloaded",
                timeout=60000,
            )
            print(f"\nURL actual: {page.url}")
            page.wait_for_timeout(5000)

            diagnosticar_inputs(page)

            print("\nBuscando campo de usuario...")
            usuario_input = buscar_campo(page, SELECTORES_USUARIO)
            if usuario_input is None:
                print("\n✗ No se encontró el campo de usuario.")
                capturar(page, "error_login_usuario.png")
                input("\nPulsa ENTER para cerrar Chrome...")
                return

            print("✓ Campo de usuario encontrado.")
            usuario_input.fill(usuario)
            print("✓ Usuario/correo rellenado.")

            print("\nBuscando campo de contraseña...")
            password_input = buscar_campo(page, SELECTORES_PASSWORD)
            if password_input is None:
                print("\n✗ No se encontró el campo de contraseña.")
                capturar(page, "error_login_password.png")
                input("\nPulsa ENTER para cerrar Chrome...")
                return

            print("✓ Campo de contraseña encontrado.")
            password_input.fill(password)
            print("✓ Contraseña rellenada.")

            submit = page.locator('[aria-label="Log In"]')
            if not enviar_formulario(page, submit, nombre="login"):
                input("\nPulsa ENTER para cerrar Chrome...")
                return

            separador("✓ FORMULARIO DE LOGIN COMPLETADO")
            print("\nUsuario y contraseña fueron rellenados.")
            print("El inicio de sesión queda para continuar manualmente.")
            input("\nPulsa ENTER para cerrar Chrome...")

        except Exception as e:
            separador("✗ ERROR DURANTE EL LOGIN")
            print(f"\nTipo: {type(e).__name__}")
            print(f"Mensaje: {e}")

        finally:
            browser.close()


# ==========================================================
# MENÚ PRINCIPAL
# ==========================================================

OPCIONES = {
    "1": ("Crear nueva cuenta", crear_cuenta),
    "2": ("Iniciar sesión", iniciar_sesion),
    "3": ("Mostrar cuentas guardadas", mostrar_cuentas),
    "4": ("Exportar cuentas a TXT", exportar_cuentas_txt),
    "5": ("Borrar todas las cuentas", borrar_todas_las_cuentas),
}


def menu():
    """Bucle principal del gestor de cuentas."""
    while True:
        separador("GESTOR DE CUENTAS")
        for numero, (titulo, _) in OPCIONES.items():
            print(f"{numero}. {titulo}")
        print("6. Salir")
        print("=" * 60)

        opcion = input("\nSelecciona una opción: ").strip()

        if opcion == "6":
            print("\nPrograma cerrado.")
            return
        if opcion in OPCIONES:
            OPCIONES[opcion][1]()
        else:
            print("\n✗ Opción no válida.")


if __name__ == "__main__":
    menu()
