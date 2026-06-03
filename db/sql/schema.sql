-- ============================================================
-- RECREAR BASE DE DATOS DESDE CERO
-- ADVERTENCIA:
-- DROP DATABASE elimina completamente la base anterior,
-- incluyendo tablas, datos y relaciones.
-- ============================================================

DROP DATABASE IF EXISTS turnos_medicos;

CREATE DATABASE turnos_medicos;

USE turnos_medicos;

-- ============================================================
-- PROYECTO: Sistema de Gestión de Turnos Médicos
-- OBJETIVO:
-- Crear una base de datos simple para consultar pacientes,
-- médicos, especialidades, turnos, disponibilidad e historia clínica.
-- ============================================================


-- ============================================================
-- 1. TABLA: pacientes
-- Guarda los datos personales de los pacientes.
-- Cada paciente se identifica de forma única por su DNI.
-- ============================================================

CREATE TABLE pacientes (
    id_paciente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    dni VARCHAR(15) NOT NULL UNIQUE,
    fecha_nacimiento DATE NOT NULL,
    telefono VARCHAR(20),
    email VARCHAR(100),
    direccion VARCHAR(255)
);


-- ============================================================
-- 2. TABLA: especialidades
-- Guarda las especialidades médicas disponibles.
-- Ejemplo: Cardiología, Pediatría, Dermatología.
-- ============================================================

CREATE TABLE especialidades (
    id_especialidad INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT
);


-- ============================================================
-- 3. TABLA: medicos
-- Guarda los datos de los médicos.
-- Cada médico pertenece a una especialidad.
-- ============================================================

CREATE TABLE medicos (
    id_medico INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    matricula VARCHAR(20) NOT NULL UNIQUE,
    telefono VARCHAR(20),
    email VARCHAR(100),
    id_especialidad INT NOT NULL,

    CONSTRAINT fk_medicos_especialidades
        FOREIGN KEY (id_especialidad)
        REFERENCES especialidades(id_especialidad)
);


-- ============================================================
-- 4. TABLA: empleados
-- Guarda los datos del personal administrativo.
-- En este proyecto se usa para saber quién cargó un turno.
-- ============================================================

CREATE TABLE empleados (
    id_empleado INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    dni VARCHAR(15) NOT NULL UNIQUE,
    usuario VARCHAR(30) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL,
    rol VARCHAR(30) NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE
);


-- ============================================================
-- 5. TABLA: turnos
-- Tabla principal del sistema.
-- Relaciona un paciente con un médico en una fecha y hora.
-- También permite registrar el empleado que cargó el turno.
-- ============================================================

CREATE TABLE turnos (
    id_turno INT AUTO_INCREMENT PRIMARY KEY,
    paciente_id INT NOT NULL,
    medico_id INT NOT NULL,
    empleado_id INT NULL,
    fecha_turno DATETIME NOT NULL,
    estado VARCHAR(20) NOT NULL DEFAULT 'pendiente',
    motivo_consulta VARCHAR(255),
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_turnos_pacientes
        FOREIGN KEY (paciente_id)
        REFERENCES pacientes(id_paciente),

    CONSTRAINT fk_turnos_medicos
        FOREIGN KEY (medico_id)
        REFERENCES medicos(id_medico),

    CONSTRAINT fk_turnos_empleados
        FOREIGN KEY (empleado_id)
        REFERENCES empleados(id_empleado),

    -- Evita que un médico tenga dos turnos en el mismo horario.
    CONSTRAINT uq_turno_medico_fecha
        UNIQUE (medico_id, fecha_turno)
);


-- ============================================================
-- 6. TABLA: disponibilidad_medica
-- Guarda los días y horarios en los que atiende cada médico.
-- No reserva turnos, solo indica la agenda base del profesional.
-- ============================================================

CREATE TABLE disponibilidad_medica (
    id_disponibilidad INT AUTO_INCREMENT PRIMARY KEY,
    medico_id INT NOT NULL,
    dia_semana VARCHAR(15) NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE,

    CONSTRAINT fk_disponibilidad_medico
        FOREIGN KEY (medico_id)
        REFERENCES medicos(id_medico)
);


-- ============================================================
-- 7. TABLA: historia_clinica
-- Guarda registros médicos básicos de un paciente.
-- Se vincula con el paciente, el médico y el turno correspondiente.
-- ============================================================

CREATE TABLE historia_clinica (
    id_historia_clinica INT AUTO_INCREMENT PRIMARY KEY,
    paciente_id INT NOT NULL,
    medico_id INT NOT NULL,
    id_turno INT NOT NULL,
    fecha_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    diagnostico TEXT NOT NULL,
    tratamiento TEXT,
    observaciones TEXT,

    CONSTRAINT fk_historia_pacientes
        FOREIGN KEY (paciente_id)
        REFERENCES pacientes(id_paciente),

    CONSTRAINT fk_historia_medicos
        FOREIGN KEY (medico_id)
        REFERENCES medicos(id_medico),

    CONSTRAINT fk_historia_turnos
        FOREIGN KEY (id_turno)
        REFERENCES turnos(id_turno)
);