CREATE DATABASE proyecto_prueba;

USE proyecto_prueba;
-- ============================================================
-- PROYECTO: Sistema de Gestión y Análisis de Stock
-- BASE DE DATOS: stock_data_lab


-- ============================================================
-- 1. TABLA: categorias
-- Guarda las familias o grupos de productos.
-- Ej: Alimentos, Bebidas, Limpieza, Herramientas.
-- ============================================================

CREATE TABLE categorias (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(255),
    activo BOOLEAN NOT NULL DEFAULT TRUE,

    CONSTRAINT uk_categorias_nombre UNIQUE (nombre)
);


-- ============================================================
-- 2. TABLA: proveedores
-- Guarda las empresas o personas que abastecen productos.
-- ============================================================

CREATE TABLE proveedores (
    id_proveedor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL,
    cuit VARCHAR(20),
    telefono VARCHAR(30),
    email VARCHAR(120),
    direccion VARCHAR(255),
    activo BOOLEAN NOT NULL DEFAULT TRUE,

    CONSTRAINT uk_proveedores_nombre UNIQUE (nombre),
    CONSTRAINT uk_proveedores_cuit UNIQUE (cuit)
);


-- ============================================================
-- 3. TABLA: productos
-- Guarda el catálogo de productos.
-- NO guarda stock_actual.
-- El stock actual se calcula desde movimientos_stock.
-- ============================================================

CREATE TABLE productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL,
    descripcion VARCHAR(255),
    categoria_id INT NOT NULL,
    proveedor_id INT NOT NULL,
    precio_costo DECIMAL(12,2) NOT NULL,
    precio_venta DECIMAL(12,2) NOT NULL,
    stock_minimo INT NOT NULL DEFAULT 0,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    fecha_alta DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uk_productos_nombre UNIQUE (nombre),

    CONSTRAINT fk_productos_categoria
        FOREIGN KEY (categoria_id)
        REFERENCES categorias(id_categoria)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_productos_proveedor
        FOREIGN KEY (proveedor_id)
        REFERENCES proveedores(id_proveedor)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT chk_productos_precio_costo
        CHECK (precio_costo >= 0),

    CONSTRAINT chk_productos_precio_venta
        CHECK (precio_venta >= 0),

    CONSTRAINT chk_productos_stock_minimo
        CHECK (stock_minimo >= 0)
);


-- ============================================================
-- 4. TABLA: depositos
-- Guarda los lugares físicos donde puede existir stock.
-- ============================================================

CREATE TABLE depositos (
    id_deposito INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(255),
    descripcion VARCHAR(255),
    activo BOOLEAN NOT NULL DEFAULT TRUE,

    CONSTRAINT uk_depositos_nombre UNIQUE (nombre)
);


-- ============================================================
-- 5. TABLA: usuarios
-- Guarda quién registra compras, ventas o movimientos.
-- No representa necesariamente un login real.
-- ============================================================

CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(120),
    rol VARCHAR(60) NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE,

    CONSTRAINT uk_usuarios_email UNIQUE (email)
);


-- ============================================================
-- 6. TABLA: tipos_movimiento
-- Define si un movimiento suma o resta stock.
-- signo = 1  -> suma stock
-- signo = -1 -> resta stock
-- ============================================================

CREATE TABLE tipos_movimiento (
    id_tipo_movimiento INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(255),
    signo TINYINT NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE,

    CONSTRAINT uk_tipos_movimiento_nombre UNIQUE (nombre),

    CONSTRAINT chk_tipos_movimiento_signo
        CHECK (signo IN (1, -1))
);


-- ============================================================
-- 7. TABLA: compras
-- Encabezado de una compra realizada a un proveedor.
-- Los productos comprados van en detalle_compra.
-- ============================================================

