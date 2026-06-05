from services.pacientes_services import crear_paciente, buscar_paciente_por_dni, listar_pacientes, actualizar_paciente, eliminar_paciente
from utils.consola import imprimir_tabla

def menu_pacientes():
    while True:
        print("\n--- Menú de Pacientes ---")
        print("1. Crear nuevo paciente")
        print("2. Buscar paciente por DNI")
        print("3. Listar todos los pacientes")
        print("4. Actualizar datos del paciente")
        print("5. Eliminar paciente")
        print("0. Volver al menú principal")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nombre = input("Ingrese el nombre del paciente: ")
            apellido = input("Ingrese el apellido del paciente: ")
            dni = input("Ingrese el DNI del paciente: ")
            fecha_nacimiento = input("Ingrese la fecha de nacimiento del paciente (YYYY-MM-DD): ")
            telefono = input("Ingrese el teléfono del paciente: ")
            email = input("Ingrese el email del paciente: ")
            direccion = input("Ingrese la dirección del paciente: ")
            
            filas_afectadas, ultimo_id = crear_paciente(
                nombre,
                apellido,
                dni,
                fecha_nacimiento,
                telefono,
                email,
                direccion
            )

            if filas_afectadas > 0:
                print("Paciente creado exitosamente.")
                paciente = buscar_paciente_por_dni(dni)

                if paciente:
                    imprimir_tabla([paciente])
            else:
                print("No se pudo crear el paciente.")

        elif opcion == "2":
            dni = input("Ingrese el DNI del paciente a buscar: ")
            paciente = buscar_paciente_por_dni(dni)
            if paciente:
                imprimir_tabla([paciente])
            else:
                print("No se encontró ningún paciente.")

        elif opcion == "3":
            pacientes = listar_pacientes()
            imprimir_tabla(pacientes)

        elif opcion == "4":
            id_paciente = input("Ingrese el ID del paciente a actualizar: ")
            telefono = input("Ingrese el nuevo teléfono del paciente: ")
            direccion = input("Ingrese la nueva dirección del paciente: ")
            paciente = actualizar_paciente(id_paciente, telefono, direccion)
            imprimir_tabla([paciente])


        elif opcion == "5":
            dni = input("Ingrese el DNI del paciente a eliminar: ")
            paciente = eliminar_paciente(dni)

            if paciente:
                print(f"Paciente eliminado exitosamente")
            else:
                print("No se encontró ningún paciente con ese DNI.")

        elif opcion == "0":
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción del menú.")