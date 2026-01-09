-- =========================================================
-- 1) AGREGAR CENTRO EDUCATIVO
-- =========================================================
INSERT INTO universidad (nombre, ciudad, estado, pais)
SELECT 'ESCOM', 'Ciudad de Mexico', 'CDMX', 'Mexico'
WHERE NOT EXISTS (
  SELECT 1 FROM universidad u WHERE u.nombre = 'ESCOM'
);

-- =========================================================
-- 2) VISTA PARA PREPARATORIA
-- =========================================================
INSERT INTO cat_tipo_carrera (nombre)
SELECT 'PREPARATORIA'
WHERE NOT EXISTS (
  SELECT 1 FROM cat_tipo_carrera WHERE nombre ILIKE '%prepa%'
     OR nombre ILIKE '%preparatoria%'
     OR nombre ILIKE '%bachiller%'
     OR nombre ILIKE '%media%'
);

-- =========================================================
-- 3) INGRESAR CARRERAS PARA PREPARATORIA
-- =========================================================
BEGIN;
SELECT id_tipo_carrera, nombre
FROM cat_tipo_carrera;

-- =========================================================
-- VALIDACIONES + CARRERAS PREPA (idempotente)
-- =========================================================
DO $$
DECLARE
  v_id_universidad   INT;
  v_id_tipo_carrera  INT;
  v_id_nivel_prepa   INT;
BEGIN
  SELECT u.id_universidad
    INTO v_id_universidad
  FROM universidad u
  WHERE u.nombre = 'ESCOM'
  ORDER BY u.id_universidad
  LIMIT 1;

  IF v_id_universidad IS NULL THEN
    RAISE EXCEPTION 'No se pudo resolver id_universidad para universidad=ESCOM.';
  END IF;

  SELECT tc.id_tipo_carrera
    INTO v_id_tipo_carrera
  FROM tipo_carrera tc
  WHERE tc.nombre ILIKE '%prepa%'
     OR tc.nombre ILIKE '%preparatoria%'
     OR tc.nombre ILIKE '%bachiller%'
     OR tc.nombre ILIKE '%media%'
  ORDER BY tc.id_tipo_carrera
  LIMIT 1;

  IF v_id_tipo_carrera IS NULL THEN
    RAISE EXCEPTION 'No existe tipo_carrera para Preparatoria (prepa/preparatoria/bachiller/media). Inserta ese registro primero.';
  END IF;

  SELECT n.id_nivel
    INTO v_id_nivel_prepa
  FROM nivel_educativo n
  WHERE n.nombre ILIKE '%prepa%'
     OR n.nombre ILIKE '%preparatoria%'
     OR n.nombre ILIKE '%bachiller%'
  ORDER BY n.id_nivel
  LIMIT 1;

  IF v_id_nivel_prepa IS NULL THEN
    RAISE EXCEPTION 'No existe nivel_educativo para Preparatoria (prepa/preparatoria/bachiller). Inserta ese registro primero.';
  END IF;

  -- 1.1 Tronco Común (tolerante a mayúsculas/acentos)
  INSERT INTO carrera (nombre, duracion_semestres, activo, id_tipo_carrera, id_universidad)
  SELECT 'Tronco Común', 6, TRUE, v_id_tipo_carrera, v_id_universidad
  WHERE NOT EXISTS (
    SELECT 1
    FROM carrera c
    WHERE c.id_universidad = v_id_universidad
      AND c.nombre ILIKE '%tronco%comun%'
  );

  -- 1.2 Carreras técnicas (exact match)
  INSERT INTO carrera (nombre, duracion_semestres, activo, id_tipo_carrera, id_universidad)
  SELECT t.nombre, t.duracion_semestres, TRUE, v_id_tipo_carrera, v_id_universidad
  FROM (VALUES
    ('TECNICO COMPUTACION', 6),
    ('TECNICO EN SISTEMAS DIGITALES', 6),
    ('TECNICO EN SISTEMAS AUTOMOTRICES', 6)
  ) AS t(nombre, duracion_semestres)
  WHERE NOT EXISTS (
    SELECT 1
    FROM carrera c
    WHERE c.id_universidad = v_id_universidad
      AND c.nombre = t.nombre
  );
END $$;


