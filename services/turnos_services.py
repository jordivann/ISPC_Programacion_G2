from services.db_services import ejecutar_select, ejecutar_modificacion

def crear_turno(
    paciente_id,
    medico_id,
    empleado_id,
    fecha_turno,
    motivo_consulta
):

    consulta = """
    INSERT INTO turnos
    (
        paciente_id,
        medico_id,
        empleado_id,
        fecha_turno,
        motivo_consulta
    )
    VALUES (%s, %s, %s, %s, %s)
    """

    return ejecutar_modificacion(
        consulta,
        (
            paciente_id,
            medico_id,
            empleado_id,
            fecha_turno,
            motivo_consulta
        )
    )
#Permite listar todos los turnos registrados en la base de datos, mostrando información relevante del paciente, médico y fecha del turno
def listar_turnos():
    consulta = """
    SELECT 
        t.id_turno AS ID,
        CONCAT(p.nombre, ' ', p.apellido) AS Paciente,
        CONCAT(m.nombre, ' ', m.apellido) AS Médico,
        t.fecha_turno AS Fecha,
        t.motivo_consulta AS Motivo,
        t.estado AS Estado
    FROM turnos t
    INNER JOIN pacientes p ON t.paciente_id = p.id_paciente
    INNER JOIN medicos m ON t.medico_id = m.id_medico
    ORDER BY t.fecha_turno DESC;
    """
    return ejecutar_select(consulta)

# Permite cancelar un turno de la base de datos utilizando su ID
def cancelar_turno(id_turno):
    consulta = """
    DELETE FROM turnos
    WHERE id_turno = %s;
    """
    return ejecutar_modificacion(consulta, (id_turno,))

# Permite cambiar el estado de un turno (por ejemplo, de "pendiente" a "completado" o "cancelado")
def cambiar_estado_turno(id_turno, nuevo_estado):
    consulta = """
    UPDATE turnos
    SET estado = %s
    WHERE id_turno = %s;
    """
    return ejecutar_modificacion(consulta, (nuevo_estado, id_turno))