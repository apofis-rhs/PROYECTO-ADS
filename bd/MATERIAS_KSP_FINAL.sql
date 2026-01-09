-- MATERIAS

-- =============================================
--           MATERIAS PARA KINDER 1
-- =============================================
-- Nota: Buscamos 'Kinder' O 'Preescolar' indistintamente e ignorando mayúsculas (ILIKE)

-- Desarrollo Socioemocional I
INSERT INTO materia (clave, nombre, creditos, nivel_sugerido, sesiones_por_semana, id_carrera, id_nivel)
VALUES ('KIN-K1-ES1', 'Desarrollo Socioemocional I', 7, 1, 4, NULL,
        (SELECT id_nivel FROM nivel_educativo
         WHERE nombre ILIKE '%Kinder%' OR nombre ILIKE '%Preescolar%'
         LIMIT 1));

-- Estimulación Cognitiva I
INSERT INTO materia (clave, nombre, creditos, nivel_sugerido, sesiones_por_semana, id_carrera, id_nivel)
VALUES ('KIN-K1-ET1', 'Estimulación Cognitiva I', 7, 1, 5, NULL,
        (SELECT id_nivel FROM nivel_educativo
         WHERE nombre ILIKE '%Kinder%' OR nombre ILIKE '%Preescolar%'
         LIMIT 1));

-- Juego y Experimentación I
INSERT INTO materia (clave, nombre, creditos, nivel_sugerido, sesiones_por_semana, id_carrera, id_nivel)
VALUES ('KIN-K1-JE1', 'Juego y Experimentación I', 7, 1, 5, NULL,
        (SELECT id_nivel FROM nivel_educativo
         WHERE nombre ILIKE '%Kinder%' OR nombre ILIKE '%Preescolar%'
         LIMIT 1));

-- Comunicación y Lenguaje Oral
INSERT INTO materia (clave, nombre, creditos, nivel_sugerido, sesiones_por_semana, id_carrera, id_nivel)
VALUES ('KIN-K1-CL1', 'Comunicación y Lenguaje Oral', 7, 1, 5, NULL,
        (SELECT id_nivel FROM nivel_educativo
         WHERE nombre ILIKE '%Kinder%' OR nombre ILIKE '%Preescolar%'
         LIMIT 1));

-- Arte, Creatividad y Movimiento I
INSERT INTO materia (clave, nombre, creditos, nivel_sugerido, sesiones_por_semana, id_carrera, id_nivel)
VALUES ('KIN-K1-AR1', 'Arte, Creatividad y Movimiento I', 7, 1, 5, NULL,
        (SELECT id_nivel FROM nivel_educativo
         WHERE nombre ILIKE '%Kinder%' OR nombre ILIKE '%Preescolar%'
         LIMIT 1));

-- Razonamiento Matemático Inicial I
INSERT INTO materia (clave, nombre, creditos, nivel_sugerido, sesiones_por_semana, id_carrera, id_nivel)
VALUES ('KIN-K1-RM1', 'Razonamiento Matemático Inicial I', 7, 1, 5, NULL,
        (SELECT id_nivel FROM nivel_educativo
         WHERE nombre ILIKE '%Kinder%' OR nombre ILIKE '%Preescolar%'
         LIMIT 1));

-- SCRIPT CORREGIDO PARA POBLAR MATERIAS
-- Solución al error de id_nivel NULL

-- =============================================
--           MATERIAS PARA KINDER 2
-- =============================================
-- Nota: Buscamos 'Kinder' O 'Preescolar' indistintamente e ignorando mayúsculas (ILIKE)

-- Desarrollo Socioemocional II
INSERT INTO materia (clave, nombre, creditos, nivel_sugerido, sesiones_por_semana, id_carrera, id_nivel)
VALUES ('KIN-K2-ES2', 'Desarrollo Socioemocional II', 7, 2, 4, NULL,
        (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE '%Kinder%' OR nombre ILIKE '%Preescolar%' LIMIT 1));

