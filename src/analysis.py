import os
from decimal import Decimal

import pandas as pd
import matplotlib.pyplot as plt

from db import ejecutar_consulta


REPORTS_DIR = "reports"
CHARTS_DIR = os.path.join(REPORTS_DIR, "charts")
TABLES_DIR = os.path.join(REPORTS_DIR, "tables")


def crear_carpetas_reportes():
    os.makedirs(CHARTS_DIR, exist_ok=True)
    os.makedirs(TABLES_DIR, exist_ok=True)


def consultar_dataframe(consulta, parametros=None):
    """
    Ejecuta una consulta SQL usando ejecutar_consulta()
    y devuelve un DataFrame de pandas.
    """
    datos = ejecutar_consulta(consulta, parametros)

    if not datos:
        return pd.DataFrame()

    df = pd.DataFrame(datos)

    # Convierte valores Decimal a float para evitar problemas con gráficos/cálculos.
    for columna in df.columns:
        if df[columna].apply(lambda x: isinstance(x, Decimal)).any():
            df[columna] = df[columna].astype(float)

    return df


def guardar_tabla(df, nombre_archivo):
    if df.empty:
        return

    ruta = os.path.join(TABLES_DIR, nombre_archivo)
    df.to_csv(ruta, index=False, encoding="utf-8-sig")
    print(f"Tabla exportada: {ruta}")


def guardar_grafico(nombre_archivo):
    ruta = os.path.join(CHARTS_DIR, nombre_archivo)
    plt.tight_layout()
    plt.savefig(ruta, dpi=150)
    plt.close()
    print(f"Grafico exportado: {ruta}")


def mostrar_titulo(titulo):
    print()
    print("=" * 90)
    print(titulo.upper())
    print("=" * 90)


# ============================================================
# 1. STOCK ACTUAL
# ============================================================

def obtener_stock_actual():
    consulta = """
    SELECT
        v.id_producto,
        v.producto,
        v.categoria,
        v.proveedor,
        v.stock_minimo,
        v.stock_actual,
        v.estado_stock,
        p.precio_costo,
        p.precio_venta,
        (v.stock_actual * p.precio_costo) AS valor_stock_costo,
        (v.stock_actual * p.precio_venta) AS valor_stock_venta,
        (p.precio_venta - p.precio_costo) AS ganancia_unitaria,
        (v.stock_actual * (p.precio_venta - p.precio_costo)) AS ganancia_potencial_stock
    FROM vw_stock_actual_por_producto v
    INNER JOIN productos p
        ON v.id_producto = p.id_producto
    ORDER BY v.producto;
    """

    return consultar_dataframe(consulta)


def analizar_stock_general():
    mostrar_titulo("1. Analisis general de stock")

    df = obtener_stock_actual()

    if df.empty:
        print("No hay datos de stock para analizar.")
        return df

    df["diferencia_con_minimo"] = df["stock_actual"] - df["stock_minimo"]

    guardar_tabla(df, "stock_actual_por_producto.csv")

    print(df[[
        "id_producto",
        "producto",
        "categoria",
        "stock_minimo",
        "stock_actual",
        "diferencia_con_minimo",
        "estado_stock",
        "valor_stock_costo",
        "valor_stock_venta"
    ]])

    total_productos = len(df)
    productos_ok = len(df[df["estado_stock"] == "STOCK_OK"])
    productos_reposicion = len(df[df["estado_stock"] == "REPOSICION_NECESARIA"])
    productos_sin_stock = len(df[df["stock_actual"] <= 0])

    valor_total_costo = df["valor_stock_costo"].sum()
    valor_total_venta = df["valor_stock_venta"].sum()
    ganancia_potencial = df["ganancia_potencial_stock"].sum()

    print()
    print("Indicadores principales:")
    print(f"Total de productos: {total_productos}")
    print(f"Productos con stock OK: {productos_ok}")
    print(f"Productos con reposicion necesaria: {productos_reposicion}")
    print(f"Productos sin stock: {productos_sin_stock}")
    print(f"Valor total del stock a costo: ${valor_total_costo:,.2f}")
    print(f"Valor total del stock a venta: ${valor_total_venta:,.2f}")
    print(f"Ganancia potencial sobre stock actual: ${ganancia_potencial:,.2f}")

    return df


