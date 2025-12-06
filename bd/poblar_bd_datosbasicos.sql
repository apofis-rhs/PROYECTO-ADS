-- poblar bd para nivel educativo:
-- NIVELES EDUCATIVOS

INSERT INTO nivel_educativo (id_nivel, nombre) VALUES
(1, 'KINDER'),
(2, 'PRIMARIA'),
(3, 'SECUNDARIA'),
(4, 'PREPARATORIA'),
(5, 'UNIVERSIDAD');

-- Mostrar

SELECT * FROM nivel_educativo;

-- TIPO RELACIÓN TUTOR
INSERT INTO cat_tipo_relacion_tutor (nombre) VALUES
('PADRE'),
('MADRE'),
('TUTOR');

-- mostrar
SELECT * FROM cat_tipo_relacion_tutor;

-- TIPOS DE CARRERA
INSERT INTO cat_tipo_carrera (nombre) VALUES
('TECNICA'),
('UNIVERSITARIA');
-- Mostrar
SELECT * FROM cat_tipo_carrera;

-- TURNOS
INSERT INTO cat_turno (nombre) VALUES
('MATUTINO'),
('VESPERTINO');

-- MOSTRAR
SELECT * FROM cat_turno;

-- ESTADO DEL ALUMNO
INSERT INTO cat_estado_alumno (nombre) VALUES
('ACTIVO'),
('BAJA_TEMPORAL'),
('BAJA_DEFINITIVA'),
('EGRESADO');
-- MOSTRAR
SELECT * FROM cat_estado_alumno;

-- ESTADO DE INSCRIPCIÓN (ALUMNO_GRUPO)
INSERT INTO cat_estado_inscripcion (nombre) VALUES
('CURSANDO'),
('BAJA'),
('REPROBADA');

-- mostrar
SELECT * FROM cat_estado_inscripcion;

-- TIPOS DE INCIDENTE
INSERT INTO cat_tipo_incidente (nombre) VALUES
('ACADEMICO'),
('CONDUCTA'),
('ADMINISTRATIVO');
-- mostrar 
SELECT * FROM cat_tipo_incidente;


-- GRAVEDAD DE INCIDENTE
INSERT INTO cat_gravedad_incidente (nombre) VALUES
('LEVE'),
('MODERADA'),
('GRAVE');

-- mostrar
SELECT * FROM cat_gravedad_incidente;

-- ESTADO DEL HISTORIAL ACADÉMICO
INSERT INTO cat_estado_historial (nombre) VALUES
('CURSANDO'),
('APROBADO'),
('REPROBADO');

-- Mstrar 
SELECT * FROM cat_estado_historial;