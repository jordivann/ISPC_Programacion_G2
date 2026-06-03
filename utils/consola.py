# ============================================================
# UTILIDADES DE CONSOLA
# Este archivo centraliza funciones para mostrar datos de forma
# clara, ordenada y reutilizable en todo el sistema.
# ============================================================


def pausar():
    """
    Pausa la ejecución hasta que el usuario presione Enter.
    """
    input("\nPresione Enter para continuar...")


def imprimir_titulo(titulo):
    """
    Imprime un título principal para separar secciones del menú.
    """
    ancho = 90
    print("\n" + "=" * ancho)
    print(titulo.upper().center(ancho))
    print("=" * ancho)


def imprimir_subtitulo(subtitulo):
    """
    Imprime un subtítulo para separar bloques internos.
    """
    ancho = 90
    print("\n" + "-" * ancho)
    print(subtitulo.upper())
    print("-" * ancho)


def imprimir_mensaje(mensaje):
    """
    Imprime un mensaje informativo simple.
    """
    print(f"\n{mensaje}")


def imprimir_error(mensaje):
    """
    Imprime un mensaje de error.
    """
    print(f"\n[ERROR] {mensaje}")


def imprimir_exito(mensaje):
    """
    Imprime un mensaje de éxito.
    """
    print(f"\n[OK] {mensaje}")


def imprimir_advertencia(mensaje):
    """
    Imprime un mensaje de advertencia.
    """
    print(f"\n[AVISO] {mensaje}")


def solicitar_texto(mensaje):
    """
    Solicita texto al usuario y elimina espacios innecesarios.
    """
    return input(mensaje).strip()


def solicitar_entero(mensaje):
    """
    Solicita un número entero al usuario.
    Si el valor ingresado no es válido, devuelve None.
    """
    valor = input(mensaje).strip()

    if valor == "":
        return None

    try:
        return int(valor)
    except ValueError:
        imprimir_error("Debe ingresar un número válido.")
        return None


def formatear_valor(valor):
    """
    Formatea valores antes de imprimirlos en tabla.
    Evita mostrar None directamente.
    """
    if valor is None:
        return "-"

    return str(valor)


def imprimir_tabla(registros):
    """
    Imprime una lista de diccionarios en formato tabla.

    Ejemplo esperado:
    [
        {"ID": 1, "Nombre": "Juan", "DNI": "40111222"},
        {"ID": 2, "Nombre": "María", "DNI": "38222333"}
    ]
    """

    if not registros:
        imprimir_advertencia("No se encontraron resultados.")
        return

    columnas = list(registros[0].keys())

    # Calcula el ancho máximo necesario para cada columna.
    anchos = {}

    for columna in columnas:
        ancho_columna = len(str(columna))

        for fila in registros:
            valor = formatear_valor(fila.get(columna))
            ancho_columna = max(ancho_columna, len(valor))

        # Límite razonable para evitar tablas gigantes.
        anchos[columna] = min(ancho_columna, 35)

    def cortar_texto(texto, ancho):
        """
        Corta textos demasiado largos para mantener la tabla prolija.
        """
        texto = formatear_valor(texto)

        if len(texto) <= ancho:
            return texto

        if ancho <= 3:
            return texto[:ancho]

        return texto[:ancho - 3] + "..."

    # Línea separadora.
    linea = "+"

    for columna in columnas:
        linea += "-" * (anchos[columna] + 2) + "+"

    # Encabezado.
    print("\n" + linea)

    encabezado = "|"
    for columna in columnas:
        encabezado += f" {str(columna).ljust(anchos[columna])} |"

    print(encabezado)
    print(linea)

    # Filas.
    for fila in registros:
        fila_texto = "|"

        for columna in columnas:
            valor = cortar_texto(fila.get(columna), anchos[columna])
            fila_texto += f" {valor.ljust(anchos[columna])} |"

        print(fila_texto)

    print(linea)
    print(f"\nTotal de registros: {len(registros)}")


def imprimir_menu(titulo, opciones):
    """
    Imprime un menú con opciones numeradas.

    opciones debe ser una lista de tuplas:
    [
        ("1", "Listar pacientes"),
        ("2", "Buscar paciente por DNI"),
        ("0", "Salir")
    ]
    """

    imprimir_titulo(titulo)

    for numero, descripcion in opciones:
        print(f"{numero}. {descripcion}")


def imprimir_detalle(registro):
    """
    Imprime un único diccionario en formato ficha.

    Sirve para mostrar el resultado de una búsqueda puntual.
    """

    if not registro:
        imprimir_advertencia("No se encontraron resultados.")
        return

    print()

    for clave, valor in registro.items():
        print(f"{clave}: {formatear_valor(valor)}")


def imprimir_lista_numerada(registros, campo_id, campo_descripcion):
    """
    Imprime una lista simple usando un campo ID y un campo descriptivo.

    Ejemplo:
    1. Cardiología
    2. Pediatría
    """

    if not registros:
        imprimir_advertencia("No se encontraron resultados.")
        return

    print()

    for registro in registros:
        print(f"{registro[campo_id]}. {registro[campo_descripcion]}")


def limpiar_consola():
    """
    Limpia visualmente la consola.
    No usa comandos del sistema para evitar problemas entre Windows, Git Bash y PowerShell.
    """
    print("\n" * 3)


def imprimir_opciones(opciones):
    """
    Imprime opciones desde un diccionario.

    Ejemplo:
    {
        "1": "pendiente",
        "2": "confirmado"
    }
    """

    print()

    for clave, valor in opciones.items():
        print(f"{clave}. {valor}")


def seleccionar_opcion(mensaje, opciones):
    """
    Permite seleccionar una opción desde un diccionario.

    Devuelve el valor asociado a la opción elegida.
    Si la opción no existe, devuelve None.
    """

    imprimir_opciones(opciones)

    opcion = input(mensaje).strip()

    if opcion not in opciones:
        imprimir_error("Opción inválida.")
        return None

    return opciones[opcion]

def seleccionar_de_lista(mensaje, opciones):
    """
    Permite seleccionar un elemento desde una lista.

    Devuelve el elemento elegido.
    Si la opción es inválida, devuelve None.
    """

    if not opciones:
        imprimir_advertencia("No hay opciones disponibles.")
        return None

    print()

    for indice, opcion in enumerate(opciones, start=1):
        print(f"{indice}. {opcion}")

    valor = input(mensaje).strip()

    try:
        indice = int(valor)

        if indice < 1 or indice > len(opciones):
            imprimir_error("Opción inválida.")
            return None

        return opciones[indice - 1]

    except ValueError:
        imprimir_error("Debe ingresar un número válido.")
        return None