from services.db_services import ejecutar_select, ejecutar_modificacion
from datetime import datetime, timedelta



def ver_turnos_por_dni_paciente(dni):
    consulta = """
        SELECT 
            t.id_turno AS Turno,
            t.fecha_turno AS `Fecha Turno`,
            t.estado AS Estado,
            CONCAT(p.nombre, ' ', p.apellido) AS Paciente,
            p.dni AS DNI,
            CONCAT(m.nombre, ' ', m.apellido) AS Medico,
            e.nombre AS Especialidad,
            t.motivo_consulta AS `Motivo Consulta`
        FROM turnos t
        INNER JOIN pacientes p
            ON t.paciente_id = p.id_paciente
        INNER JOIN medicos m
            ON t.medico_id = m.id_medico
        INNER JOIN especialidades e
            ON m.id_especialidad = e.id_especialidad
        WHERE p.dni = %s
        ORDER BY t.fecha_turno DESC;
    """

    return ejecutar_select(consulta, (dni,))


def ver_turnos_por_medico(id_medico):
    consulta = """
        SELECT 
            t.id_turno AS Turno,
            t.fecha_turno AS `Fecha Turno`,
            t.estado AS Estado,
            CONCAT(p.nombre, ' ', p.apellido) AS Paciente,
            p.dni AS DNI,
            p.telefono AS Telefono,
            t.motivo_consulta AS `Motivo Consulta`
        FROM turnos t
        INNER JOIN pacientes p
            ON t.paciente_id = p.id_paciente
        WHERE t.medico_id = %s
        ORDER BY t.fecha_turno;
    """

    return ejecutar_select(consulta, (id_medico,))


def ver_todos_los_turnos():
    consulta = """
        SELECT 
            t.id_turno AS Turno,
            t.fecha_turno AS `Fecha Turno`,
            t.estado AS Estado,
            CONCAT(p.nombre, ' ', p.apellido) AS Paciente,
            CONCAT(m.nombre, ' ', m.apellido) AS Medico,
            e.nombre AS Especialidad,
            t.motivo_consulta AS `Motivo Consulta`
        FROM turnos t
        INNER JOIN pacientes p
            ON t.paciente_id = p.id_paciente
        INNER JOIN medicos m
            ON t.medico_id = m.id_medico
        INNER JOIN especialidades e
            ON m.id_especialidad = e.id_especialidad
        ORDER BY t.fecha_turno;
    """

    return ejecutar_select(consulta)


def filtrar_turnos_por_estado(estado):
    consulta = """
        SELECT 
            t.id_turno AS Turno,
            t.fecha_turno AS `Fecha Turno`,
            t.estado AS Estado,
            CONCAT(p.nombre, ' ', p.apellido) AS Paciente,
            CONCAT(m.nombre, ' ', m.apellido) AS Medico,
            e.nombre AS Especialidad,
            t.motivo_consulta AS `Motivo Consulta`
        FROM turnos t
        INNER JOIN pacientes p
            ON t.paciente_id = p.id_paciente
        INNER JOIN medicos m
            ON t.medico_id = m.id_medico
        INNER JOIN especialidades e
            ON m.id_especialidad = e.id_especialidad
        WHERE LOWER(t.estado) = %s
        ORDER BY t.fecha_turno;
    """

    return ejecutar_select(consulta, (estado,))


def existe_turno_para_medico(id_medico, fecha_turno):
    """
    Verifica si el médico ya tiene un turno activo en esa fecha y hora.
    """

    consulta = """
        SELECT 
            id_turno AS Turno,
            fecha_turno AS `Fecha Turno`,
            estado AS Estado
        FROM turnos
        WHERE medico_id = %s
          AND fecha_turno = %s
          AND estado IN ('pendiente', 'confirmado');
    """

    resultados = ejecutar_select(consulta, (id_medico, fecha_turno))

    return len(resultados) > 0