-- =========================================================
-- 4) PREPARATORIA - TRONCO COMUN (MATERIAS)
-- =========================================================
WITH
u AS (
  SELECT id_universidad
  FROM universidad
  WHERE nombre = 'ESCOM'
  ORDER BY id_universidad
  LIMIT 1
),
c_tronco AS (
  SELECT c.id_carrera
  FROM carrera c
  JOIN u ON u.id_universidad = c.id_universidad
  WHERE c.nombre ILIKE '%tronco%comun%'
  ORDER BY c.id_carrera
  LIMIT 1
),
n_prepa AS (
  SELECT id_nivel
  FROM nivel_educativo
  WHERE nombre ILIKE '%prepa%' OR nombre ILIKE '%preparatoria%' OR nombre ILIKE '%bachiller%'
  ORDER BY id_nivel
  LIMIT 1
),
datos AS (
  SELECT *
  FROM (VALUES
    ('PRE-PA1-AA',   'Álgebra', 7, 1, 5),
    ('PRE-PA1-FI',   'Filosofía I', 7, 1, 3),
    ('PRE-PA1-CB1',  'Computación Básica I', 7, 1, 4),
    ('PRE-PA1-IN1',  'Inglés I', 7, 1, 5),
    ('PRE-PA1-EOE1', 'Expresión Oral y Escrita I', 7, 1, 4),
    ('PRE-PA1-DHP',  'Desarrollo de Habilidades del Pensamiento', 7, 1, 3),
    ('PRE-PA1-HMC1', 'Historia de México Contemporáneo I', 7, 1, 3),
    ('PRE-PA1-DP',   'Desarrollo Personal', 7, 1, 4),
    ('PRE-PA1-OJP1', 'Orientación Juvenil y Profesional I', 7, 1, 2),

    ('PRE-PA2-GT',   'Geometría y Trigonometría', 7, 2, 5),
    ('PRE-PA2-FII',  'Filosofía II', 7, 2, 3),
    ('PRE-PA2-CB2',  'Computación Básica II', 7, 2, 4),
    ('PRE-PA2-IN2',  'Inglés II', 7, 2, 5),
    ('PRE-PA2-EOE2', 'Expresión Oral y Escrita II', 7, 2, 4),
    ('PRE-PA2-BB',   'Biología Básica', 7, 2, 5),
    ('PRE-PA2-HMC2', 'Historia de México Contemporáneo II', 7, 2, 3),
    ('PRE-PA2-OJP2', 'Orientación Juvenil y Profesional II', 7, 2, 2),
    ('PRE-PA2-OPT1', 'Optativa 1', 7, 2, 3),

    ('PRE-TC3-GA',   'Geometría Analítica', 7, 3, 5),
    ('PRE-TC3-FIS1', 'Física I', 7, 3, 5),
    ('PRE-TC3-QUI1', 'Química I', 7, 3, 4),
    ('PRE-TC3-IN3',  'Inglés III', 7, 3, 6),
    ('PRE-TC3-CC',   'Comunicación Científica', 7, 3, 3),

    ('PRE-TC4-CD',   'Cálculo Diferencial', 7, 4, 5),
    ('PRE-TC4-FIS2', 'Física II', 7, 4, 5),
    ('PRE-TC4-QUI2', 'Química II', 7, 4, 4),
    ('PRE-TC4-IN4',  'Inglés IV', 7, 4, 6),
    ('PRE-TC4-OJP3', 'Orientación Juvenil y Profesional III', 7, 4, 2),

    ('PRE-TC5-CI',   'Cálculo Integral', 7, 5, 5),
    ('PRE-TC5-FIS3', 'Física III', 7, 5, 5),
    ('PRE-TC5-QUI3', 'Química III', 7, 5, 4),
    ('PRE-TC5-IN5',  'Inglés V', 7, 5, 6),

    ('PRE-TC6-PE',   'Probabilidad y Estadística', 7, 6, 5),
    ('PRE-TC6-FIS4', 'Física IV', 7, 6, 5),
    ('PRE-TC6-QUI4', 'Química IV', 7, 6, 4),
    ('PRE-TC6-IN6',  'Inglés VI', 7, 6, 6)
  ) AS t(clave, nombre, creditos, nivel_sugerido, sesiones_por_semana)
)
INSERT INTO materia (clave, nombre, creditos, nivel_sugerido, sesiones_por_semana, id_carrera, id_nivel)
SELECT
  d.clave, d.nombre, d.creditos, d.nivel_sugerido, d.sesiones_por_semana,
  c_tronco.id_carrera,
  n_prepa.id_nivel