-- Estimulación Cognitiva II
INSERT INTO materia (clave, nombre, creditos, nivel_sugerido, sesiones_por_semana, id_carrera, id_nivel)
VALUES ('KIN-K2-ET2', 'Estimulación Cognitiva II', 7, 2, 5, NULL,
        (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE '%Kinder%' OR nombre ILIKE '%Preescolar%' LIMIT 1));

-- Juego y Experimentación II
INSERT INTO materia (clave, nombre, creditos, nivel_sugerido, sesiones_por_semana, id_carrera, id_nivel)
VALUES ('KIN-K2-JE2', 'Juego y Experimentación II', 7, 2, 5, NULL,
        (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE '%Kinder%' OR nombre ILIKE '%Preescolar%' LIMIT 1));

-- Comunicación y Lectoescritura Inicial
INSERT INTO materia (clave, nombre, creditos, nivel_sugerido, sesiones_por_semana, id_carrera, id_nivel)
VALUES ('KIN-K2-LC2', 'Comunicación y Lectoescritura Inicial', 7, 2, 5, NULL,
        (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE '%Kinder%' OR nombre ILIKE '%Preescolar%' LIMIT 1));

-- Arte, Creatividad y Movimiento
INSERT INTO materia (clave, nombre, creditos, nivel_sugerido, sesiones_por_semana, id_carrera, id_nivel)
VALUES ('KIN-K2-AR2', 'Arte, Creatividad y Movimiento', 7, 2, 5, NULL,
        (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE '%Kinder%' OR nombre ILIKE '%Preescolar%' LIMIT 1));

-- Razonamiento Matemático Inicial
INSERT INTO materia (clave, nombre, creditos, nivel_sugerido, sesiones_por_semana, id_carrera, id_nivel)
VALUES ('KIN-K2-RM2', 'Razonamiento Matemático Inicial', 7, 2, 5, NULL,
        (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE '%Kinder%' OR nombre ILIKE '%Preescolar%' LIMIT 1));


-- =========================================================
-- MATERIAS PARA PRIMARIA
-- =========================================================

------------------------------------------------------------
-- 1° PRIMARIA
------------------------------------------------------------

INSERT INTO materia (clave, nombre, creditos, nivel_sugerido, id_carrera, id_nivel, sesiones_por_semana) VALUES
('PRI-P1-ESP', 'Español I',              7, 1, NULL, (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE 'Primaria' LIMIT 1), 5),
('PRI-P1-MAT', 'Matemáticas I',          7, 1, NULL, (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE 'Primaria' LIMIT 1), 5),
('PRI-P1-CN',  'Ciencias Naturales I',   7, 1, NULL, (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE 'Primaria' LIMIT 1), 4),
('PRI-P1-HIS', 'Historia I',             7, 1, NULL, (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE 'Primaria' LIMIT 1), 3),
('PRI-P1-GEO', 'Geografía I',            7, 1, NULL, (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE 'Primaria' LIMIT 1), 3),
('PRI-P1-FCE', 'Formación Cívica y Ética I', 7, 1, NULL, (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE 'Primaria' LIMIT 1), 2);

------------------------------------------------------------
-- 2° PRIMARIA
------------------------------------------------------------

INSERT INTO materia (clave, nombre, creditos, nivel_sugerido, id_carrera, id_nivel, sesiones_por_semana) VALUES
('PRI-P2-ESP', 'Español II',              7, 2, NULL, (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE 'Primaria' LIMIT 1), 5),
('PRI-P2-MAT', 'Matemáticas II',          7, 2, NULL, (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE 'Primaria' LIMIT 1), 5),
('PRI-P2-CN',  'Ciencias Naturales II',   7, 2, NULL, (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE 'Primaria' LIMIT 1), 4),
('PRI-P2-HIS', 'Historia II',             7, 2, NULL, (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE 'Primaria' LIMIT 1), 3),
('PRI-P2-GEO', 'Geografía II',            7, 2, NULL, (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE 'Primaria' LIMIT 1), 3),
('PRI-P2-FCE', 'Formación Cívica y Ética II', 7, 2, NULL, (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE 'Primaria' LIMIT 1), 2);

