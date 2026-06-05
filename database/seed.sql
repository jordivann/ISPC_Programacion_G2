USE turnos_medicos;

-- ============================================================
-- SEED DE DATOS
-- Carga información inicial para probar consultas SELECT,
-- filtros, relaciones y reportes simples.
-- ============================================================


-- ============================================================
-- 1. PACIENTES
-- Pacientes de ejemplo para buscar por DNI y consultar turnos.
-- ============================================================

use turnos_medicos;
INSERT INTO pacientes (
    nombre,
    apellido,
    dni,
    fecha_nacimiento,
    telefono,
    email,
    direccion
)
VALUES
('Juan', 'Pérez', '40111222', '1992-04-15', '3516001001', 'juan.perez@email.com', 'Av. Colón 123'),
('María', 'Gómez', '38222333', '1988-09-22', '3516001002', 'maria.gomez@email.com', 'Bv. San Juan 456'),
('Carlos', 'Ramírez', '35999888', '1979-01-10', '3516001003', 'carlos.ramirez@email.com', 'Laprida 789'),
('Lucía', 'Torres', '42777111', '1997-06-05', '3516001004', 'lucia.torres@email.com', 'Obispo Trejo 321'),
('Sofía', 'Molina', '44555123', '2001-11-30', '3516001005', 'sofia.molina@email.com', 'Chacabuco 654'),
('Diego', 'Herrera', '33666111', '1985-03-18', '3516001006', 'diego.herrera@email.com', 'Santa Rosa 987'),
('Valentina', 'Castro', '39888777', '1990-12-02', '3516001007', 'valentina.castro@email.com', 'General Paz 147'),
('Ricardo', 'López', '28777444', '1972-08-25', '3516001008', 'ricardo.lopez@email.com', 'Dean Funes 258'),
('Camila', 'Navarro', '42123999', '1996-05-14', '3516001009', 'camila.navarro@email.com', 'Ituzaingó 369'),
('Andrés', 'Moreno', '37555444', '1989-10-08', '3516001010', 'andres.moreno@email.com', 'Maipú 741');


-- ============================================================
-- 2. MÉDICOS
-- Cada médico se vincula con una especialidad mediante id_especialidad.
--
-- IDs esperados:
-- 1 = Cardiología
-- 2 = Pediatría
-- 3 = Dermatología
-- 4 = Traumatología
-- ============================================================

INSERT INTO medicos (
    nombre,
    apellido,
    matricula,
    telefono,
    especialidad
)
VALUES
-- Cardiología
('Ana', 'Paredes', 'MP-1001', '3517001001', 'Cardiología'),
('Roberto', 'Silva', 'MP-1002', '3517001002', 'Cardiología'),
('Carolina', 'Vega', 'MP-1003', '3517001003', 'Cardiología'),

-- Pediatría
('Gabriel', 'Ríos', 'MP-2001', '3517002001', 'Pediatría'),
('Paula', 'Medina', 'MP-2002', '3517002002', 'Pediatría'),
('Florencia', 'Acuña', 'MP-2003', '3517002003','Pediatría'),

-- Dermatología
('Santiago', 'Ortega', 'MP-3001', '3517003001', 'Dermatología'),
('Julieta', 'Luna', 'MP-3002', '3517003002', 'Dermatología'),

-- Traumatología
('Miguel', 'Campos', 'MP-4001', '3517004001', 'Traumatología'),
('Daniela', 'Fuentes', 'MP-4002', '3517004002', 'Traumatología'),
('Hernán', 'Sosa', 'MP-4003', '3517004003', 'Traumatología');


-- ============================================================
-- 4. TURNOS
-- Turnos de ejemplo para consultar por paciente, médico,
-- especialidad, fecha o estado.
-- ============================================================

INSERT INTO turnos (
    paciente_id,
    medico_id,
    fecha_turno,
    estado,
    motivo_consulta
)
VALUES
-- Cardiología
(1, 1,  '2026-06-03 08:30:00', 'pendiente', 'Chequeo general cardiológico'),
(2, 1,     '2026-06-03 09:00:00', 'confirmado', 'Control de presión arterial'),
(3, 2,    '2026-06-04 14:30:00', 'confirmado', 'Dolor en el pecho'),

-- Pediatría
(4, 4,  '2026-06-03 09:20:00', 'pendiente', 'Control pediátrico'),
(5, 5,     '2026-06-04 08:30:00', 'confirmado', 'Fiebre y malestar general'),
(6, 6, '2026-06-05 15:00:00', 'pendiente', 'Consulta pediátrica'),

-- Dermatología
(7, 7,     '2026-06-04 15:30:00', 'confirmado', 'Revisión de manchas en la piel'),
(8, 8,  '2026-06-05 10:30:00', 'pendiente', 'Consulta por irritación'),

-- Traumatología
(9, 9,      '2026-06-03 15:00:00', 'confirmado', 'Dolor de rodilla'),
(10, 10, '2026-06-04 09:30:00', 'pendiente', 'Dolor lumbar'),
(1, 11,     '2026-06-05 08:30:00', 'confirmado', 'Control de esguince'),

-- Turnos históricos para reportes
(2, 3,     '2026-05-20 10:00:00', 'atendido', 'Control cardiológico realizado'),
(3, 7,     '2026-05-21 16:00:00', 'ausente', 'Consulta dermatológica no asistida'),
(4, 9,  '2026-05-22 09:00:00', 'cancelado', 'Turno cancelado por el paciente');