FROM datos d
CROSS JOIN c_tronco
CROSS JOIN n_prepa
WHERE NOT EXISTS (SELECT 1 FROM materia m WHERE m.clave = d.clave);

-- =========================================================
-- 5) PREPARATORIA - MATERIAS POR CARRERA (TECNICAS) (idempotente)
-- =========================================================

-- 1) TECNICO COMPUTACION (niveles 3 a 6)
WITH
c AS (
  SELECT id_carrera FROM carrera WHERE nombre = 'TECNICO COMPUTACION' ORDER BY id_carrera LIMIT 1
),
n AS (
  SELECT id_nivel
  FROM nivel_educativo
  WHERE nombre ILIKE '%prepa%' OR nombre ILIKE '%preparatoria%' OR nombre ILIKE '%bachiller%'
  ORDER BY id_nivel
  LIMIT 1
),
datos AS (
  SELECT * FROM (VALUES
    ('PRE-COMP3-ALGP', 'Algoritmia y Programación', 7, 3, 4),
    ('PRE-COMP3-ENS',  'Ensamblado y Soporte de Componentes Electrónicos', 7, 3, 4),
    ('PRE-COMP3-OPT2', 'Optativa 2', 7, 3, 3),

    ('PRE-COMP4-PMOD', 'Programación Modular', 7, 4, 4),
    ('PRE-COMP4-REDC', 'Redes de Comunicaciones', 7, 4, 4),
    ('PRE-COMP4-SO',   'Sistemas Operativos', 7, 4, 4),
    ('PRE-COMP4-OPT3', 'Optativa 3', 7, 4, 3),

    ('PRE-COMP5-EG',   'Desarrollo de Aplicaciones con Entornos Gráficos', 7, 5, 5),
    ('PRE-COMP5-BD',   'Bases de Datos', 7, 5, 4),
    ('PRE-COMP5-PWEB', 'Portales Web', 7, 5, 4),
    ('PRE-COMP5-OPT4', 'Optativa 4', 7, 5, 3),

    ('PRE-COMP6-MOV',  'Programación de Aplicaciones para Dispositivos Móviles', 7, 6, 5),
    ('PRE-COMP6-SEG',  'Seguridad Informática', 7, 6, 4),
    ('PRE-COMP6-ICD',  'Introducción a la Ciencia de Datos', 7, 6, 3),
    ('PRE-COMP6-OPT5', 'Optativa 5 (Opción Curricular de Titulación)', 7, 6, 5)
  ) AS t(clave, nombre, creditos, nivel_sugerido, sesiones_por_semana)
)
INSERT INTO materia (clave, nombre, creditos, nivel_sugerido, id_carrera, id_nivel, sesiones_por_semana)
SELECT d.clave, d.nombre, d.creditos, d.nivel_sugerido, c.id_carrera, n.id_nivel, d.sesiones_por_semana
FROM datos d
CROSS JOIN c
CROSS JOIN n
WHERE NOT EXISTS (SELECT 1 FROM materia m WHERE m.clave = d.clave);

