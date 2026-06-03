from conexion import conectar

from utils.consola import (
    pausar,
    limpiar_consola,
    imprimir_titulo,
    imprimir_subtitulo,
    imprimir_tabla,
    imprimir_error,
    imprimir_exito,
    imprimir_advertencia,
    solicitar_texto,
    solicitar_entero,
    seleccionar_opcion,
    seleccionar_de_lista,
)

from services.pacientes_services import (
    listar_pacientes,
    buscar_paciente_por_dni,
    obtener_pacientes_resumidos,
)

from services.medicos_services import (
    listar_especialidades,
    obtener_especialidades_resumidas,
    listar_medicos,
    obtener_medicos_resumidos,
    buscar_medicos_por_especialidad,
    ver_disponibilidad_por_medico,
    ver_disponibilidad_por_especialidad,
)

from services.turnos_services import (
    ver_turnos_por_dni_paciente,
    ver_turnos_por_medico,
    ver_todos_los_turnos,
    filtrar_turnos_por_estado,
    registrar_turno,
    cambiar_estado_turno,
    generar_horarios_disponibles,
    obtener_fechas_con_horarios_disponibles,
)

from services.reportes_services import (
    reporte_turnos_por_estado,
    reporte_turnos_por_especialidad,
)


def probar_conexion():
    try:
        conexion = conectar()

        if conexion.is_connected():
            imprimir_exito("Conexión exitosa a la base de datos.")

        conexion.close()

    except Exception as error:
        imprimir_error("No se pudo conectar con la base de datos.")
        print(error)


# ============================================================
# OPCIONES DEL MENÚ
# ============================================================

def opcion_listar_pacientes():
    imprimir_titulo("Listado de pacientes")
    imprimir_tabla(listar_pacientes())


def opcion_buscar_paciente_por_dni():
    dni = solicitar_texto("\nIngrese el DNI del paciente: ")

    if dni == "":
        imprimir_error("Debe ingresar un DNI.")
        return

    imprimir_titulo("Resultado de búsqueda por DNI")
    imprimir_tabla(buscar_paciente_por_dni(dni))


def opcion_listar_especialidades():
    imprimir_titulo("Especialidades médicas")
    imprimir_tabla(listar_especialidades())


def opcion_listar_medicos():
    imprimir_titulo("Listado de médicos")
    imprimir_tabla(listar_medicos())


def opcion_buscar_medicos_por_especialidad():
    imprimir_titulo("Buscar médicos por especialidad")

    imprimir_subtitulo("Especialidades disponibles")
    imprimir_tabla(obtener_especialidades_resumidas())

    id_especialidad = solicitar_entero(
        "\nIngrese el ID de la especialidad que desea consultar: "
    )

    if id_especialidad is None:
        imprimir_error("Debe ingresar un ID de especialidad.")
        return

    imprimir_subtitulo("Médicos encontrados")
    imprimir_tabla(buscar_medicos_por_especialidad(id_especialidad))


def opcion_ver_turnos_por_dni_paciente():
    dni = solicitar_texto("\nIngrese el DNI del paciente: ")

    if dni == "":
        imprimir_error("Debe ingresar un DNI.")
        return

    imprimir_titulo("Turnos del paciente")
    imprimir_tabla(ver_turnos_por_dni_paciente(dni))


def opcion_ver_turnos_por_medico():
    imprimir_titulo("Ver turnos por médico")

    imprimir_subtitulo("Médicos disponibles")
    imprimir_tabla(obtener_medicos_resumidos())

    id_medico = solicitar_entero("\nIngrese el ID del médico: ")

    if id_medico is None:
        imprimir_error("Debe ingresar un ID de médico.")
        return

    imprimir_titulo("Agenda del médico")
    imprimir_tabla(ver_turnos_por_medico(id_medico))


def opcion_ver_todos_los_turnos():
    imprimir_titulo("Listado general de turnos")
    imprimir_tabla(ver_todos_los_turnos())


def opcion_filtrar_turnos_por_estado():
    imprimir_titulo("Filtrar turnos por estado")

    estados = {
        "1": "pendiente",
        "2": "confirmado",
        "3": "cancelado",
        "4": "atendido",
        "5": "ausente",
    }

    estado = seleccionar_opcion("\nSeleccione el estado: ", estados)

    if estado is None:
        return

    imprimir_titulo(f"Turnos con estado: {estado}")
    imprimir_tabla(filtrar_turnos_por_estado(estado))