def graficar_estado_stock(df_stock):
    if df_stock.empty:
        return

    resumen = (
        df_stock
        .groupby("estado_stock")
        .size()
        .reset_index(name="cantidad_productos")
    )

    plt.figure(figsize=(8, 5))
    plt.bar(resumen["estado_stock"], resumen["cantidad_productos"])
    plt.title("Cantidad de productos por estado de stock")
    plt.xlabel("Estado de stock")
    plt.ylabel("Cantidad de productos")

    guardar_grafico("01_estado_stock.png")


def graficar_top_stock_actual(df_stock):
    if df_stock.empty:
        return

    df_top = df_stock.sort_values("stock_actual", ascending=False).head(10)

    plt.figure(figsize=(11, 6))
    plt.bar(df_top["producto"], df_top["stock_actual"])
    plt.title("Top 10 productos con mayor stock actual")
    plt.xlabel("Producto")
    plt.ylabel("Stock actual")
    plt.xticks(rotation=45, ha="right")

    guardar_grafico("02_top_stock_actual.png")


def graficar_productos_criticos(df_stock):
    if df_stock.empty:
        return

    df_criticos = (
        df_stock[df_stock["estado_stock"] == "REPOSICION_NECESARIA"]
        .sort_values("diferencia_con_minimo")
        .head(10)
    )

    if df_criticos.empty:
        return

    plt.figure(figsize=(11, 6))
    plt.bar(df_criticos["producto"], df_criticos["diferencia_con_minimo"])
    plt.title("Productos criticos: diferencia contra stock minimo")
    plt.xlabel("Producto")
    plt.ylabel("Stock actual - stock minimo")
    plt.xticks(rotation=45, ha="right")

    guardar_grafico("03_productos_criticos.png")


# ============================================================
# 2. ANALISIS POR CATEGORIA
# ============================================================

def obtener_stock_por_categoria():
    consulta = """
    SELECT
        v.categoria,
        COUNT(v.id_producto) AS cantidad_productos,
        SUM(v.stock_actual) AS unidades_en_stock,
        SUM(v.stock_actual * p.precio_costo) AS valor_stock_costo,
        SUM(v.stock_actual * p.precio_venta) AS valor_stock_venta,
        SUM(v.stock_actual * (p.precio_venta - p.precio_costo)) AS ganancia_potencial
    FROM vw_stock_actual_por_producto v
    INNER JOIN productos p
        ON v.id_producto = p.id_producto
    GROUP BY v.categoria
    ORDER BY valor_stock_costo DESC;
    """

    return consultar_dataframe(consulta)


def analizar_stock_por_categoria():
    mostrar_titulo("2. Analisis de stock por categoria")

    df = obtener_stock_por_categoria()

    if df.empty:
        print("No hay datos por categoria.")
        return df

    guardar_tabla(df, "stock_por_categoria.csv")

    print(df)

    return df


def graficar_valor_stock_categoria(df_categoria):
    if df_categoria.empty:
        return

    plt.figure(figsize=(10, 6))
    plt.bar(df_categoria["categoria"], df_categoria["valor_stock_costo"])
    plt.title("Valor de stock por categoria a precio de costo")
    plt.xlabel("Categoria")
    plt.ylabel("Valor de stock a costo")
    plt.xticks(rotation=45, ha="right")

    guardar_grafico("04_valor_stock_por_categoria.png")


# ============================================================
# 3. MOVIMIENTOS DE STOCK
# ============================================================

def obtener_movimientos_stock():
    consulta = """
    SELECT
        ms.id_movimiento,
        p.nombre AS producto,
        c.nombre AS categoria,
        d.nombre AS deposito,
        tm.nombre AS tipo_movimiento,
        tm.signo,
        ms.cantidad,
        (ms.cantidad * tm.signo) AS impacto_stock,
        CONCAT(u.nombre, ' ', u.apellido) AS usuario,
        ms.fecha_movimiento,
        ms.observacion
    FROM movimientos_stock ms
    INNER JOIN productos p
        ON ms.producto_id = p.id_producto
    INNER JOIN categorias c
        ON p.categoria_id = c.id_categoria
    INNER JOIN depositos d
        ON ms.deposito_id = d.id_deposito
    INNER JOIN tipos_movimiento tm
        ON ms.tipo_movimiento_id = tm.id_tipo_movimiento
    INNER JOIN usuarios u
        ON ms.usuario_id = u.id_usuario
    ORDER BY ms.fecha_movimiento ASC;
    """

    return consultar_dataframe(consulta)


