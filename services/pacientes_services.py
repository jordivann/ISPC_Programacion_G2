from services.db_services import ejecutar_select


def listar_pacientes():
    consulta = """
        SELECT 
            id_paciente AS ID,
            nombre AS Nombre,
            apellido AS Apellido,
            dni AS DNI,
            telefono AS Telefono,
            email AS Email
        FROM pacientes
        ORDER BY apellido, nombre;
    """

    return ejecutar_select(consulta)


def buscar_paciente_por_dni(dni):
    consulta = """
        SELECT 
            id_paciente AS ID,
            nombre AS Nombre,
            apellido AS Apellido,
            dni AS DNI,
            fecha_nacimiento AS FechaNacimiento,
            telefono AS Telefono,
            email AS Email,
            direccion AS Direccion
        FROM pacientes
        WHERE dni = %s;
    """

    return ejecutar_select(consulta, (dni,))


def obtener_pacientes_resumidos():
    consulta = """
        SELECT 
            id_paciente AS ID,
            CONCAT(nombre, ' ', apellido) AS Paciente,
            dni AS DNI
        FROM pacientes
        ORDER BY apellido, nombre;
    """

    return ejecutar_select(consulta)