def opcion_ver_disponibilidad_por_medico():
    imprimir_titulo("Ver disponibilidad por médico")

    imprimir_subtitulo("Médicos disponibles")
    imprimir_tabla(obtener_medicos_resumidos())

    id_medico = solicitar_entero("\nIngrese el ID del médico: ")

    if id_medico is None:
        imprimir_error("Debe ingresar un ID de médico.")
        return

    imprimir_titulo("Disponibilidad del médico")
    imprimir_tabla(ver_disponibilidad_por_medico(id_medico))


def opcion_ver_disponibilidad_por_especialidad():
    imprimir_titulo("Ver disponibilidad por especialidad")

    imprimir_subtitulo("Especialidades disponibles")
    imprimir_tabla(obtener_especialidades_resumidas())

    id_especialidad = solicitar_entero("\nIngrese el ID de la especialidad: ")

    if id_especialidad is None:
        imprimir_error("Debe ingresar un ID de especialidad.")
        return

    imprimir_titulo("Disponibilidad por especialidad")
    imprimir_tabla(ver_disponibilidad_por_especialidad(id_especialidad))


def opcion_reporte_turnos_por_estado():
    imprimir_titulo("Reporte de turnos por estado")
    imprimir_tabla(reporte_turnos_por_estado())


def opcion_reporte_turnos_por_especialidad():
    imprimir_titulo("Reporte de turnos por especialidad")
    imprimir_tabla(reporte_turnos_por_especialidad())


# ============================================================
# INSERT: REGISTRAR TURNO
# ============================================================

def opcion_registrar_turno():
    imprimir_titulo("Registrar nuevo turno")

    imprimir_subtitulo("Pacientes disponibles")
    imprimir_tabla(obtener_pacientes_resumidos())

    id_paciente = solicitar_entero("\nIngrese el ID del paciente: ")

    if id_paciente is None:
        imprimir_error("Debe ingresar un ID de paciente válido.")
        return

    imprimir_subtitulo("Médicos disponibles")
    imprimir_tabla(obtener_medicos_resumidos())

    id_medico = solicitar_entero("\nIngrese el ID del médico: ")

    if id_medico is None:
        imprimir_error("Debe ingresar un ID de médico válido.")
        return

    fecha = solicitar_texto("\nIngrese la fecha del turno (AAAA-MM-DD): ")
    hora = solicitar_texto("Ingrese la hora del turno (HH:MM): ")

    if fecha == "" or hora == "":
        imprimir_error("Debe ingresar fecha y hora.")
        return

    fecha_turno = f"{fecha} {hora}:00"

    if existe_turno_para_medico(id_medico, fecha_turno):
        imprimir_error("El médico ya tiene un turno pendiente o confirmado en ese horario.")
        return

    motivo = solicitar_texto("Ingrese el motivo de consulta: ")

    if motivo == "":
        motivo = "Consulta médica"

    try:
        filas_afectadas, ultimo_id = registrar_turno(
            id_paciente,
            id_medico,
            fecha_turno,
            motivo
        )

        if filas_afectadas > 0:
            imprimir_exito(f"Turno registrado correctamente. ID generado: {ultimo_id}")
        else:
            imprimir_advertencia("No se pudo registrar el turno.")

    except Exception as error:
        imprimir_error("No se pudo registrar el turno.")
        print(error)


# ============================================================
# UPDATE: CAMBIAR ESTADO DE TURNO
# ============================================================

def opcion_cambiar_estado_turno():
    imprimir_titulo("Cambiar estado de un turno")

    imprimir_subtitulo("Turnos registrados")
    imprimir_tabla(ver_todos_los_turnos())

    id_turno = solicitar_entero("\nIngrese el ID del turno que desea modificar: ")

    if id_turno is None:
        imprimir_error("Debe ingresar un ID de turno válido.")
        return

    estados = {
        "1": "pendiente",
        "2": "confirmado",
        "3": "cancelado",
        "4": "atendido",
        "5": "ausente",
    }

    nuevo_estado = seleccionar_opcion("\nSeleccione el nuevo estado: ", estados)

    if nuevo_estado is None:
        return

    filas_afectadas, _ = cambiar_estado_turno(id_turno, nuevo_estado)

    if filas_afectadas > 0:
        imprimir_exito("Estado del turno actualizado correctamente.")
    else:
        imprimir_advertencia("No se encontró un turno con ese ID.")


# ============================================================
# MENÚ PRINCIPAL
# ============================================================

