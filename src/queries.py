from db import ejecutar_consulta


def obtener_proveedores():
    consulta = """
    SELECT 
        id_proveedor,
        nombre,
        cuit,
        telefono,
        email,
        direccion,
        activo
    FROM proveedores
    ORDER BY nombre;
    """

    return ejecutar_consulta(consulta)
    


def obtener_productos():
    consulta = """
    SELECT
        p.id_producto,
        p.nombre AS producto,
        c.nombre AS categoria,
        pr.nombre AS proveedor,
        p.precio_costo,
        p.precio_venta,
        p.stock_minimo,
        p.activo
    FROM productos p
    INNER JOIN categorias c
        ON p.categoria_id = c.id_categoria
    INNER JOIN proveedores pr
        ON p.proveedor_id = pr.id_proveedor
    ORDER BY p.nombre;
    """

    return ejecutar_consulta(consulta)


def obtener_stock_actual():
    consulta = """
    SELECT
        id_producto,
        producto,
        categoria,
        proveedor,
        stock_minimo,
        stock_actual,
        estado_stock
    FROM vw_stock_actual_por_producto
    ORDER BY producto;
    """

    return ejecutar_consulta(consulta)


def obtener_productos_reposicion():
    consulta = """
    SELECT
        id_producto,
        producto,
        categoria,
        proveedor,
        stock_minimo,
        stock_actual,
        estado_stock
    FROM vw_stock_actual_por_producto
    WHERE estado_stock = 'REPOSICION_NECESARIA'
    ORDER BY stock_actual ASC, producto ASC;
    """

    return ejecutar_consulta(consulta)


def obtener_movimientos_stock():
    consulta = """
    SELECT
        ms.id_movimiento,
        p.nombre AS producto,
        d.nombre AS deposito,
        tm.nombre AS tipo_movimiento,
        tm.signo,
        ms.cantidad,
        (ms.cantidad * tm.signo) AS impacto_stock,
        u.nombre AS usuario_nombre,
        u.apellido AS usuario_apellido,
        ms.fecha_movimiento,
        ms.observacion
    FROM movimientos_stock ms
    INNER JOIN productos p
        ON ms.producto_id = p.id_producto
    INNER JOIN depositos d
        ON ms.deposito_id = d.id_deposito
    INNER JOIN tipos_movimiento tm
        ON ms.tipo_movimiento_id = tm.id_tipo_movimiento
    INNER JOIN usuarios u
        ON ms.usuario_id = u.id_usuario
    ORDER BY ms.fecha_movimiento DESC;
    """

    return ejecutar_consulta(consulta)


def obtener_stock_por_deposito():
    consulta = """
    SELECT
        producto,
        deposito,
        stock_actual
    FROM vw_stock_actual_por_deposito
    WHERE deposito IS NOT NULL
    ORDER BY producto, deposito;
    """

    return ejecutar_consulta(consulta)


def obtener_resumen_por_estado_stock():
    consulta = """
    SELECT
        estado_stock,
        COUNT(*) AS cantidad_productos
    FROM vw_stock_actual_por_producto
    GROUP BY estado_stock;
    """

    return ejecutar_consulta(consulta)


def buscar_producto_por_nombre(nombre_producto):
    consulta = """
    SELECT
        id_producto,
        producto,
        categoria,
        proveedor,
        stock_minimo,
        stock_actual,
        estado_stock
    FROM vw_stock_actual_por_producto
    WHERE producto LIKE %s
    ORDER BY producto;
    """

    parametro = (f"%{nombre_producto}%",)

    return ejecutar_consulta(consulta, parametro)



def obtener_stock_actual():
    consulta = """
    SELECT
        id_producto,
        producto,
        categoria,
        proveedor,
        stock_minimo,
        stock_actual,
        estado_stock
    FROM vw_stock_actual_por_producto
    ORDER BY producto;
    """

    return ejecutar_consulta(consulta)


def obtener_productos_reposicion():
    consulta = """
    SELECT
        id_producto,
        producto,
        categoria,
        proveedor,
        stock_minimo,
        stock_actual,
        estado_stock
    FROM vw_stock_actual_por_producto
    WHERE estado_stock = 'REPOSICION_NECESARIA'
    ORDER BY stock_actual ASC, producto ASC;
    """

    return ejecutar_consulta(consulta)


def obtener_resumen_estado_stock():
    consulta = """
    SELECT
        estado_stock,
        COUNT(*) AS cantidad_productos
    FROM vw_stock_actual_por_producto
    GROUP BY estado_stock;
    """

    return ejecutar_consulta(consulta)


def obtener_movimientos_por_tipo():
    consulta = """
    SELECT
        tm.nombre AS tipo_movimiento,
        tm.signo,
        COUNT(ms.id_movimiento) AS cantidad_movimientos,
        SUM(ms.cantidad) AS unidades_movidas
    FROM movimientos_stock ms
    INNER JOIN tipos_movimiento tm
        ON ms.tipo_movimiento_id = tm.id_tipo_movimiento
    GROUP BY tm.nombre, tm.signo
    ORDER BY cantidad_movimientos DESC;
    """

    return ejecutar_consulta(consulta)


def obtener_productos_mas_vendidos():
    consulta = """
    SELECT
        p.nombre AS producto,
        c.nombre AS categoria,
        SUM(dv.cantidad) AS unidades_vendidas,
        SUM(dv.subtotal) AS total_vendido
    FROM detalle_venta dv
    INNER JOIN productos p
        ON dv.producto_id = p.id_producto
    INNER JOIN categorias c
        ON p.categoria_id = c.id_categoria
    GROUP BY p.nombre, c.nombre
    ORDER BY unidades_vendidas DESC;
    """

    return ejecutar_consulta(consulta)


def obtener_valor_stock_por_producto():
    consulta = """
    SELECT
        v.id_producto,
        v.producto,
        v.categoria,
        v.proveedor,
        v.stock_actual,
        p.precio_costo,
        p.precio_venta,
        (v.stock_actual * p.precio_costo) AS valor_stock_costo,
        (v.stock_actual * p.precio_venta) AS valor_stock_venta
    FROM vw_stock_actual_por_producto v
    INNER JOIN productos p
        ON v.id_producto = p.id_producto
    ORDER BY valor_stock_costo DESC;
    """

    return ejecutar_consulta(consulta)


def obtener_stock_por_categoria():
    consulta = """
    SELECT
        v.categoria,
        COUNT(v.id_producto) AS cantidad_productos,
        SUM(v.stock_actual) AS unidades_stock,
        SUM(v.stock_actual * p.precio_costo) AS valor_stock_costo,
        SUM(v.stock_actual * p.precio_venta) AS valor_stock_venta
    FROM vw_stock_actual_por_producto v
    INNER JOIN productos p
        ON v.id_producto = p.id_producto
    GROUP BY v.categoria
    ORDER BY valor_stock_costo DESC;
    """

    return ejecutar_consulta(consulta)