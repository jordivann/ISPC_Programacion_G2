from services.turnos_services import (
    crear_turno,
    listar_turnos,
    cambiar_estado_turno,
    cancelar_turno
)

from utils.consola import imprimir_tabla


def menu_turnos():

    while True:

        print("\n--- MENÚ DE TURNOS ---")
        print("1. Crear turno")
        print("2. Listar turnos")
        print("3. Actualizar estado")
        print("4. Cancelar turno")
        print("0. Volver al menú principal")

        opcion = input("Seleccione una opción: ")

        # Crear turno
        if opcion == "1":

            paciente_id = input("ID Paciente: ")
            medico_id = input("ID Médico: ")
            empleado_id = input("ID Empleado: ")

            fecha_turno = input(
                "Fecha y hora (YYYY-MM-DD HH:MM:SS): "
            )

            motivo_consulta = input(
                "Motivo de consulta: "
            )

            crear_turno(
                paciente_id,
                medico_id,
                empleado_id,
                fecha_turno,
                motivo_consulta
            )

            print("Turno registrado correctamente.")

       
        # Listar turnos
        elif opcion == "2":

            turnos = listar_turnos()

            imprimir_tabla(turnos)

        # Actualizar estado
        elif opcion == "3":

            id_turno = input(
                "Ingrese ID del turno: "
            )

            print("\nEstados disponibles")
            print("1. Pendiente")
            print("2. Confirmado")
            print("3. Atendido")
            print("4. Cancelado")

            opcion_estado = input(
                "Seleccione un estado: "
            )

            estados = {
                "1": "pendiente",
                "2": "confirmado",
                "3": "atendido",
                "4": "cancelado"
            }

            estado = estados.get(opcion_estado)

            if estado:

                cambiar_estado_turno(
                    id_turno,
                    estado
                )

                print("Estado actualizado.")

            else:

                print("Estado inválido.")

        # Cancelar turno
        elif opcion == "4":

            id_turno = input(
                "Ingrese ID del turno: "
            )

            cancelar_turno(id_turno)

            print("Turno cancelado.")

        elif opcion == "0":

            break

        else:

            print("Opción inválida.")