from services.empleado_services import (
    crear_empleado,
    buscar_empleado_por_dni,
    listar_empleados,
    actualizar_empleado,
    eliminar_empleado
)

from utils.consola import imprimir_tabla


def menu_empleados():

    while True:

        print("\n--- MENÚ DE EMPLEADOS ---")
        print("1. Crear empleado")
        print("2. Buscar empleado por DNI")
        print("3. Listar empleados")
        print("4. Actualizar empleado")
        print("5. Eliminar empleado")
        print("0. Volver al menú principal")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":

            nombre = input("Ingrese el nombre: ")
            apellido = input("Ingrese el apellido: ")
            dni = input("Ingrese el DNI: ")
            rol = input("Ingrese el rol (admin, medico, recepcionista): ")

            crear_empleado(
                nombre,
                apellido,
                dni,
                rol
            )

            empleado = buscar_empleado_por_dni(dni)

            if empleado:
                imprimir_tabla([empleado])
            else:
                print("Empleado no encontrado.")

            

        elif opcion == "2":

            dni = input("Ingrese el DNI del empleado: ")

            empleado = buscar_empleado_por_dni(dni)

            if empleado:
                imprimir_tabla([empleado])
            else:
                print("Empleado no encontrado.")

        elif opcion == "3":

            empleados = listar_empleados()

            imprimir_tabla(empleados)

        elif opcion == "4":

            dni = input(
                "Ingrese el DNI del empleado a actualizar: "
            )
            rol = input("Nuevo rol: ")
            activo = input("¿El empleado está activo? (s/n): ").lower() == 's'
            
            if activo == 's':
                activo = True
            else:
                activo = False

            actualizar_empleado(
                dni,
                rol,
                activo
            )

            print("Empleado actualizado correctamente.")

        elif opcion == "5":

            dni = input(
                "Ingrese el DNI del empleado a eliminar: "
            )

            empleado = eliminar_empleado(dni)
            if empleado:
                print("Empleado eliminado correctamente.")
            else:
                print("No se encontró ningún empleado con ese DNI.")

          

        elif opcion == "0":

            break

        else:

            print("Opción inválida.")