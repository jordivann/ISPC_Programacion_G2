from services.medicos_services import (
    crear_medico,
    buscar_medico_por_matricula,
    listar_medicos,
    actualizar_medico,
    eliminar_medico
)

from utils.consola import imprimir_tabla


def menu_medicos():

    while True:

        print("\n--- MENÚ DE MÉDICOS ---")
        print("1. Crear nuevo médico")
        print("2. Buscar médico por matrícula")
        print("3. Listar todos los médicos")
        print("4. Actualizar datos del médico")
        print("5. Eliminar médico")
        print("0. Volver al menú principal")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":

            nombre = input("Ingrese el nombre: ")
            apellido = input("Ingrese el apellido: ")
            matricula = input("Ingrese la matrícula: ")
            telefono = input("Ingrese el teléfono: ")
            email = input("Ingrese el email: ")
            especialidad = input("Ingrese la especialidad: ")

            crear_medico(
                nombre,
                apellido,
                matricula,
                telefono,
                email,
                especialidad
            )

            medico = buscar_medico_por_matricula(matricula)

            imprimir_tabla([medico])

        elif opcion == "2":

            matricula = input("Ingrese la matrícula: ")

            medico = buscar_medico_por_matricula(matricula)

            if medico:
                imprimir_tabla([medico])
            else:
                print("Médico no encontrado.")

        elif opcion == "3":

            medicos = listar_medicos()

            imprimir_tabla(medicos)

        elif opcion == "4":

            matricula = input(
                "Ingrese la matrícula del médico a actualizar: "
            )
            telefono = input("Nuevo teléfono: ")
            email = input("Nuevo email: ")

            actualizar_medico(
                matricula,
                telefono,
                email
            )

            print("Médico actualizado correctamente.")

        elif opcion == "5":

            matricula = input(
                "Ingrese la matrícula del médico a eliminar: "
            )

            eliminar_medico(matricula)

            print("Médico eliminado correctamente.")

        elif opcion == "0":

            break

        else:

            print("Opción inválida.")