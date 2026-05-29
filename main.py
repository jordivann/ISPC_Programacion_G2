from db import probar_conexion, imprimir_resultados
from queries import obtener_proveedores


def main():
    probar_conexion()

    proveedores = obtener_proveedores()

    imprimir_resultados("Listado de proveedores", proveedores)


if __name__ == "__main__":
    main()