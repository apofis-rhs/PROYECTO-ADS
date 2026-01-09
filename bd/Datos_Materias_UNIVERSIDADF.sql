BEGIN;

-- =========================================================
-- 1) Asegurar tipo de carrera UNIVERSIDAD (cat_tipo_carrera)
-- =========================================================
INSERT INTO cat_tipo_carrera (nombre)
SELECT 'UNIVERSIDAD'
WHERE NOT EXISTS (
  SELECT 1
  FROM cat_tipo_carrera
  WHERE nombre ILIKE '%universidad%'
     OR nombre ILIKE '%licenci%'
     OR nombre ILIKE '%ingenier%'
);

-- =========================================================
-- 2) Crear carrera: INGENIERIA EN SISTEMAS COMPUTACIONALES
-- =========================================================
DO $$
DECLARE
  v_id_universidad  INT;
  v_id_tipo_uni     INT;
BEGIN
  SELECT id_universidad
    INTO v_id_universidad
  FROM universidad
  WHERE nombre = 'ESCOM'
  ORDER BY id_universidad
  LIMIT 1;

  IF v_id_universidad IS NULL THEN
    RAISE EXCEPTION 'No existe universidad con nombre = ESCOM.';
  END IF;

  SELECT id_tipo_carrera
    INTO v_id_tipo_uni
  FROM cat_tipo_carrera
  WHERE nombre ILIKE '%universidad%'
     OR nombre ILIKE '%licenci%'
     OR nombre ILIKE '%ingenier%'
  ORDER BY id_tipo_carrera
  LIMIT 1;

  IF v_id_tipo_uni IS NULL THEN
    RAISE EXCEPTION 'No se pudo resolver id_tipo_carrera para UNIVERSIDAD.';
  END IF;

  INSERT INTO carrera (nombre, duracion_semestres, activo, id_tipo_carrera, id_universidad)
  SELECT 'INGENIERIA EN SISTEMAS COMPUTACIONALES', 8, TRUE, v_id_tipo_uni, v_id_universidad
  WHERE NOT EXISTS (
    SELECT 1
    FROM carrera c
    WHERE c.id_universidad = v_id_universidad
      AND c.nombre = 'INGENIERIA EN SISTEMAS COMPUTACIONALES'
  );
END $$;