CREATE TABLE compras (
    id_compra INT AUTO_INCREMENT PRIMARY KEY,
    proveedor_id INT NOT NULL,
    usuario_id INT NOT NULL,
    fecha_compra DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    numero_comprobante VARCHAR(80),
    total DECIMAL(12,2) NOT NULL DEFAULT 0,
    observacion VARCHAR(255),

    CONSTRAINT fk_compras_proveedor
        FOREIGN KEY (proveedor_id)
        REFERENCES proveedores(id_proveedor)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_compras_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id_usuario)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT chk_compras_total
        CHECK (total >= 0)
);


-- ============================================================
-- 8. TABLA: ventas
-- Encabezado de una venta.
-- Los productos vendidos van en detalle_venta.
-- ============================================================

CREATE TABLE ventas (
    id_venta INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    fecha_venta DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    cliente_nombre VARCHAR(120) NOT NULL DEFAULT 'Consumidor final',
    numero_comprobante VARCHAR(80),
    total DECIMAL(12,2) NOT NULL DEFAULT 0,
    observacion VARCHAR(255),

    CONSTRAINT fk_ventas_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id_usuario)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT chk_ventas_total
        CHECK (total >= 0)
);


-- ============================================================
-- 9. TABLA: detalle_compra
-- Productos incluidos dentro de una compra.
-- Resuelve la relación N a N entre compras y productos.
-- ============================================================

CREATE TABLE detalle_compra (
    id_detalle_compra INT AUTO_INCREMENT PRIMARY KEY,
    compra_id INT NOT NULL,
    producto_id INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(12,2) NOT NULL,
    subtotal DECIMAL(12,2) NOT NULL,

    CONSTRAINT fk_detalle_compra_compra
        FOREIGN KEY (compra_id)
        REFERENCES compras(id_compra)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_detalle_compra_producto
        FOREIGN KEY (producto_id)
        REFERENCES productos(id_producto)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT chk_detalle_compra_cantidad
        CHECK (cantidad > 0),

    CONSTRAINT chk_detalle_compra_precio_unitario
        CHECK (precio_unitario >= 0),

    CONSTRAINT chk_detalle_compra_subtotal
        CHECK (subtotal >= 0)
);


-- ============================================================
-- 10. TABLA: detalle_venta
-- Productos incluidos dentro de una venta.
-- Resuelve la relación N a N entre ventas y productos.
-- ============================================================

CREATE TABLE detalle_venta (
    id_detalle_venta INT AUTO_INCREMENT PRIMARY KEY,
    venta_id INT NOT NULL,
    producto_id INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(12,2) NOT NULL,
    subtotal DECIMAL(12,2) NOT NULL,

    CONSTRAINT fk_detalle_venta_venta
        FOREIGN KEY (venta_id)
        REFERENCES ventas(id_venta)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_detalle_venta_producto
        FOREIGN KEY (producto_id)
        REFERENCES productos(id_producto)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT chk_detalle_venta_cantidad
        CHECK (cantidad > 0),

    CONSTRAINT chk_detalle_venta_precio_unitario
        CHECK (precio_unitario >= 0),

    CONSTRAINT chk_detalle_venta_subtotal
        CHECK (subtotal >= 0)
) ;


-- ============================================================
-- 11. TABLA: movimientos_stock
-- Tabla central del sistema.
-- Registra cada entrada, salida o ajuste de stock.
--
-- cantidad siempre se guarda positiva.
-- El impacto real se calcula como:
-- cantidad * tipos_movimiento.signo
-- ============================================================

CREATE TABLE movimientos_stock (
    id_movimiento INT AUTO_INCREMENT PRIMARY KEY,
    producto_id INT NOT NULL,
    deposito_id INT NOT NULL,
    tipo_movimiento_id INT NOT NULL,
    usuario_id INT NOT NULL,
    cantidad INT NOT NULL,
    fecha_movimiento DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    observacion VARCHAR(255),

    compra_id INT NULL,
    venta_id INT NULL,

    CONSTRAINT fk_movimientos_producto
        FOREIGN KEY (producto_id)
        REFERENCES productos(id_producto)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_movimientos_deposito
        FOREIGN KEY (deposito_id)
        REFERENCES depositos(id_deposito)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_movimientos_tipo_movimiento
        FOREIGN KEY (tipo_movimiento_id)
        REFERENCES tipos_movimiento(id_tipo_movimiento)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_movimientos_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id_usuario)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_movimientos_compra
        FOREIGN KEY (compra_id)
        REFERENCES compras(id_compra)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    CONSTRAINT fk_movimientos_venta
        FOREIGN KEY (venta_id)
        REFERENCES ventas(id_venta)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    CONSTRAINT chk_movimientos_cantidad
        CHECK (cantidad > 0)
);


