-- =========================================================
-- 1) INGRESAR NIVELES ACADEMICOS
-- =========================================================
INSERT INTO nivel_educativo (id_nivel, nombre) VALUES
(1, 'KINDER'),
(2, 'PRIMARIA'),
(3, 'SECUNDARIA'),
(4, 'PREPARATORIA'),
(5, 'UNIVERSIDAD');

-- =========================================================
-- 1) INGRESAR REGLA HORARIOS
-- =========================================================
INSERT INTO regla_horario (
    id_nivel,
    semestre,
    tipo_alumno,
    duracion_bloque_min,
    materias_max_por_dia,
    descanso_duracion_min,
    descanso_despues_bloque,
    permitir_taller,
    bloque_taller,
    carga_docente_max,
    activo
) VALUES (
    (SELECT id_nivel FROM nivel_educativo WHERE nombre = 'KINDER'),
    NULL,      -- semestre: no aplica para Kínder
    NULL,      -- tipo_alumno: no aplica para Kínder
    90,        -- duración por bloque (puedes subir a 90 si quieres)
    5,         -- máximo de clases por día para Kínder
    30,        -- descanso de 30 minutos
    2,         -- descanso después de 2 bloques
    FALSE,     -- permitir_taller
    NULL,      -- bloque_taller
    4,         -- carga máxima de grupos por docente (ejemplo)
    TRUE       -- regla activa
);



