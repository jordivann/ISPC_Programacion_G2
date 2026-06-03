from services.db_services import ejecutar_select


def reporte_turnos_por_estado():
    consulta = """
        SELECT 
            estado AS Estado,
            COUNT(*) AS Cantidad
        FROM turnos
        GROUP BY estado
        ORDER BY Cantidad DESC;
    """

    return ejecutar_select(consulta)


def reporte_turnos_por_especialidad():
    consulta = """
        SELECT 
            e.nombre AS Especialidad,
            COUNT(t.id_turno) AS `Cantidad Turnos`
        FROM turnos t
        INNER JOIN medicos m
            ON t.medico_id = m.id_medico
        INNER JOIN especialidades e
            ON m.id_especialidad = e.id_especialidad
        GROUP BY e.id_especialidad, e.nombre
        ORDER BY `Cantidad Turnos` DESC;
    """

    return ejecutar_select(consulta)