def analizar_movimientos():
    mostrar_titulo("3. Analisis de movimientos de stock")

    df = obtener_movimientos_stock()

    if df.empty:
        print("No hay movimientos de stock.")
        return df

    guardar_tabla(df, "movimientos_stock.csv")

    resumen_tipo = (
        df.groupby(["tipo_movimiento", "signo"])
        .agg(
            cantidad_movimientos=("id_movimiento", "count"),
            unidades_movidas=("cantidad", "sum"),
            impacto_total=("impacto_stock", "sum")
        )
        .reset_index()
        .sort_values("cantidad_movimientos", ascending=False)
    )

    guardar_tabla(resumen_tipo, "movimientos_por_tipo.csv")

    print("Resumen por tipo de movimiento:")
    print(resumen_tipo)

    return df


def graficar_movimientos_por_tipo(df_movimientos):
    if df_movimientos.empty:
        return

    resumen = (
        df_movimientos.groupby("tipo_movimiento")
        .agg(unidades_movidas=("cantidad", "sum"))
        .reset_index()
        .sort_values("unidades_movidas", ascending=False)
    )

    plt.figure(figsize=(10, 6))
    plt.bar(resumen["tipo_movimiento"], resumen["unidades_movidas"])
    plt.title("Unidades movidas por tipo de movimiento")
    plt.xlabel("Tipo de movimiento")
    plt.ylabel("Unidades movidas")
    plt.xticks(rotation=45, ha="right")

    guardar_grafico("05_movimientos_por_tipo.png")


def graficar_movimientos_por_fecha(df_movimientos):
    if df_movimientos.empty:
        return

    df = df_movimientos.copy()
    df["fecha_movimiento"] = pd.to_datetime(df["fecha_movimiento"])
    df["fecha"] = df["fecha_movimiento"].dt.date

    resumen = (
        df.groupby("fecha")
        .agg(impacto_total=("impacto_stock", "sum"))
        .reset_index()
    )

    plt.figure(figsize=(10, 6))
    plt.plot(resumen["fecha"], resumen["impacto_total"], marker="o")
    plt.title("Impacto neto de stock por fecha")
    plt.xlabel("Fecha")
    plt.ylabel("Impacto neto de stock")
    plt.xticks(rotation=45, ha="right")

    guardar_grafico("06_impacto_stock_por_fecha.png")


# ============================================================
# 4. VENTAS Y ROTACION
# ============================================================

def obtener_productos_vendidos():
    consulta = """
    SELECT
        p.id_producto,
        p.nombre AS producto,
        c.nombre AS categoria,
        SUM(dv.cantidad) AS unidades_vendidas,
        SUM(dv.subtotal) AS total_vendido,
        AVG(dv.precio_unitario) AS precio_promedio_venta
    FROM detalle_venta dv
    INNER JOIN productos p
        ON dv.producto_id = p.id_producto
    INNER JOIN categorias c
        ON p.categoria_id = c.id_categoria
    GROUP BY p.id_producto, p.nombre, c.nombre
    ORDER BY unidades_vendidas DESC;
    """

    return consultar_dataframe(consulta)


def analizar_ventas_y_rotacion(df_stock):
    mostrar_titulo("4. Analisis de ventas y rotacion")

    df_ventas = obtener_productos_vendidos()

    if df_ventas.empty:
        print("No hay ventas cargadas.")
        return df_ventas

    guardar_tabla(df_ventas, "productos_vendidos.csv")

    print("Productos mas vendidos:")
    print(df_ventas)

    if not df_stock.empty:
        df_rotacion = df_ventas.merge(
            df_stock[["id_producto", "stock_actual", "stock_minimo"]],
            on="id_producto",
            how="left"
        )

        # Rotacion aproximada:
        # unidades vendidas / (unidades vendidas + stock actual)
        # Da una idea de qué proporción de lo disponible se movió.
        df_rotacion["rotacion_aproximada"] = (
            df_rotacion["unidades_vendidas"] /
            (df_rotacion["unidades_vendidas"] + df_rotacion["stock_actual"])
        )

        df_rotacion = df_rotacion.sort_values("rotacion_aproximada", ascending=False)

        guardar_tabla(df_rotacion, "rotacion_aproximada_productos.csv")

        print()
        print("Rotacion aproximada:")
        print(df_rotacion[[
            "producto",
            "categoria",
            "unidades_vendidas",
            "stock_actual",
            "rotacion_aproximada"
        ]])

        return df_rotacion

    return df_ventas


def graficar_productos_mas_vendidos(df_ventas):
    if df_ventas.empty:
        return

    df_top = df_ventas.sort_values("unidades_vendidas", ascending=False).head(10)

    plt.figure(figsize=(11, 6))
    plt.bar(df_top["producto"], df_top["unidades_vendidas"])
    plt.title("Top productos mas vendidos")
    plt.xlabel("Producto")
    plt.ylabel("Unidades vendidas")
    plt.xticks(rotation=45, ha="right")

    guardar_grafico("07_productos_mas_vendidos.png")