------------------------------------------------------------
-- 3° PRIMARIA
------------------------------------------------------------

INSERT INTO materia (clave, nombre, creditos, nivel_sugerido, id_carrera, id_nivel, sesiones_por_semana) VALUES
('PRI-P3-ESP', 'Español III',              7, 3, NULL, (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE 'Primaria' LIMIT 1), 5),
('PRI-P3-MAT', 'Matemáticas III',          7, 3, NULL, (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE 'Primaria' LIMIT 1), 5),
('PRI-P3-CN',  'Ciencias Naturales III',   7, 3, NULL, (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE 'Primaria' LIMIT 1), 4),
('PRI-P3-HIS', 'Historia III',             7, 3, NULL, (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE 'Primaria' LIMIT 1), 3),
('PRI-P3-GEO', 'Geografía III',            7, 3, NULL, (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE 'Primaria' LIMIT 1), 3),
('PRI-P3-FCE', 'Formación Cívica y Ética III', 7, 3, NULL, (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE 'Primaria' LIMIT 1), 2);

------------------------------------------------------------
-- 4° PRIMARIA
------------------------------------------------------------

INSERT INTO materia (clave, nombre, creditos, nivel_sugerido, id_carrera, id_nivel, sesiones_por_semana) VALUES
('PRI-P4-ESP', 'Español IV',              7, 4, NULL, (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE 'Primaria' LIMIT 1), 5),
('PRI-P4-MAT', 'Matemáticas IV',          7, 4, NULL, (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE 'Primaria' LIMIT 1), 5),
('PRI-P4-CN',  'Ciencias Naturales IV',   7, 4, NULL, (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE 'Primaria' LIMIT 1), 4),
('PRI-P4-HIS', 'Historia IV',             7, 4, NULL, (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE 'Primaria' LIMIT 1), 3),
('PRI-P4-GEO', 'Geografía IV',            7, 4, NULL, (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE 'Primaria' LIMIT 1), 3),
('PRI-P4-FCE', 'Formación Cívica y Ética IV', 7, 4, NULL, (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE 'Primaria' LIMIT 1), 2);

------------------------------------------------------------
-- 5° PRIMARIA
------------------------------------------------------------

INSERT INTO materia (clave, nombre, creditos, nivel_sugerido, id_carrera, id_nivel, sesiones_por_semana) VALUES
('PRI-P5-ESP', 'Español V',              7, 5, NULL, (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE 'Primaria' LIMIT 1), 5),
('PRI-P5-MAT', 'Matemáticas V',          7, 5, NULL, (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE 'Primaria' LIMIT 1), 5),
('PRI-P5-CN',  'Ciencias Naturales V',   7, 5, NULL, (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE 'Primaria' LIMIT 1), 4),
('PRI-P5-HIS', 'Historia V',             7, 5, NULL, (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE 'Primaria' LIMIT 1), 3),
('PRI-P5-GEO', 'Geografía V',            7, 5, NULL, (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE 'Primaria' LIMIT 1), 3),
('PRI-P5-FCE', 'Formación Cívica y Ética V', 7, 5, NULL, (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE 'Primaria' LIMIT 1), 2);

------------------------------------------------------------
-- 6° PRIMARIA
------------------------------------------------------------

