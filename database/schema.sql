CREATE DATABASE IF NOT EXISTS turnos_medicos;

USE turnos_medicos;
-- ============================================================
-- PROYECTO: Sistema de Gestión de Turnos Médicos
-- BASE DE DATOS: turnos_medicos


-- ============================================================
-- 1. TABLA: Empleados
-- Representa al personal administrativo que utilizara el sistema para gestionar pacientes y turnos
-- ============================================================

CREATE TABLE empleados (
    id_empleado INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    dni VARCHAR(15) NOT NULL UNIQUE,
    telefono VARCHAR(20) NULL,
    email VARCHAR(100) NULL UNIQUE,
    usuario VARCHAR(30) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL,
    rol varchar(30) NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
);


-- ============================================================
-- 2. TABLA: paciente
-- Contiene la información personal del paciente..
-- ============================================================

CREATE TABLE pacientes (
    id_paciente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    dni VARCHAR(15) NOT NULL UNIQUE,
    fecha_nacimiento DATE NOT NULL,
    email VARCHAR(100) NULL UNIQUE,
    telefono VARCHAR(20) NULL,
    direccion VARCHAR(255) NULL,
    
);

-- ============================================================
-- 3. TABLA: medico
-- Almacena información de los profesionales. 
-- ============================================================

CREATE TABLE medicos (
    id_medico INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    matricula VARCHAR(20) NOT NULL UNIQUE,
    especialidad VARCHAR(100) NOT NULL,
    email VARCHAR(100) NULL UNIQUE,
    telefono VARCHAR(20) NULL,

);

-- ============================================================
-- 4. TABLA: turnos
-- Tabla principal que relaciona paciente, médico y empleado.
-- ============================================================

CREATE TABLE turnos (
    id_turno INT AUTO_INCREMENT PRIMARY KEY,
    paciente_id INT NOT NULL,
    medico_id INT NOT NULL,
    empleado_id INT NOT NULL,
    fecha_turno DATETIME NOT NULL,
    estado VARCHAR(20) NOT NULL DEFAULT 'pendiente',
    motivo_consulta VARCHAR(255)
);


-- ============================================================
-- 5. TABLA: historia clinica
-- Permite registrar el historial médico del paciente 
-- ============================================================

CREATE TABLE historia_clinica (
    id_historia_clinica INT AUTO_INCREMENT PRIMARY KEY,
    paciente_id INT NOT NULL,
    medico_id INT NOT NULL,
    fecha_registro DATETIME NOT NULL,
    diagnostico TEXT NOT NULL,
    tratamiento TEXT,
    observaciones TEXT
);
 