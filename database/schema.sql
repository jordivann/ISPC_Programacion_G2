CREATE DATABASE IF NOT EXISTS turnos_medicos;

USE turnos_medicos;
-- ============================================================
-- PROYECTO: Consultorio Medico San Rafael
-- BASE DE DATOS: turnos_medicos


-- ============================================================
-- 1. TABLA: Empleado
-- Guarda los datos de los empleados del consultorio.
-- Ej: nombre, apellido, email, teléfono, especialidad (si es médico), etc.
-- ============================================================

CREATE TABLE Empleado (
    id_empleado INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    dni VARCHAR(15) UNIQUE NOT NULL,
    email VARCHAR(120) NOT NULL,
    telefono VARCHAR(30) NULL,
    usuario VARCHAR(30) UNIQUE NOT NULL,
    contraseña VARCHAR(255) NOT NULL,
    rol VARCHAR(30) NOT NULL, -- Ej: 'medico', 'recepcionista', 'admin'
    ACTIVE BOOLEAN NOT NULL DEFAULT TRUE

);


-- ============================================================
-- 2. TABLA: Paciente
-- Contiene la información personal del paciente.
-- ============================================================

CREATE TABLE Paciente (
    id_paciente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    dni VARCHAR(15) UNIQUE NOT NULL,
    email VARCHAR(150)  NOT NULL,
    telefono VARCHAR(20) NULL,
    fecha_nacimiento DATE NOT NULL,
    direccion VARCHAR(150) NULL
    
);
-- ============================================================
-- 3. TABLA: Medico
-- Almacena informacion de los profesionales.

-- ============================================================

CREATE TABLE Medico (
    id_medico INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    matricula VARCHAR(20) UNIQUE NOT NULL,
    especialidad VARCHAR(100) NULL,
    email VARCHAR(120) NOT NULL,
    telefono VARCHAR(20) NULL
    );
    
-- ============================================================
-- 4. TABLA: turnos
-- Tabla principal que relaciona paciente, médico y empleado..
-- ============================================================

CREATE TABLE Turnos (
    id_turno INT AUTO_INCREMENT PRIMARY KEY,
    id_paciente INT NOT NULL,
    id_medico INT NOT NULL,
    id_empleado INT NOT NULL,
    fecha_turno DATE NOT NULL,
    hora_turno TIME NOT NULL,
    estado VARCHAR(20) NOT NULL, -- Ej: 'pendiente', 'confirmado', 'cancelado'
    motivo VARCHAR(200) NULL,

    FOREIGN KEY (id_paciente) REFERENCES Paciente (id_paciente),
    FOREIGN KEY (id_medico) REFERENCES Medico (id_medico),
    FOREIGN KEY (id_empleado) REFERENCES Empleado (id_empleado)
);


-- ============================================================
-- 5. TABLA: Historia Clinica
-- Permite registrar el historial medico del paciente
-- ============================================================

CREATE TABLE Historia_clinica (
    id_historia_clinica INT AUTO_INCREMENT PRIMARY KEY,
    id_paciente INT NOT NULL,
    id_medico INT NOT NULL,
    fecha_registro DATETIME NOT NULL,
    diagnostico TEXT,
    tratamiento TEXT,
    observaciones TEXT,
    FOREIGN KEY (id_paciente) REFERENCES Paciente (id_paciente),
    FOREIGN KEY (id_medico) REFERENCES Medico (id_medico)
    
);