-- =========================================================
-- 3) Insertar materias ISC (Sem 1 a 8) (idempotente por clave)
-- =========================================================
WITH
u AS (
  SELECT id_universidad
  FROM universidad
  WHERE nombre = 'ESCOM'
  ORDER BY id_universidad
  LIMIT 1
),
c_isc AS (
  SELECT c.id_carrera
  FROM carrera c
  JOIN u ON u.id_universidad = c.id_universidad
  WHERE c.nombre = 'INGENIERIA EN SISTEMAS COMPUTACIONALES'
  ORDER BY c.id_carrera
  LIMIT 1
),
n_uni AS (
  SELECT id_nivel
  FROM nivel_educativo
  WHERE nombre ILIKE '%universidad%'
  ORDER BY id_nivel
  LIMIT 1
),
datos AS (
  SELECT *
  FROM (VALUES
    -- =========================
    -- SEMESTRE 1
    -- =========================
    ('UNI-ISC-S1-CAL',  'Cálculo', 7, 1, 3),
    ('UNI-ISC-S1-AV',   'Análisis Vectorial', 7, 1, 3),
    ('UNI-ISC-S1-MD',   'Matemáticas Discretas', 7, 1, 3),
    ('UNI-ISC-S1-COE',  'Comunicación Oral y Escrita', 7, 1, 2),
    ('UNI-ISC-S1-FP',   'Fundamentos de Programación', 7, 1, 3),

    -- =========================
    -- SEMESTRE 2
    -- =========================
    ('UNI-ISC-S2-AL',   'Álgebra Lineal', 7, 2, 3),
    ('UNI-ISC-S2-CA',   'Cálculo Aplicado', 7, 2, 3),
    ('UNI-ISC-S2-ME',   'Mecánica y Electromagnetismo', 7, 2, 4),
    ('UNI-ISC-S2-IES',  'Ingeniería, Ética y Sociedad', 7, 2, 3),
    ('UNI-ISC-S2-FE',   'Fundamentos Económicos', 7, 2, 3),
    ('UNI-ISC-S2-AED',  'Algoritmos y Estructura de Datos', 7, 2, 3),

    -- =========================
    -- SEMESTRE 3
    -- =========================
    ('UNI-ISC-S3-ED',   'Ecuaciones Diferenciales', 7, 3, 3),
    ('UNI-ISC-S3-CE',   'Circuitos Eléctricos', 7, 3, 3),
    ('UNI-ISC-S3-FDD',  'Fundamentos de Diseño Digital', 7, 3, 3),
    ('UNI-ISC-S3-BD',   'Bases de Datos', 7, 3, 3),
    ('UNI-ISC-S3-FIN',  'Finanzas Empresariales', 7, 3, 3),
    ('UNI-ISC-S3-PP',   'Paradigmas de Programación', 7, 3, 3),
    ('UNI-ISC-S3-ADA',  'Análisis y Diseño de Algoritmos', 7, 3, 3),

    -- =========================
    -- SEMESTRE 4
    -- =========================
    ('UNI-ISC-S4-PE',   'Probabilidad y Estadística', 7, 4, 3),
    ('UNI-ISC-S4-MAI',  'Matemáticas Avanzadas para la Ingeniería', 7, 4, 3),
    ('UNI-ISC-S4-EA',   'Electrónica Analógica', 7, 4, 3),
    ('UNI-ISC-S4-DSD',  'Diseño de Sistemas Digitales', 7, 4, 3),
    ('UNI-ISC-S4-TDAW', 'Tecnologías para el Desarrollo de Aplicaciones Web', 7, 4, 3),
    ('UNI-ISC-S4-SO',   'Sistemas Operativos', 7, 4, 3),
    ('UNI-ISC-S4-TC',   'Teoría de la Computación', 7, 4, 3),

    -- =========================
    -- SEMESTRE 5
    -- =========================
    ('UNI-ISC-S5-PDS',  'Procesamiento Digital de Señales', 7, 5, 3),
    ('UNI-ISC-S5-IC',   'Instrumentación y Control', 7, 5, 3),
    ('UNI-ISC-S5-ARQ',  'Arquitectura de Computadoras', 7, 5, 3),
    ('UNI-ISC-S5-ADS',  'Análisis y Diseño de Sistemas', 7, 5, 3),
    ('UNI-ISC-S5-FEPI', 'Formulación y Evaluación de Proyectos Informáticos', 7, 5, 3),
    ('UNI-ISC-S5-COMP', 'Compiladores', 7, 5, 3),
    ('UNI-ISC-S5-RC',   'Redes de Computadoras', 7, 5, 3),

    -- =========================
    -- SEMESTRE 6
    -- =========================
    ('UNI-ISC-S6-SEC',  'Sistemas en Chip', 7, 6, 3),
    ('UNI-ISC-S6-OPTA1','Optativa A1', 7, 6, 3),
    ('UNI-ISC-S6-OPTB1','Optativa B1', 7, 6, 3),
    ('UNI-ISC-S6-MCTD', 'Métodos Cuantitativos para la Toma de Decisiones', 7, 6, 3),
    ('UNI-ISC-S6-ISW',  'Ingeniería de Software', 7, 6, 3),
    ('UNI-ISC-S6-IA',   'Inteligencia Artificial', 7, 6, 3),
    ('UNI-ISC-S6-ACR',  'Aplicaciones para Comunicaciones en Red', 7, 6, 3),

    -- =========================
    -- SEMESTRE 7
    -- =========================
    ('UNI-ISC-S7-DAMN', 'Desarrollo de Aplicaciones Móviles Nativas', 7, 7, 3),
    ('UNI-ISC-S7-OPTA2','Optativa A2', 7, 7, 3),
    ('UNI-ISC-S7-OPTB2','Optativa B2', 7, 7, 3),
    ('UNI-ISC-S7-TT1',  'Trabajo Terminal I', 7, 7, 6),
    ('UNI-ISC-S7-SD',   'Sistemas Distribuidos', 7, 7, 3),
    ('UNI-ISC-S7-ASR',  'Administración de Servicios en Red', 7, 7, 3),

    -- =========================
    -- SEMESTRE 8
    -- =========================
    ('UNI-ISC-S8-EP',   'Estancia Profesional', 7, 8, 2),
    ('UNI-ISC-S8-DHAD', 'Desarrollo de Habilidades Sociales para la Alta Dirección', 7, 8, 2),
    ('UNI-ISC-S8-TT2',  'Trabajo Terminal II', 7, 8, 6),
    ('UNI-ISC-S8-GE',   'Gestión Empresarial', 7, 8, 3),
    ('UNI-ISC-S8-LP',   'Liderazgo Personal', 7, 8, 3)
  ) AS t(clave, nombre, creditos, nivel_sugerido, sesiones_por_semana)
)
INSERT INTO materia (clave, nombre, creditos, nivel_sugerido, sesiones_por_semana, id_carrera, id_nivel)
SELECT
  d.clave,
  d.nombre,
  d.creditos,
  d.nivel_sugerido,
  d.sesiones_por_semana,
  c_isc.id_carrera,
  n_uni.id_nivel
FROM datos d
CROSS JOIN c_isc
CROSS JOIN n_uni
WHERE NOT EXISTS (
  SELECT 1 FROM materia m WHERE m.clave = d.clave
);

COMMIT;