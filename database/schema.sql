-- ============================================================
-- RECREAR BASE DE DATOS DESDE CERO
-- ADVERTENCIA:
-- DROP DATABASE elimina completamente la base anterior,
-- incluyendo tablas, datos y relaciones.
-- ============================================================

DROP DATABASE IF EXISTS turnos_medicos;
CREATE DATABASE turnos_medicos;


USE turnos_medicos;


CREATE TABLE pacientes (
    id_paciente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    dni VARCHAR(15) NOT NULL UNIQUE,
    fecha_nacimiento DATE NOT NULL,
    telefono VARCHAR(20),
    email varchar(35),
    direccion VARCHAR(255)
);


CREATE TABLE medicos (
    id_medico INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    matricula VARCHAR(20) NOT NULL UNIQUE,
    telefono VARCHAR(20),
    especialidad VARCHAR(50) NOT NULL
);


CREATE TABLE turnos (
    id_turno INT AUTO_INCREMENT PRIMARY KEY,
    paciente_id INT NOT NULL,
    medico_id INT NOT NULL,
    fecha_turno DATETIME NOT NULL,
    estado VARCHAR(20) NOT NULL DEFAULT 'pendiente',
    motivo_consulta VARCHAR(255),


    CONSTRAINT fk_turnos_pacientes
        FOREIGN KEY (paciente_id)
        REFERENCES pacientes(id_paciente),


    CONSTRAINT fk_turnos_medicos
        FOREIGN KEY (medico_id)
        REFERENCES medicos(id_medico)
);
