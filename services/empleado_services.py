from services.db_services import ejecutar_modificacion , ejecutar_select

# Permite crear un nuevo empleado en la base de datos
def crear_empleado(nombre, apellido, dni, rol):
    
    consulta = """
    INSERT INTO empleados
    (nombre, apellido, dni, rol)
    VALUES (%s, %s, %s, %s)
    """

    return ejecutar_modificacion(consulta, (nombre, apellido, dni, rol))

# Permite buscar un empleado por su DNI
def buscar_empleado_por_dni(dni):
    consulta = """
        SELECT *
        FROM empleados
        WHERE dni = %s;
        """
    resultado = ejecutar_select(consulta, (dni,))

    if resultado:
        return resultado[0]  # Devuelve el primer resultado encontrado
    
    return None  # Si no se encuentra ningún empleado con ese DNI, devuelve None

# Permite listar todos los empleados registrados en la base de datos
def listar_empleados():
    consulta = """
        SELECT 
            id_empleado AS ID,
            CONCAT(nombre, ' ', apellido) AS Empleado,
            dni AS DNI,
            activo AS Activo
        FROM empleados
        WHERE activo = TRUE
        ORDER BY apellido, nombre;
        """
    return ejecutar_select(consulta)


def actualizar_empleado(dni, rol, activo):
    consulta = """
        UPDATE empleados
        SET rol = %s,
            activo = %s
        WHERE dni = %s;
        """
    
    return ejecutar_modificacion(consulta, (rol, activo, dni))

# Permite eliminar un empleado de la base de datos utilizando su DNI
def eliminar_empleado(dni):
    
    consulta = """
        UPDATE empleados
        SET activo = FALSE
        WHERE dni = %s;
        """
    
    return ejecutar_modificacion(consulta, (dni,))