-- 6) TECNICO EN SISTEMAS AUTOMOTRICES (niveles 3 a 6)
WITH
c AS (
  SELECT id_carrera FROM carrera WHERE nombre = 'TECNICO EN SISTEMAS AUTOMOTRICES' ORDER BY id_carrera LIMIT 1
),
n AS (
  SELECT id_nivel
  FROM nivel_educativo
  WHERE nombre ILIKE '%prepa%' OR nombre ILIKE '%preparatoria%' OR nombre ILIKE '%bachiller%'
  ORDER BY id_nivel
  LIMIT 1
),
datos AS (
  SELECT * FROM (VALUES
    ('PRE-AUTO3-SAUTO', 'Sistemas del Automóvil', 7, 3, 1),
    ('PRE-AUTO3-MHEA',  'Manejo de Herramientas y Equipo de Medición Automotriz', 7, 3, 1),
    ('PRE-AUTO3-AEMP',  'Administración Empresarial Automotriz', 7, 3, 1),

    ('PRE-AUTO4-SIF',   'Servicio Integral al Sistema de Frenos', 7, 4, 1),
    ('PRE-AUTO4-SSDA',  'Sistema de Suspensión y Dirección Adaptativas', 7, 4, 1),
    ('PRE-AUTO4-SCAD',  'Seguridad, Confort y Aerodinámica', 7, 4, 1),
    ('PRE-AUTO4-OPT2',  'Optativa 2', 7, 4, 1),

    ('PRE-AUTO5-RMCI',  'Reacondicionamiento de Motores de Combustión Interna', 7, 5, 1),
    ('PRE-AUTO5-ME3D',  'Modelado y Ensamble en 3D', 7, 5, 1),
    ('PRE-AUTO5-SEE',   'Sistemas Eléctricos y Electrónicos', 7, 5, 1),
    ('PRE-AUTO5-OPT3',  'Optativa 3', 7, 5, 1),

    ('PRE-AUTO6-TMCI',  'Tecnologías de Motores de Combustión Interna', 7, 6, 1),
    ('PRE-AUTO6-TM',    'Tren Motriz', 7, 6, 1),
    ('PRE-AUTO6-AUTO',  'Autotrónica', 7, 6, 1),
    ('PRE-AUTO6-OPT4',  'Optativa 4 (Opción Curricular de Titulación)', 7, 6, 1)
  ) AS t(clave, nombre, creditos, nivel_sugerido, sesiones_por_semana)
)
INSERT INTO materia (clave, nombre, creditos, nivel_sugerido, id_carrera, id_nivel, sesiones_por_semana)
SELECT d.clave, d.nombre, d.creditos, d.nivel_sugerido, c.id_carrera, n.id_nivel, d.sesiones_por_semana
FROM datos d
CROSS JOIN c
CROSS JOIN n
WHERE NOT EXISTS (SELECT 1 FROM materia m WHERE m.clave = d.clave);

-- 7) TECNICO EN SISTEMAS DIGITALES (niveles 3 a 6)
WITH
c AS (
  SELECT id_carrera FROM carrera WHERE nombre = 'TECNICO EN SISTEMAS DIGITALES' ORDER BY id_carrera LIMIT 1
),
n AS (
  SELECT id_nivel
  FROM nivel_educativo
  WHERE nombre ILIKE '%prepa%' OR nombre ILIKE '%preparatoria%' OR nombre ILIKE '%bachiller%'
  ORDER BY id_nivel
  LIMIT 1
),
datos AS (
  SELECT * FROM (VALUES
    ('PRE-DIG3-CLCOMB', 'Circuitos Lógicos Combinatorios', 7, 3, 2),
    ('PRE-DIG3-CE',     'Circuitos Electrónicos', 7, 3, 2),
    ('PRE-DIG3-INSE',   'Instrumentación Electrónica', 7, 3, 1),

    ('PRE-DIG4-CLSEC',  'Circuitos Lógicos Secuenciales', 7, 4, 2),
    ('PRE-DIG4-EE',     'Elementos Electrónicos', 7, 4, 2),
    ('PRE-DIG4-LP',     'Lenguaje de Programación', 7, 4, 1),
    ('PRE-DIG4-OPT2',   'Optativa 2', 7, 4, 0),

    ('PRE-DIG5-AMIC',   'Arquitectura de Microcontroladores', 7, 5, 2),
    ('PRE-DIG5-DE',     'Dispositivos Electrónicos', 7, 5, 2),
    ('PRE-DIG5-EAD',    'Electrónica Analógica y Digital', 7, 5, 2),
    ('PRE-DIG5-OPT3',   'Optativa 3', 7, 5, 1),

    ('PRE-DIG6-AMICRO', 'Aplicaciones con Microcontroladores', 7, 6, 2),
    ('PRE-DIG6-MEE',    'Mantenimiento de Equipo Electrónico', 7, 6, 2),
    ('PRE-DIG6-RD',     'Redes Digitales', 7, 6, 2),
    ('PRE-DIG6-OPT4',   'Optativa 4 (Opción Curricular de Titulación)', 7, 6, 2)
  ) AS t(clave, nombre, creditos, nivel_sugerido, sesiones_por_semana)
)
INSERT INTO materia (clave, nombre, creditos, nivel_sugerido, id_carrera, id_nivel, sesiones_por_semana)
SELECT d.clave, d.nombre, d.creditos, d.nivel_sugerido, c.id_carrera, n.id_nivel, d.sesiones_por_semana
FROM datos d
CROSS JOIN c
CROSS JOIN n
WHERE NOT EXISTS (SELECT 1 FROM materia m WHERE m.clave = d.clave);