def mostrar_menu():
    while True:
        limpiar_consola()

        imprimir_titulo("Sistema de consultas - Turnos médicos")

        print("CONSULTAS GENERALES")
        print("1. Probar conexión")
        print("2. Listar pacientes")
        print("3. Buscar paciente por DNI")
        print("4. Listar especialidades")
        print("5. Listar médicos")

        print("\nFILTROS Y BÚSQUEDAS")
        print("6. Buscar médicos por especialidad")
        print("7. Ver turnos de un paciente por DNI")
        print("8. Ver turnos de un médico")
        print("9. Ver todos los turnos")
        print("10. Filtrar turnos por estado")
        print("11. Ver disponibilidad por médico")
        print("12. Ver disponibilidad por especialidad")

        print("\nGESTIÓN DE TURNOS")
        print("13. Registrar nuevo turno")
        print("14. Cambiar estado de un turno")

        print("\nREPORTES")
        print("15. Reporte: turnos por estado")
        print("16. Reporte: turnos por especialidad")

        print("\n0. Salir")

        opcion = solicitar_texto("\nSeleccione una opción: ")

        try:
            if opcion == "1":
                probar_conexion()
            elif opcion == "2":
                opcion_listar_pacientes()
            elif opcion == "3":
                opcion_buscar_paciente_por_dni()
            elif opcion == "4":
                opcion_listar_especialidades()
            elif opcion == "5":
                opcion_listar_medicos()
            elif opcion == "6":
                opcion_buscar_medicos_por_especialidad()
            elif opcion == "7":
                opcion_ver_turnos_por_dni_paciente()
            elif opcion == "8":
                opcion_ver_turnos_por_medico()
            elif opcion == "9":
                opcion_ver_todos_los_turnos()
            elif opcion == "10":
                opcion_filtrar_turnos_por_estado()
            elif opcion == "11":
                opcion_ver_disponibilidad_por_medico()
            elif opcion == "12":
                opcion_ver_disponibilidad_por_especialidad()
            elif opcion == "13":
                opcion_registrar_turno()
            elif opcion == "14":
                opcion_cambiar_estado_turno()
            elif opcion == "15":
                opcion_reporte_turnos_por_estado()
            elif opcion == "16":
                opcion_reporte_turnos_por_especialidad()
            elif opcion == "0":
                imprimir_exito("Saliendo del sistema.")
                break
            else:
                imprimir_error("Opción inválida. Intente nuevamente.")

        except Exception as error:
            imprimir_error("Ocurrió un error al ejecutar la opción seleccionada.")
            print(error)

        pausar()


# from conexion import conectar


# def probar_conexion():
#     """
#     Prueba si Python logra conectarse correctamente a MySQL.
#     """

#     try:
#         conexion = conectar()

#         if conexion.is_connected():
#             print("\nConexión exitosa a la base de datos.")

#         conexion.close()

#     except Exception as error:
#         print("\nError al conectar con la base de datos:")
#         print(error)


# def listar_pacientes():
#     """
#     Ejecuta un SELECT simple sobre la tabla pacientes.
#     Sirve como primera prueba de lectura desde Python.
#     """

#     try:
#         conexion = conectar()
#         cursor = conexion.cursor()

#         consulta = """
#             SELECT 
#                 id_paciente,
#                 nombre,
#                 apellido,
#                 dni,
#                 telefono
#             FROM pacientes
#             ORDER BY apellido, nombre;
#         """

#         cursor.execute(consulta)
#         pacientes = cursor.fetchall()

#         print("\nListado de pacientes:")
#         print("-" * 60)

#         if not pacientes:
#             print("No hay pacientes cargados.")
#         else:
#             for paciente in pacientes:
#                 print(f"ID: {paciente[0]}")
#                 print(f"Nombre: {paciente[1]} {paciente[2]}")
#                 print(f"DNI: {paciente[3]}")
#                 print(f"Teléfono: {paciente[4]}")
#                 print("-" * 60)

#         cursor.close()
#         conexion.close()

#     except Exception as error:
#         print("\nError al consultar pacientes:")
#         print(error)


# def mostrar_menu():
#     """
#     Muestra el menú principal del sistema por consola.
#     """

#     while True:
#         print("\n" + "=" * 60)
#         print("SISTEMA DE TURNOS MÉDICOS")
#         print("=" * 60)
#         print("1. Probar conexión")
#         print("2. Listar pacientes")
#         print("0. Salir")

#         opcion = input("\nSeleccione una opción: ").strip()

#         if opcion == "1":
#             probar_conexion()

#         elif opcion == "2":
#             listar_pacientes()

#         elif opcion == "0":
#             print("\nSaliendo del sistema...")
#             break

#         else:
#             print("\nOpción inválida. Intente nuevamente.")

#         input("\nPresione Enter para continuar...")