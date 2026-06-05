from services.db_services import ejecutar_modificacion, ejecutar_select


def crear_paciente(nombre, apellido, dni, fecha_nacimiento, telefono, email, direccion):
    consulta = """
    INSERT INTO pacientes
    (nombre, apellido, dni, fecha_nacimiento, telefono, email, direccion)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    return ejecutar_modificacion(
        consulta,
        (nombre, apellido, dni, fecha_nacimiento, telefono, email, direccion)
    )


def buscar_paciente_por_dni(dni):
    consulta = """
        SELECT *
        FROM pacientes
        WHERE dni = %s;
    """

    resultado = ejecutar_select(consulta, (dni,))

    if resultado:
        return resultado[0]

    return None


def listar_pacientes():
    consulta = """
        SELECT
            id_paciente AS ID,
            CONCAT(apellido, ' ', nombre) AS Paciente,
            dni AS DNI
        FROM pacientes
        ORDER BY apellido, nombre;
    """

    return ejecutar_select(consulta)


def actualizar_paciente(id_paciente, telefono, direccion):
    consulta = """
        UPDATE pacientes
        SET telefono = %s,
            direccion = %s
        WHERE id_paciente = %s;
    """

    return ejecutar_modificacion(
        consulta,
        (telefono, direccion, id_paciente)
    )


def eliminar_paciente(dni):
    consulta = """
        DELETE FROM pacientes
        WHERE dni = %s;
    """

    return ejecutar_modificacion(consulta, (dni,))