-- ============================================================
-- ÍNDICES RECOMENDADOS
-- Ayudan a mejorar consultas frecuentes.
-- ============================================================

CREATE INDEX idx_productos_categoria
ON productos(categoria_id);

CREATE INDEX idx_productos_proveedor
ON productos(proveedor_id);

CREATE INDEX idx_compras_proveedor
ON compras(proveedor_id);

CREATE INDEX idx_compras_usuario
ON compras(usuario_id);

CREATE INDEX idx_ventas_usuario
ON ventas(usuario_id);

CREATE INDEX idx_detalle_compra_compra
ON detalle_compra(compra_id);

CREATE INDEX idx_detalle_compra_producto
ON detalle_compra(producto_id);

CREATE INDEX idx_detalle_venta_venta
ON detalle_venta(venta_id);

CREATE INDEX idx_detalle_venta_producto
ON detalle_venta(producto_id);

CREATE INDEX idx_movimientos_producto
ON movimientos_stock(producto_id);

CREATE INDEX idx_movimientos_deposito
ON movimientos_stock(deposito_id);

CREATE INDEX idx_movimientos_tipo
ON movimientos_stock(tipo_movimiento_id);

CREATE INDEX idx_movimientos_usuario
ON movimientos_stock(usuario_id);

CREATE INDEX idx_movimientos_fecha
ON movimientos_stock(fecha_movimiento);


-- ============================================================
-- VISTA: vw_stock_actual_por_producto
-- Calcula el stock total actual por producto.
-- ============================================================

CREATE OR REPLACE VIEW vw_stock_actual_por_producto AS
SELECT
    p.id_producto,
    p.nombre AS producto,
    c.nombre AS categoria,
    pr.nombre AS proveedor,
    p.stock_minimo,
    COALESCE(SUM(ms.cantidad * tm.signo), 0) AS stock_actual,
    CASE
        WHEN COALESCE(SUM(ms.cantidad * tm.signo), 0) <= p.stock_minimo
            THEN 'REPOSICION_NECESARIA'
        ELSE 'STOCK_OK'
    END AS estado_stock
FROM productos p
INNER JOIN categorias c
    ON p.categoria_id = c.id_categoria
INNER JOIN proveedores pr
    ON p.proveedor_id = pr.id_proveedor
LEFT JOIN movimientos_stock ms
    ON p.id_producto = ms.producto_id
LEFT JOIN tipos_movimiento tm
    ON ms.tipo_movimiento_id = tm.id_tipo_movimiento
GROUP BY
    p.id_producto,
    p.nombre,
    c.nombre,
    pr.nombre,
    p.stock_minimo;


-- ============================================================
-- VISTA: vw_stock_actual_por_deposito
-- Calcula el stock actual por producto y por depósito.
-- ============================================================

CREATE OR REPLACE VIEW vw_stock_actual_por_deposito AS
SELECT
    p.id_producto,
    p.nombre AS producto,
    d.id_deposito,
    d.nombre AS deposito,
    COALESCE(SUM(ms.cantidad * tm.signo), 0) AS stock_actual
FROM productos p
LEFT JOIN movimientos_stock ms
    ON p.id_producto = ms.producto_id
LEFT JOIN tipos_movimiento tm
    ON ms.tipo_movimiento_id = tm.id_tipo_movimiento
LEFT JOIN depositos d
    ON ms.deposito_id = d.id_deposito
GROUP BY
    p.id_producto,
    p.nombre,
    d.id_deposito,
    d.nombre;