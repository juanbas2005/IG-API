# IG-API — Gestor de cuentas de Instagram

Automatiza el **registro** y el **inicio de sesión** de cuentas de Instagram
con Playwright (Google Chrome), genera datos aleatorios para cada cuenta y
guarda las credenciales localmente en JSON.

> ⚠️ **Aviso legal**: la creación automatizada de cuentas puede vulnerar los
> [Términos de Uso de Instagram](https://help.instagram.com/581066165581870).
> Este proyecto es para fines educativos y de automatización personal.
> Úsalo bajo tu propia responsabilidad.

## Requisitos

- Python 3.8+
- Google Chrome instalado
- Playwright:

```bash
pip install playwright
playwright install chromium   # opcional: el script usa el Chrome del sistema
```

## Instalación

```bash
git clone https://github.com/juanbas2005/IG-API.git
cd IG-API
pip install playwright
```

## Uso

```bash
python ig_gestor.py
```

Menú principal:

| Opción | Acción |
|---|---|
| 1 | Crear nueva cuenta — genera datos, los guarda y automatiza el registro |
| 2 | Iniciar sesión — elige una cuenta guardada y rellena el login |
| 3 | Mostrar cuentas guardadas |
| 4 | Exportar cuentas a `cuentas.txt` |
| 5 | Borrar todas las cuentas (pide confirmación `BORRAR`) |
| 6 | Salir |

### Registro automático (opción 1)

1. Genera nombre, apellido, usuario y contraseña aleatorios.
2. Guarda la cuenta en `cuentas.json` como `Cuenta N` (numeración correlativa).
3. Abre Chrome, rellena el formulario de registro con el correo de
   `CORREO_REGISTRO` y envía el formulario.
4. Si aparece la pantalla de fecha de nacimiento, completa mes/día/año
   según `DIA_NACIMIENTO`, `MES_NACIMIENTO`, `ANIO_NACIMIENTO`.
5. El navegador **permanece abierto**: los pasos de verificación (código
   SMS/email, captcha) deben completarse manualmente.

### Inicio de sesión (opción 2)

Localiza los campos de usuario y contraseña probando varios selectores (ver
`SELECTORES_USUARIO` / `SELECTORES_PASSWORD` en `ig_gestor.py`), los rellena y
envía el formulario. La comprobación del segundo factor es manual.

## Configuración

Todo se configura con constantes al principio de `ig_gestor.py`:

| Constante | Valor por defecto | Descripción |
|---|---|---|
| `CORREO_REGISTRO` | `razaharez.2020@gmail.com` | Correo usado al registrar cuentas |
| `DIA_NACIMIENTO` | `15` | Día de nacimiento |
| `MES_NACIMIENTO` | `8` | Mes (1–12) |
| `ANIO_NACIMIENTO` | `2000` | Año de nacimiento |
| `ARCHIVO_CUENTAS` | `cuentas.json` | Almacén de credenciales |
| `ARCHIVO_TXT` | `cuentas.txt` | Exportación en texto plano |

## Archivos generados

- `cuentas.json` — credenciales (texto plano)
- `cuentas.txt` — exportación legible
- `*.png` — capturas de pantalla de errores y estados (`error_registro.png`,
  `submit_deshabilitado.png`, `error_login_usuario.png`, …)

Todos están en `.gitignore` para no subir credenciales ni capturas al repositorio.

## Tests

Las funciones puras (generadores, numeración de cuentas, lectura/escritura de
JSON) tienen un self-check sin dependencias:

```bash
python test_ig_gestor.py
```

Los flujos del navegador no se testean automáticamente: requieren Chrome y,
en el caso del registro, interacción manual con Instagram.

## Estructura

```
ig_gestor.py         # Toda la lógica (un solo archivo)
test_ig_gestor.py    # Self-check de funciones puras
cuentas.json         # Generado en tiempo de ejecución (gitignored)
cuentas.txt          # Generado en tiempo de ejecución (gitignored)
```

## Notas de seguridad

- Las contraseñas se guardan **en texto plano** en `cuentas.json`. Si esto te
  preocupa, no uses la opción 1 en máquinas compartidas y mantiene ese archivo
  fuera de cualquier copia de seguridad pública.
- La contraseña generada usa `secrets` (criptográficamente seguro), no `random`.
- `CORREO_REGISTRO` es un valor fijo del código original: cámbialo por el tuyo
  antes de registrar cuentas reales.
