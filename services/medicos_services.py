from services.db_services import ejecutar_select


def listar_especialidades():
    consulta = """
        SELECT 
            id_especialidad AS ID,
            nombre AS Especialidad,
            descripcion AS Descripcion
        FROM especialidades
        ORDER BY nombre;
    """

    return ejecutar_select(consulta)


def obtener_especialidades_resumidas():
    consulta = """
        SELECT 
            id_especialidad AS ID,
            nombre AS Especialidad
        FROM especialidades
        ORDER BY nombre;
    """

    return ejecutar_select(consulta)


def listar_medicos():
    consulta = """
        SELECT 
            m.id_medico AS ID,
            CONCAT(m.nombre, ' ', m.apellido) AS Medico,
            m.matricula AS Matricula,
            m.telefono AS Telefono,
            e.nombre AS Especialidad
        FROM medicos m
        INNER JOIN especialidades e
            ON m.id_especialidad = e.id_especialidad
        ORDER BY e.nombre, m.apellido, m.nombre;
    """

    return ejecutar_select(consulta)


def obtener_medicos_resumidos():
    consulta = """
        SELECT 
            m.id_medico AS ID,
            CONCAT(m.nombre, ' ', m.apellido) AS Medico,
            e.nombre AS Especialidad
        FROM medicos m
        INNER JOIN especialidades e
            ON m.id_especialidad = e.id_especialidad
        ORDER BY e.nombre, m.apellido, m.nombre;
    """

    return ejecutar_select(consulta)


def buscar_medicos_por_especialidad(id_especialidad):
    consulta = """
        SELECT 
            m.id_medico AS ID,
            CONCAT(m.nombre, ' ', m.apellido) AS Medico,
            m.matricula AS Matricula,
            m.telefono AS Telefono,
            m.email AS Email,
            e.nombre AS Especialidad
        FROM medicos m
        INNER JOIN especialidades e
            ON m.id_especialidad = e.id_especialidad
        WHERE e.id_especialidad = %s
        ORDER BY m.apellido, m.nombre;
    """

    return ejecutar_select(consulta, (id_especialidad,))


def ver_disponibilidad_por_medico(id_medico):
    consulta = """
        SELECT 
            CONCAT(m.nombre, ' ', m.apellido) AS Medico,
            e.nombre AS Especialidad,
            d.dia_semana AS Dia,
            d.hora_inicio AS Desde,
            d.hora_fin AS Hasta,
            d.activo AS Activo
        FROM disponibilidad_medica d
        INNER JOIN medicos m
            ON d.medico_id = m.id_medico
        INNER JOIN especialidades e
            ON m.id_especialidad = e.id_especialidad
        WHERE d.medico_id = %s
        ORDER BY d.dia_semana, d.hora_inicio;
    """

    return ejecutar_select(consulta, (id_medico,))


def ver_disponibilidad_por_especialidad(id_especialidad):
    consulta = """
        SELECT 
            e.nombre AS Especialidad,
            CONCAT(m.nombre, ' ', m.apellido) AS Medico,
            d.dia_semana AS Dia,
            d.hora_inicio AS Desde,
            d.hora_fin AS Hasta
        FROM medicos m
        INNER JOIN especialidades e
            ON m.id_especialidad = e.id_especialidad
        INNER JOIN disponibilidad_medica d
            ON m.id_medico = d.medico_id
        WHERE e.id_especialidad = %s
          AND d.activo = TRUE
        ORDER BY m.apellido, m.nombre, d.dia_semana, d.hora_inicio;
    """

    return ejecutar_select(consulta, (id_especialidad,))