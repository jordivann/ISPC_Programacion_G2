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
-- 2. ESPECIALIDADES
-- Especialidades disponibles en la clínica.
-- ============================================================

INSERT INTO especialidades (
    nombre,
    descripcion
)
VALUES
('Cardiología', 'Diagnóstico y tratamiento de enfermedades del corazón.'),
('Pediatría', 'Atención médica de niños y adolescentes.'),
('Dermatología', 'Diagnóstico y tratamiento de enfermedades de la piel.'),
('Traumatología', 'Tratamiento de lesiones óseas, articulares y musculares.');


-- ============================================================
-- 3. MÉDICOS
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
    email,
    id_especialidad
)
VALUES
-- Cardiología
('Ana', 'Paredes', 'MP-1001', '3517001001', 'ana.paredes@clinica.com', 1),
('Roberto', 'Silva', 'MP-1002', '3517001002', 'roberto.silva@clinica.com', 1),
('Carolina', 'Vega', 'MP-1003', '3517001003', 'carolina.vega@clinica.com', 1),

-- Pediatría
('Gabriel', 'Ríos', 'MP-2001', '3517002001', 'gabriel.rios@clinica.com', 2),
('Paula', 'Medina', 'MP-2002', '3517002002', 'paula.medina@clinica.com', 2),
('Florencia', 'Acuña', 'MP-2003', '3517002003', 'florencia.acuna@clinica.com', 2),

-- Dermatología
('Santiago', 'Ortega', 'MP-3001', '3517003001', 'santiago.ortega@clinica.com', 3),
('Julieta', 'Luna', 'MP-3002', '3517003002', 'julieta.luna@clinica.com', 3),

-- Traumatología
('Miguel', 'Campos', 'MP-4001', '3517004001', 'miguel.campos@clinica.com', 4),
('Daniela', 'Fuentes', 'MP-4002', '3517004002', 'daniela.fuentes@clinica.com', 4),
('Hernán', 'Sosa', 'MP-4003', '3517004003', 'hernan.sosa@clinica.com', 4);


-- ============================================================
-- 4. EMPLEADOS
-- Personal administrativo que puede cargar o gestionar turnos.
-- ============================================================

INSERT INTO empleados (
    nombre,
    apellido,
    dni,
    usuario,
    contrasena,
    rol,
    activo
)
VALUES
('Laura', 'Fernández', '30111222', 'lfernandez', '123456', 'administrador', TRUE),
('Martín', 'Suárez', '32222333', 'msuarez', '123456', 'recepcionista', TRUE);


-- ============================================================
-- 5. DISPONIBILIDAD MÉDICA
-- Indica qué días y horarios atiende cada médico.
-- No crea turnos; solo representa la agenda base.
-- ============================================================

INSERT INTO disponibilidad_medica (
    medico_id,
    dia_semana,
    hora_inicio,
    hora_fin,
    activo
)
VALUES
-- Cardiología
(1, 'Lunes', '08:00:00', '12:00:00', TRUE),
(1, 'Miércoles', '08:00:00', '12:00:00', TRUE),
(2, 'Martes', '14:00:00', '18:00:00', TRUE),
(2, 'Jueves', '14:00:00', '18:00:00', TRUE),
(3, 'Viernes', '09:00:00', '13:00:00', TRUE),

-- Pediatría
(4, 'Lunes', '09:00:00', '13:00:00', TRUE),
(4, 'Miércoles', '09:00:00', '13:00:00', TRUE),
(5, 'Martes', '08:00:00', '12:00:00', TRUE),
(5, 'Jueves', '08:00:00', '12:00:00', TRUE),
(6, 'Viernes', '14:00:00', '18:00:00', TRUE),

-- Dermatología
(7, 'Lunes', '15:00:00', '19:00:00', TRUE),
(7, 'Jueves', '15:00:00', '19:00:00', TRUE),
(8, 'Martes', '10:00:00', '14:00:00', TRUE),
(8, 'Viernes', '10:00:00', '14:00:00', TRUE),

-- Traumatología
(9, 'Lunes', '08:00:00', '12:00:00', TRUE),
(9, 'Miércoles', '14:00:00', '18:00:00', TRUE),
(10, 'Martes', '09:00:00', '13:00:00', TRUE),
(10, 'Jueves', '09:00:00', '13:00:00', TRUE),
(11, 'Viernes', '08:00:00', '12:00:00', TRUE);


-- ============================================================
-- 6. TURNOS
-- Turnos de ejemplo para consultar por paciente, médico,
-- especialidad, fecha o estado.
-- ============================================================

INSERT INTO turnos (
    paciente_id,
    medico_id,
    empleado_id,
    fecha_turno,
    estado,
    motivo_consulta
)
VALUES
-- Cardiología
(1, 1, NULL, '2026-06-03 08:30:00', 'pendiente', 'Chequeo general cardiológico'),
(2, 1, 1,    '2026-06-03 09:00:00', 'confirmado', 'Control de presión arterial'),
(3, 2, 2,    '2026-06-04 14:30:00', 'confirmado', 'Dolor en el pecho'),

-- Pediatría
(4, 4, NULL, '2026-06-03 09:20:00', 'pendiente', 'Control pediátrico'),
(5, 5, 1,    '2026-06-04 08:30:00', 'confirmado', 'Fiebre y malestar general'),
(6, 6, NULL, '2026-06-05 15:00:00', 'pendiente', 'Consulta pediátrica'),

-- Dermatología
(7, 7, 2,    '2026-06-04 15:30:00', 'confirmado', 'Revisión de manchas en la piel'),
(8, 8, NULL, '2026-06-05 10:30:00', 'pendiente', 'Consulta por irritación'),

-- Traumatología
(9, 9, 1,     '2026-06-03 15:00:00', 'confirmado', 'Dolor de rodilla'),
(10, 10, NULL,'2026-06-04 09:30:00', 'pendiente', 'Dolor lumbar'),
(1, 11, 2,    '2026-06-05 08:30:00', 'confirmado', 'Control de esguince'),

-- Turnos históricos para reportes
(2, 3, 1,    '2026-05-20 10:00:00', 'atendido', 'Control cardiológico realizado'),
(3, 7, 2,    '2026-05-21 16:00:00', 'ausente', 'Consulta dermatológica no asistida'),
(4, 9, NULL, '2026-05-22 09:00:00', 'cancelado', 'Turno cancelado por el paciente');


-- ============================================================
-- 7. HISTORIA CLÍNICA
-- Registro médico asociado a un turno ya atendido.
-- ============================================================

INSERT INTO historia_clinica (
    paciente_id,
    medico_id,
    id_turno,
    fecha_registro,
    diagnostico,
    tratamiento,
    observaciones
)
VALUES
(
    2,
    3,
    12,
    '2026-05-20 10:45:00',
    'Presión arterial dentro de valores normales.',
    'Control anual recomendado. Mantener hábitos saludables.',
    'Paciente sin síntomas relevantes al momento de la consulta.'
);