def graficar_ingresos_por_producto(df_ventas):
    if df_ventas.empty:
        return

    df_top = df_ventas.sort_values("total_vendido", ascending=False).head(10)

    plt.figure(figsize=(11, 6))
    plt.bar(df_top["producto"], df_top["total_vendido"])
    plt.title("Top productos por importe vendido")
    plt.xlabel("Producto")
    plt.ylabel("Total vendido")
    plt.xticks(rotation=45, ha="right")

    guardar_grafico("08_importe_vendido_por_producto.png")


# ============================================================
# 5. COMPRAS VS VENTAS
# ============================================================

def obtener_compras_vs_ventas():
    consulta = """
    SELECT
        p.id_producto,
        p.nombre AS producto,
        c.nombre AS categoria,
        COALESCE(compras.unidades_compradas, 0) AS unidades_compradas,
        COALESCE(ventas.unidades_vendidas, 0) AS unidades_vendidas,
        COALESCE(compras.importe_comprado, 0) AS importe_comprado,
        COALESCE(ventas.importe_vendido, 0) AS importe_vendido
    FROM productos p
    INNER JOIN categorias c
        ON p.categoria_id = c.id_categoria
    LEFT JOIN (
        SELECT
            producto_id,
            SUM(cantidad) AS unidades_compradas,
            SUM(subtotal) AS importe_comprado
        FROM detalle_compra
        GROUP BY producto_id
    ) compras
        ON p.id_producto = compras.producto_id
    LEFT JOIN (
        SELECT
            producto_id,
            SUM(cantidad) AS unidades_vendidas,
            SUM(subtotal) AS importe_vendido
        FROM detalle_venta
        GROUP BY producto_id
    ) ventas
        ON p.id_producto = ventas.producto_id
    ORDER BY p.nombre;
    """

    return consultar_dataframe(consulta)


def analizar_compras_vs_ventas():
    mostrar_titulo("5. Analisis de compras vs ventas")

    df = obtener_compras_vs_ventas()

    if df.empty:
        print("No hay datos para comparar compras y ventas.")
        return df

    df["saldo_unidades"] = df["unidades_compradas"] - df["unidades_vendidas"]
    df["diferencia_importe"] = df["importe_vendido"] - df["importe_comprado"]

    guardar_tabla(df, "compras_vs_ventas.csv")

    print(df)

    return df


def graficar_compras_vs_ventas(df_cv):
    if df_cv.empty:
        return

    df_top = df_cv.sort_values("unidades_compradas", ascending=False).head(10)

    x = range(len(df_top))

    plt.figure(figsize=(12, 6))
    plt.bar(x, df_top["unidades_compradas"], width=0.4, label="Compradas")
    plt.bar([i + 0.4 for i in x], df_top["unidades_vendidas"], width=0.4, label="Vendidas")
    plt.title("Comparacion de unidades compradas vs vendidas")
    plt.xlabel("Producto")
    plt.ylabel("Unidades")
    plt.xticks([i + 0.2 for i in x], df_top["producto"], rotation=45, ha="right")
    plt.legend()

    guardar_grafico("09_compras_vs_ventas.png")


# ============================================================
# 6. ALERTAS Y CONCLUSIONES
# ============================================================

def generar_alertas(df_stock, df_rotacion):
    mostrar_titulo("6. Alertas detectadas")

    alertas = []

    if not df_stock.empty:
        sin_stock = df_stock[df_stock["stock_actual"] <= 0]
        bajo_minimo = df_stock[df_stock["estado_stock"] == "REPOSICION_NECESARIA"]

        alertas.append(f"Productos sin stock: {len(sin_stock)}")
        alertas.append(f"Productos con reposicion necesaria: {len(bajo_minimo)}")

        if not sin_stock.empty:
            alertas.append("Productos sin stock detectados:")
            for _, fila in sin_stock.iterrows():
                alertas.append(f"- {fila['producto']} ({fila['categoria']})")

    if not df_rotacion.empty and "rotacion_aproximada" in df_rotacion.columns:
        alta_rotacion = df_rotacion[df_rotacion["rotacion_aproximada"] >= 0.30]

        alertas.append(f"Productos con rotacion aproximada alta: {len(alta_rotacion)}")

        if not alta_rotacion.empty:
            alertas.append("Productos con mayor rotacion:")
            for _, fila in alta_rotacion.head(5).iterrows():
                alertas.append(
                    f"- {fila['producto']}: "
                    f"{fila['unidades_vendidas']} unidades vendidas, "
                    f"rotacion {fila['rotacion_aproximada']:.2%}"
                )

    for alerta in alertas:
        print(alerta)

    return alertas