def opcion_registrar_turno():
    """
    Registra un nuevo turno con selección guiada.

    El usuario elige:
    - paciente;
    - especialidad;
    - médico;
    - rango de fechas;
    - día disponible;
    - horario disponible.

    No escribe la fecha ni la hora manualmente.
    """

    imprimir_titulo("Registrar nuevo turno")

    # ------------------------------------------------------------
    # 1. Seleccionar paciente
    # ------------------------------------------------------------
    imprimir_subtitulo("Pacientes disponibles")
    imprimir_tabla(obtener_pacientes_resumidos())

    id_paciente = solicitar_entero("\nIngrese el ID del paciente: ")

    if id_paciente is None:
        imprimir_error("Debe ingresar un ID de paciente válido.")
        return

    # ------------------------------------------------------------
    # 2. Seleccionar especialidad
    # ------------------------------------------------------------
    imprimir_subtitulo("Especialidades disponibles")
    imprimir_tabla(obtener_especialidades_resumidas())

    id_especialidad = solicitar_entero("\nIngrese el ID de la especialidad: ")

    if id_especialidad is None:
        imprimir_error("Debe ingresar un ID de especialidad válido.")
        return

    # ------------------------------------------------------------
    # 3. Seleccionar médico según especialidad
    # ------------------------------------------------------------
    medicos = buscar_medicos_por_especialidad(id_especialidad)

    imprimir_subtitulo("Médicos disponibles para la especialidad")
    imprimir_tabla(medicos)

    if not medicos:
        imprimir_advertencia("No hay médicos disponibles para esa especialidad.")
        return

    id_medico = solicitar_entero("\nIngrese el ID del médico: ")

    if id_medico is None:
        imprimir_error("Debe ingresar un ID de médico válido.")
        return

    # ------------------------------------------------------------
    # 4. Seleccionar rango de fechas
    # ------------------------------------------------------------
    imprimir_subtitulo("Rango de búsqueda")

    rangos = {
        "1": "Esta semana",
        "2": "Semana próxima",
        "3": "Próximas 3 semanas",
    }

    opcion_rango = seleccionar_opcion(
        "\nSeleccione el rango de fechas: ",
        rangos
    )

    if opcion_rango is None:
        return

    # Necesitamos recuperar la clave elegida, no el texto.
    # Como seleccionar_opcion devuelve el valor, buscamos la clave correspondiente.
    opcion_rango_clave = None

    for clave, valor in rangos.items():
        if valor == opcion_rango:
            opcion_rango_clave = clave

    if opcion_rango_clave is None:
        imprimir_error("No se pudo interpretar el rango seleccionado.")
        return

    # ------------------------------------------------------------
    # 5. Obtener días con horarios disponibles
    # ------------------------------------------------------------
    fechas_disponibles = obtener_fechas_con_horarios_disponibles(
        id_medico,
        opcion_rango_clave
    )

    if not fechas_disponibles:
        imprimir_advertencia("No hay días con horarios disponibles para ese rango.")
        return

    opciones_dias = []

    for item in fechas_disponibles:
        opciones_dias.append(item["descripcion"])

    imprimir_subtitulo("Días disponibles")

    dia_elegido = seleccionar_de_lista(
        "\nSeleccione el día del turno: ",
        opciones_dias
    )

    if dia_elegido is None:
        return

    fecha_elegida = None
    horarios_disponibles = []

    for item in fechas_disponibles:
        if item["descripcion"] == dia_elegido:
            fecha_elegida = item["fecha"]
            horarios_disponibles = item["horarios"]

    if fecha_elegida is None:
        imprimir_error("No se pudo obtener la fecha seleccionada.")
        return

    # ------------------------------------------------------------
    # 6. Seleccionar horario disponible
    # ------------------------------------------------------------
    imprimir_subtitulo("Horarios disponibles")

    horario_elegido = seleccionar_de_lista(
        "\nSeleccione el horario del turno: ",
        horarios_disponibles
    )

    if horario_elegido is None:
        return

    fecha_turno = f"{fecha_elegida} {horario_elegido}:00"

    # ------------------------------------------------------------
    # 7. Motivo de consulta
    # ------------------------------------------------------------
    motivo = solicitar_texto("\nIngrese el motivo de consulta: ")

    if motivo == "":
        motivo = "Consulta médica"

    # ------------------------------------------------------------
    # 8. Registrar turno
    # ------------------------------------------------------------
    try:
        filas_afectadas, ultimo_id = registrar_turno(
            id_paciente,
            id_medico,
            fecha_turno,
            motivo
        )

        if filas_afectadas > 0:
            imprimir_exito(f"Turno registrado correctamente. ID generado: {ultimo_id}")
            imprimir_exito(f"Fecha y hora asignada: {fecha_turno}")
        else:
            imprimir_advertencia("No se pudo registrar el turno.")

    except Exception as error:
        imprimir_error("No se pudo registrar el turno.")
        print(error)
