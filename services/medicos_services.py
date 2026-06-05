from services.db_services import ejecutar_modificacion , ejecutar_select

# Permite crear un nuevo médico en la base de datos
def crear_medico(nombre, apellido, matricula, telefono, email, especialidad):
    
    consulta = """
    INSERT INTO medicos
    (nombre, apellido, matricula, telefono, email, especialidad)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    return ejecutar_modificacion(consulta, (nombre, apellido, matricula, telefono, email, especialidad))

# Permite buscar un médico por su matrícula
def buscar_medico_por_matricula(matricula):
    consulta = """
        SELECT *
        FROM medicos
        WHERE matricula = %s;
        """
    resultado = ejecutar_select(consulta, (matricula,))

    if resultado:
        return resultado[0]  # Devuelve el primer resultado encontrado
    
    return None  # Si no se encuentra ningún médico con esa matrícula, devuelve None

# Permite listar todos los médicos registrados en la base de datos
def listar_medicos():
    consulta = """
        SELECT 
            id_medico AS ID,
            CONCAT(apellido, ' ', nombre) AS Médico,
            matricula AS Matrícula
        FROM medicos
        ORDER BY apellido, nombre;
        """
    return ejecutar_select(consulta)


def actualizar_medico(matricula,telefono, email):

    consulta = """
        UPDATE medicos
        SET telefono = %s,
            email = %s
        WHERE matricula = %s;
        """
    
    return ejecutar_modificacion(consulta, (telefono, email, matricula))

# Permite eliminar un médico de la base de datos utilizando su matrícula
def eliminar_medico(matricula):
    
    consulta = """
        
        DELETE FROM medicos
        WHERE matricula = %s;
        """
    return ejecutar_modificacion(consulta, (matricula,))
