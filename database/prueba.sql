USE turnos_medicos;

SELECT 
    t.id_turno,
    t.fecha_turno,
    t.estado,
    CONCAT(p.nombre, ' ', p.apellido) AS paciente,
    CONCAT(m.nombre, ' ', m.apellido) AS medico,
    e.nombre AS especialidad,
    t.motivo_consulta
FROM turnos t
INNER JOIN pacientes p
    ON t.paciente_id = p.id_paciente
INNER JOIN medicos m
    ON t.medico_id = m.id_medico
INNER JOIN especialidades e
    ON m.id_especialidad = e.id_especialidad
ORDER BY t.fecha_turno;