INSERT INTO materia (clave, nombre, creditos, nivel_sugerido, id_carrera, id_nivel, sesiones_por_semana) VALUES
('PRI-P6-ESP', 'Español VI',              7, 6, NULL, (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE 'Primaria' LIMIT 1), 5),
('PRI-P6-MAT', 'Matemáticas VI',          7, 6, NULL, (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE 'Primaria' LIMIT 1), 5),
('PRI-P6-CN',  'Ciencias Naturales VI',   7, 6, NULL, (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE 'Primaria' LIMIT 1), 4),
('PRI-P6-HIS', 'Historia VI',             7, 6, NULL, (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE 'Primaria' LIMIT 1), 3),
('PRI-P6-GEO', 'Geografía VI',            7, 6, NULL, (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE 'Primaria' LIMIT 1), 3),
('PRI-P6-FCE', 'Formación Cívica y Ética VI', 7, 6, NULL, (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE 'Primaria' LIMIT 1), 2);


-- =========================================================
-- MATERIAS PARA SECUNDARIA
-- =========================================================

------------------------------------------------------------
-- 1° SECUNDARIA
------------------------------------------------------------

INSERT INTO materia (clave, nombre, creditos, nivel_sugerido, id_carrera, id_nivel, sesiones_por_semana) VALUES
('SEC-S1-ESP', 'Español I',                 7, 1, NULL, (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE 'Secundaria' LIMIT 1), 5),
('SEC-S1-MAT', 'Matemáticas I',             7, 1, NULL, (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE 'Secundaria' LIMIT 1), 5),
('SEC-S1-BIO', 'Biología I',                7, 1, NULL, (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE 'Secundaria' LIMIT 1), 4),
('SEC-S1-HIS', 'Historia I',                7, 1, NULL, (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE 'Secundaria' LIMIT 1), 3),
('SEC-S1-ING', 'Inglés I',                  7, 1, NULL, (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE 'Secundaria' LIMIT 1), 3),
('SEC-S1-FCE', 'Formación Cívica y Ética I',7, 1, NULL, (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE 'Secundaria' LIMIT 1), 2);

------------------------------------------------------------
-- 2° SECUNDARIA
------------------------------------------------------------

INSERT INTO materia (clave, nombre, creditos, nivel_sugerido, id_carrera, id_nivel, sesiones_por_semana) VALUES
('SEC-S2-ESP', 'Español II',                 7, 2, NULL, (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE 'Secundaria' LIMIT 1), 5),
('SEC-S2-MAT', 'Matemáticas II',             7, 2, NULL, (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE 'Secundaria' LIMIT 1), 5),
('SEC-S2-FIS', 'Física II',                  7, 2, NULL, (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE 'Secundaria' LIMIT 1), 4),
('SEC-S2-HIS', 'Historia II',                7, 2, NULL, (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE 'Secundaria' LIMIT 1), 3),
('SEC-S2-ING', 'Inglés II',                  7, 2, NULL, (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE 'Secundaria' LIMIT 1), 3),
('SEC-S2-FCE', 'Formación Cívica y Ética II',7, 2, NULL, (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE 'Secundaria' LIMIT 1), 2);

------------------------------------------------------------
-- 3° SECUNDARIA
------------------------------------------------------------

INSERT INTO materia (clave, nombre, creditos, nivel_sugerido, id_carrera, id_nivel, sesiones_por_semana) VALUES
('SEC-S3-ESP', 'Español III',                 7, 3, NULL, (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE 'Secundaria' LIMIT 1), 5),
('SEC-S3-MAT', 'Matemáticas III',             7, 3, NULL, (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE 'Secundaria' LIMIT 1), 5),
('SEC-S3-QUI', 'Química III',                 7, 3, NULL, (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE 'Secundaria' LIMIT 1), 4),
('SEC-S3-HIS', 'Historia III',                7, 3, NULL, (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE 'Secundaria' LIMIT 1), 3),
('SEC-S3-ING', 'Inglés III',                  7, 3, NULL, (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE 'Secundaria' LIMIT 1), 3),
('SEC-S3-FCE', 'Formación Cívica y Ética III',7, 3, NULL, (SELECT id_nivel FROM nivel_educativo WHERE nombre ILIKE 'Secundaria' LIMIT 1), 2);

-- FIN DEL SCRIPT