-- Mostrar tablas y atributops
-- mostrar tablas de esquema

SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;

-- mostrar todas las columnas
SELECT 
    table_name AS tabla,
    column_name AS atributo,
    data_type AS tipo_dato,
    is_nullable AS permite_nulos,
    column_default AS valor_default
FROM information_schema.columns
WHERE table_schema = 'public'
ORDER BY table_name, ordinal_position;

-- mostrar columnas PK y FK

SELECT 
    tc.table_name,
    kcu.column_name
FROM 
    information_schema.table_constraints AS tc
JOIN 
    information_schema.key_column_usage AS kcu
      ON tc.constraint_name = kcu.constraint_name
WHERE 
    tc.constraint_type = 'PRIMARY KEY'
    AND tc.table_schema = 'public'
ORDER BY tc.table_name;


-- FK

SELECT
    tc.table_name AS tabla,
    kcu.column_name AS columna,
    ccu.table_name AS tabla_referenciada,
    ccu.column_name AS columna_referenciada
FROM 
    information_schema.table_constraints AS tc
JOIN 
    information_schema.key_column_usage AS kcu
      ON tc.constraint_name = kcu.constraint_name
JOIN 
    information_schema.constraint_column_usage AS ccu
      ON ccu.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY'
ORDER BY tc.table_name;


-- Estructura de una tabla

SELECT 
    column_name,
    data_type,
    character_maximum_length,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name = 'alumno';
