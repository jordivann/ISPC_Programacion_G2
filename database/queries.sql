-- consultas SQL utiles o frecuentes.

-- Ver todos los pacientes
SELECT * FROM paciente;

-- Ver turnos con nombre del paciente
SELECT
    t.id_turno,
    p.nombre,
    p.apellido,
    t.fecha_turno,
    t.hora_turno

FROM turno t

INNER JOIN paciente p
ON t.id_paciente = p.id_paciente;