def cambiar_estado_turno(id_turno, nuevo_estado):
    """
    Actualiza el estado de un turno existente.
    """

    consulta = """
        UPDATE turnos
        SET estado = %s
        WHERE id_turno = %s;
    """

    return ejecutar_modificacion(consulta, (nuevo_estado, id_turno))



def obtener_turnos_ocupados_medico(id_medico, fecha):
    """
    Devuelve los horarios ocupados de un médico en una fecha determinada.
    Solo considera turnos pendientes o confirmados.
    """

    consulta = """
        SELECT 
            TIME(fecha_turno) AS hora_ocupada
        FROM turnos
        WHERE medico_id = %s
          AND DATE(fecha_turno) = %s
          AND estado IN ('pendiente', 'confirmado');
    """

    return ejecutar_select(consulta, (id_medico, fecha))


def obtener_disponibilidad_medico_por_dia(id_medico, dia_semana):
    """
    Devuelve la disponibilidad horaria de un médico para un día específico.
    """

    consulta = """
        SELECT 
            hora_inicio,
            hora_fin
        FROM disponibilidad_medica
        WHERE medico_id = %s
          AND dia_semana = %s
          AND activo = TRUE;
    """

    return ejecutar_select(consulta, (id_medico, dia_semana))


def obtener_nombre_dia_semana(fecha):
    """
    Convierte una fecha AAAA-MM-DD al nombre del día usado en la base.
    """

    fecha_convertida = datetime.strptime(fecha, "%Y-%m-%d")

    dias = {
        0: "Lunes",
        1: "Martes",
        2: "Miércoles",
        3: "Jueves",
        4: "Viernes",
        5: "Sábado",
        6: "Domingo",
    }

    return dias[fecha_convertida.weekday()]


def generar_horarios_disponibles(id_medico, fecha):
    """
    Genera los horarios disponibles de un médico para una fecha.

    Usa la disponibilidad médica como agenda base y descarta
    los turnos que ya están ocupados.
    """

    dia_semana = obtener_nombre_dia_semana(fecha)

    disponibilidad = obtener_disponibilidad_medico_por_dia(
        id_medico,
        dia_semana
    )

    if not disponibilidad:
        return []

    turnos_ocupados = obtener_turnos_ocupados_medico(id_medico, fecha)

    horas_ocupadas = set()

    for turno in turnos_ocupados:
        horas_ocupadas.add(str(turno["hora_ocupada"]))

    horarios_disponibles = []

    # Duración fija simplificada para el ABP.
    # Como el schema simplificado no tiene duración_turno_minutos,
    # usamos turnos de 30 minutos.
    duracion_turno = 30

    for bloque in disponibilidad:
        hora_inicio = bloque["hora_inicio"]
        hora_fin = bloque["hora_fin"]

        inicio = datetime.strptime(str(hora_inicio), "%H:%M:%S")
        fin = datetime.strptime(str(hora_fin), "%H:%M:%S")

        horario_actual = inicio

        while horario_actual < fin:
            hora_texto = horario_actual.strftime("%H:%M:%S")

            if hora_texto not in horas_ocupadas:
                horarios_disponibles.append(horario_actual.strftime("%H:%M"))

            horario_actual += timedelta(minutes=duracion_turno)

    return horarios_disponibles

def registrar_turno(id_paciente, id_medico, fecha_turno, motivo_consulta):
    """
    Inserta un nuevo turno con estado pendiente.
    """

    consulta = """
        INSERT INTO turnos (
            paciente_id,
            medico_id,
            empleado_id,
            fecha_turno,
            estado,
            motivo_consulta
        )
        VALUES (%s, %s, NULL, %s, 'pendiente', %s);
    """

    return ejecutar_modificacion(
        consulta,
        (id_paciente, id_medico, fecha_turno, motivo_consulta)
    )