def generar_conclusiones(df_stock, df_categoria, df_movimientos, df_rotacion, df_cv, alertas):
    mostrar_titulo("7. Conclusiones generales")

    conclusiones = []

    if not df_stock.empty:
        total_productos = len(df_stock)
        productos_reposicion = len(df_stock[df_stock["estado_stock"] == "REPOSICION_NECESARIA"])
        porcentaje_reposicion = (productos_reposicion / total_productos) * 100

        valor_costo = df_stock["valor_stock_costo"].sum()
        valor_venta = df_stock["valor_stock_venta"].sum()

        conclusiones.append(
            f"Se analizaron {total_productos} productos cargados en el catalogo."
        )

        conclusiones.append(
            f"{productos_reposicion} productos requieren reposicion, "
            f"lo que representa el {porcentaje_reposicion:.2f}% del catalogo."
        )

        conclusiones.append(
            f"El valor total del stock disponible a precio de costo es de ${valor_costo:,.2f}."
        )

        conclusiones.append(
            f"El valor potencial del stock a precio de venta es de ${valor_venta:,.2f}."
        )

    if not df_categoria.empty:
        categoria_mayor_valor = df_categoria.iloc[0]

        conclusiones.append(
            f"La categoria con mayor valor de stock a costo es "
            f"{categoria_mayor_valor['categoria']}, con ${categoria_mayor_valor['valor_stock_costo']:,.2f}."
        )

    if not df_movimientos.empty:
        total_movimientos = len(df_movimientos)
        conclusiones.append(
            f"Se registraron {total_movimientos} movimientos de stock entre entradas, salidas y ajustes."
        )

    if not df_rotacion.empty and "rotacion_aproximada" in df_rotacion.columns:
        producto_mayor_rotacion = df_rotacion.iloc[0]

        conclusiones.append(
            f"El producto con mayor rotacion aproximada es {producto_mayor_rotacion['producto']}, "
            f"con una rotacion de {producto_mayor_rotacion['rotacion_aproximada']:.2%}."
        )

    if not df_cv.empty:
        total_comprado = df_cv["importe_comprado"].sum()
        total_vendido = df_cv["importe_vendido"].sum()

        conclusiones.append(
            f"El importe total comprado registrado es de ${total_comprado:,.2f}, "
            f"mientras que el importe total vendido registrado es de ${total_vendido:,.2f}."
        )

    conclusiones.append(
        "El stock actual no se almacena manualmente en la tabla productos; "
        "se calcula a partir de los movimientos de stock, reduciendo el riesgo de inconsistencias."
    )

    if alertas:
        conclusiones.append("Alertas principales detectadas:")
        conclusiones.extend(alertas)

    for conclusion in conclusiones:
        print(f"- {conclusion}")

    ruta = os.path.join(REPORTS_DIR, "conclusiones.txt")

    with open(ruta, "w", encoding="utf-8") as archivo:
        for conclusion in conclusiones:
            archivo.write(f"- {conclusion}\n")

    print()
    print(f"Conclusiones exportadas: {ruta}")


def main():
    crear_carpetas_reportes()

    df_stock = analizar_stock_general()
    graficar_estado_stock(df_stock)
    graficar_top_stock_actual(df_stock)
    graficar_productos_criticos(df_stock)

    df_categoria = analizar_stock_por_categoria()
    graficar_valor_stock_categoria(df_categoria)

    df_movimientos = analizar_movimientos()
    graficar_movimientos_por_tipo(df_movimientos)
    graficar_movimientos_por_fecha(df_movimientos)

    df_rotacion = analizar_ventas_y_rotacion(df_stock)
    graficar_productos_mas_vendidos(df_rotacion)
    graficar_ingresos_por_producto(df_rotacion)

    df_cv = analizar_compras_vs_ventas()
    graficar_compras_vs_ventas(df_cv)

    alertas = generar_alertas(df_stock, df_rotacion)

    generar_conclusiones(
        df_stock=df_stock,
        df_categoria=df_categoria,
        df_movimientos=df_movimientos,
        df_rotacion=df_rotacion,
        df_cv=df_cv,
        alertas=alertas
    )


if __name__ == "__main__":
    main()