def obtener_nombre_dia_semana(fecha):
    """
    Convierte una fecha AAAA-MM-DD al nombre del día usado en la base.
    """

    fecha_convertida = datetime.strptime(fecha, "%Y-%m-%d")

    dias = {
        0: "Lunes",
        1: "Martes",
        2: "Miércoles",
        3: "Jueves",
        4: "Viernes",
        5: "Sábado",
        6: "Domingo",
    }

    return dias[fecha_convertida.weekday()]


def obtener_turnos_ocupados_medico(id_medico, fecha):
    """
    Devuelve los horarios ocupados de un médico en una fecha determinada.
    Solo considera turnos pendientes o confirmados.
    """

    consulta = """
        SELECT 
            TIME(fecha_turno) AS hora_ocupada
        FROM turnos
        WHERE medico_id = %s
          AND DATE(fecha_turno) = %s
          AND estado IN ('pendiente', 'confirmado');
    """

    return ejecutar_select(consulta, (id_medico, fecha))


def obtener_disponibilidad_medico_por_dia(id_medico, dia_semana):
    """
    Devuelve la disponibilidad horaria de un médico para un día específico.
    """

    consulta = """
        SELECT 
            hora_inicio,
            hora_fin
        FROM disponibilidad_medica
        WHERE medico_id = %s
          AND dia_semana = %s
          AND activo = TRUE;
    """

    return ejecutar_select(consulta, (id_medico, dia_semana))


def generar_horarios_disponibles(id_medico, fecha):
    """
    Genera los horarios disponibles de un médico para una fecha.

    Usa disponibilidad_medica como agenda base y descarta
    los turnos que ya están ocupados.
    """

    dia_semana = obtener_nombre_dia_semana(fecha)

    disponibilidad = obtener_disponibilidad_medico_por_dia(
        id_medico,
        dia_semana
    )

    if not disponibilidad:
        return []

    turnos_ocupados = obtener_turnos_ocupados_medico(id_medico, fecha)

    horas_ocupadas = set()

    for turno in turnos_ocupados:
        horas_ocupadas.add(str(turno["hora_ocupada"]))

    horarios_disponibles = []
    duracion_turno = 30

    for bloque in disponibilidad:
        hora_inicio = bloque["hora_inicio"]
        hora_fin = bloque["hora_fin"]

        inicio = datetime.strptime(str(hora_inicio), "%H:%M:%S")
        fin = datetime.strptime(str(hora_fin), "%H:%M:%S")

        horario_actual = inicio

        while horario_actual < fin:
            hora_texto_completa = horario_actual.strftime("%H:%M:%S")

            if hora_texto_completa not in horas_ocupadas:
                horarios_disponibles.append(horario_actual.strftime("%H:%M"))

            horario_actual += timedelta(minutes=duracion_turno)

    return horarios_disponibles


def obtener_fechas_por_rango(opcion_rango):
    """
    Genera fechas según el rango elegido.

    1 = esta semana
    2 = semana próxima
    3 = próximas 3 semanas
    """

    hoy = datetime.today().date()

    # Lunes de la semana actual
    lunes_actual = hoy - timedelta(days=hoy.weekday())

    if opcion_rango == "1":
        fecha_inicio = hoy
        fecha_fin = lunes_actual + timedelta(days=6)

    elif opcion_rango == "2":
        fecha_inicio = lunes_actual + timedelta(days=7)
        fecha_fin = lunes_actual + timedelta(days=13)

    elif opcion_rango == "3":
        fecha_inicio = hoy
        fecha_fin = hoy + timedelta(days=21)

    else:
        return []

    fechas = []
    fecha_actual = fecha_inicio

    while fecha_actual <= fecha_fin:
        fechas.append(fecha_actual.strftime("%Y-%m-%d"))
        fecha_actual += timedelta(days=1)

    return fechas


def obtener_fechas_con_horarios_disponibles(id_medico, opcion_rango):
    """
    Devuelve únicamente las fechas donde el médico tiene horarios disponibles.
    """

    fechas = obtener_fechas_por_rango(opcion_rango)

    fechas_disponibles = []

    for fecha in fechas:
        horarios = generar_horarios_disponibles(id_medico, fecha)

        if horarios:
            dia_semana = obtener_nombre_dia_semana(fecha)

            fechas_disponibles.append({
                "fecha": fecha,
                "dia": dia_semana,
                "descripcion": f"{dia_semana} {fecha}",
                "horarios": horarios
            })

    return fechas_disponibles