-- BASE DE DATOS NORMALIZADA (POSTGRESQL)
-- Script para generar la estructura de la base de datos, contiene las tablas y sus relaciones
-- 1) TABLAS DE APOYO / CATÁLOGOS
-- -----------------------------------------------------

CREATE TABLE nivel_educativo (
    id_nivel SERIAL PRIMARY KEY,
    nombre   VARCHAR(50) NOT NULL
);

CREATE TABLE universidad (
    id_universidad SERIAL PRIMARY KEY,
    nombre         VARCHAR(150) NOT NULL,
    ciudad         VARCHAR(100),
    estado         VARCHAR(100),
    pais           VARCHAR(100)
);

CREATE TABLE area_interes (
    id_area SERIAL PRIMARY KEY,
    nombre  VARCHAR(100) NOT NULL
);

CREATE TABLE cat_rol_admin (
    id_rol_admin SERIAL PRIMARY KEY,
    nombre       VARCHAR(50) NOT NULL
);

CREATE TABLE cat_tipo_relacion_tutor (
    id_tipo_relacion SERIAL PRIMARY KEY,
    nombre           VARCHAR(50) NOT NULL
);

CREATE TABLE cat_tipo_carrera (
    id_tipo_carrera SERIAL PRIMARY KEY,
    nombre          VARCHAR(30) NOT NULL
);

CREATE TABLE cat_turno (
    id_turno SERIAL PRIMARY KEY,
    nombre   VARCHAR(20) NOT NULL
);

CREATE TABLE cat_estado_alumno (
    id_estado_alumno SERIAL PRIMARY KEY,
    nombre           VARCHAR(20) NOT NULL
);

CREATE TABLE cat_estado_inscripcion (
    id_estado_inscripcion SERIAL PRIMARY KEY,
    nombre                VARCHAR(20) NOT NULL
);

CREATE TABLE cat_tipo_incidente (
    id_tipo_incidente SERIAL PRIMARY KEY,
    nombre            VARCHAR(20) NOT NULL
);

CREATE TABLE cat_gravedad_incidente (
    id_gravedad_incidente SERIAL PRIMARY KEY,
    nombre                VARCHAR(20) NOT NULL
);

CREATE TABLE cat_estado_historial (
    id_estado_historial SERIAL PRIMARY KEY,
    nombre              VARCHAR(20) NOT NULL
);

-- 2) USUARIO ADMINISTRADOR
-- -----------------------------------------------------

CREATE TABLE usuario_admin (
    id_admin      SERIAL PRIMARY KEY,
    num_empleado  VARCHAR(50)  NOT NULL UNIQUE,
    usuario       VARCHAR(50)  NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    nombre        VARCHAR(100) NOT NULL,
    correo        VARCHAR(100) NOT NULL,
    id_rol_admin  INT NOT NULL,
    CONSTRAINT fk_usuario_admin_rol
        FOREIGN KEY (id_rol_admin)
        REFERENCES cat_rol_admin(id_rol_admin)
);

-- 3) PADRE / TUTOR
-- -----------------------------------------------------

CREATE TABLE padre_tutor (
    id_tutor        SERIAL PRIMARY KEY,
    nombre          VARCHAR(100) NOT NULL,
    ape_paterno     VARCHAR(100) NOT NULL,
    ape_materno     VARCHAR(100),
    telefono        VARCHAR(20),
    correo          VARCHAR(100),
    direccion       VARCHAR(200),
    id_tipo_relacion INT,
    CONSTRAINT fk_tutor_tipo_relacion
        FOREIGN KEY (id_tipo_relacion)
        REFERENCES cat_tipo_relacion_tutor(id_tipo_relacion)
);

-- 4) DOCENTE Y ÁREAS DE INTERÉS
-- -----------------------------------------------------

CREATE TABLE docente (
    id_docente   SERIAL PRIMARY KEY,
    num_empleado VARCHAR(50)  NOT NULL UNIQUE,
    nombre       VARCHAR(100) NOT NULL,
    ape_paterno  VARCHAR(100) NOT NULL,
    ape_materno  VARCHAR(100),
    correo       VARCHAR(100),
    telefono     VARCHAR(20),
    especialidad VARCHAR(100),
    fecha_ingreso DATE,
    activo       BOOLEAN DEFAULT TRUE
);

CREATE TABLE docente_area_interes (
    id_docente INT NOT NULL,
    id_area    INT NOT NULL,
    PRIMARY KEY (id_docente, id_area),
    CONSTRAINT fk_doc_area_docente
        FOREIGN KEY (id_docente)
        REFERENCES docente(id_docente),
    CONSTRAINT fk_doc_area_area
        FOREIGN KEY (id_area)
        REFERENCES area_interes(id_area)
);

-- 5) CARRERAS Y MATERIAS
-- -----------------------------------------------------

CREATE TABLE carrera (
    id_carrera         SERIAL PRIMARY KEY,
    nombre             VARCHAR(150) NOT NULL,
    id_tipo_carrera    INT,
    duracion_semestres INT,
    activo             BOOLEAN DEFAULT TRUE,
    id_universidad     INT,
    CONSTRAINT fk_carrera_universidad
        FOREIGN KEY (id_universidad)
        REFERENCES universidad(id_universidad),
    CONSTRAINT fk_carrera_tipo
        FOREIGN KEY (id_tipo_carrera)
        REFERENCES cat_tipo_carrera(id_tipo_carrera)
);

CREATE TABLE materia (
    id_materia      SERIAL PRIMARY KEY,
    clave           VARCHAR(50)  NOT NULL UNIQUE,
    nombre          VARCHAR(150) NOT NULL,
    creditos        INT          NOT NULL DEFAULT 7,
    nivel_sugerido  INT,
    id_carrera      INT,
    id_nivel        INT NOT NULL,
    CONSTRAINT fk_materia_carrera
        FOREIGN KEY (id_carrera)
        REFERENCES carrera(id_carrera),
    CONSTRAINT fk_materia_nivel
        FOREIGN KEY (id_nivel)
        REFERENCES nivel_educativo(id_nivel)
);

-- 6) ALUMNO
-- -----------------------------------------------------

CREATE TABLE alumno (
    id_alumno        SERIAL PRIMARY KEY,
    boleta           VARCHAR(20)  NOT NULL UNIQUE,
    nombre           VARCHAR(100) NOT NULL,
    ape_paterno      VARCHAR(100) NOT NULL,
    ape_materno      VARCHAR(100),
    correo           VARCHAR(100),
    telefono         VARCHAR(20),
    fecha_nacimiento DATE,
    id_estado_alumno INT,
    fecha_alta       DATE,
    semestre_actual  INT,
    id_nivel         INT NOT NULL,
    id_carrera       INT,
    id_tutor         INT,
    CONSTRAINT fk_alumno_nivel
        FOREIGN KEY (id_nivel)
        REFERENCES nivel_educativo(id_nivel),
    CONSTRAINT fk_alumno_carrera
        FOREIGN KEY (id_carrera)
        REFERENCES carrera(id_carrera),
    CONSTRAINT fk_alumno_tutor
        FOREIGN KEY (id_tutor)
        REFERENCES padre_tutor(id_tutor),
    CONSTRAINT fk_alumno_estado
        FOREIGN KEY (id_estado_alumno)
        REFERENCES cat_estado_alumno(id_estado_alumno)
);

-- 7) GRUPOS Y HORARIOS
-- -----------------------------------------------------

CREATE TABLE grupo (
    id_grupo    SERIAL PRIMARY KEY,
    clave_grupo VARCHAR(50) NOT NULL,
    grado       INT,
    periodo     VARCHAR(20) NOT NULL,
    id_turno    INT,
    id_nivel    INT NOT NULL,
    id_materia  INT NOT NULL,
    id_docente  INT NOT NULL,
    CONSTRAINT fk_grupo_nivel
        FOREIGN KEY (id_nivel)
        REFERENCES nivel_educativo(id_nivel),
    CONSTRAINT fk_grupo_materia
        FOREIGN KEY (id_materia)
        REFERENCES materia(id_materia),
    CONSTRAINT fk_grupo_docente
        FOREIGN KEY (id_docente)
        REFERENCES docente(id_docente),
    CONSTRAINT fk_grupo_turno
        FOREIGN KEY (id_turno)
        REFERENCES cat_turno(id_turno)
);

CREATE TABLE horario (
    id_horario  SERIAL PRIMARY KEY,
    dia_semana  SMALLINT NOT NULL,
    hora_inicio TIME     NOT NULL,
    hora_fin    TIME     NOT NULL,
    aula        VARCHAR(50),
    id_grupo    INT NOT NULL,
    CONSTRAINT fk_horario_grupo
        FOREIGN KEY (id_grupo)
        REFERENCES grupo(id_grupo)
);

-- 8) RELACIÓN ALUMNO – GRUPO (INSCRIPCIONES)
-- -----------------------------------------------------

CREATE TABLE alumno_grupo (
    id_alumno           INT NOT NULL,
    id_grupo            INT NOT NULL,
    id_estado_inscripcion INT,
    fecha_inscripcion   DATE,
    PRIMARY KEY (id_alumno, id_grupo),
    CONSTRAINT fk_alumno_grupo_alumno
        FOREIGN KEY (id_alumno)
        REFERENCES alumno(id_alumno),
    CONSTRAINT fk_alumno_grupo_grupo
        FOREIGN KEY (id_grupo)
        REFERENCES grupo(id_grupo),
    CONSTRAINT fk_alumno_grupo_estado
        FOREIGN KEY (id_estado_inscripcion)
        REFERENCES cat_estado_inscripcion(id_estado_inscripcion)
);

-- 9) HISTORIAL ACADÉMICO
-- -----------------------------------------------------

CREATE TABLE historial_academico (
    id_historial       SERIAL PRIMARY KEY,
    id_alumno          INT NOT NULL,
    id_materia         INT NOT NULL,
    periodo            VARCHAR(20) NOT NULL,
    calificacion       NUMERIC(3,1),
    id_estado_historial INT,
    CONSTRAINT fk_hist_alumno
        FOREIGN KEY (id_alumno)
        REFERENCES alumno(id_alumno),
    CONSTRAINT fk_hist_materia
        FOREIGN KEY (id_materia)
        REFERENCES materia(id_materia),
    CONSTRAINT fk_hist_estado
        FOREIGN KEY (id_estado_historial)
        REFERENCES cat_estado_historial(id_estado_historial)
);

-- 10) INCIDENTES
-- -----------------------------------------------------

CREATE TABLE incidente (
    id_incidente         SERIAL PRIMARY KEY,
    id_tipo_incidente    INT NOT NULL,
    fecha                DATE        NOT NULL,
    descripcion          TEXT        NOT NULL,
    id_gravedad_incidente INT,
    id_alumno            INT,
    id_docente           INT,
    id_admin             INT NOT NULL,
    CONSTRAINT fk_incidente_tipo
        FOREIGN KEY (id_tipo_incidente)
        REFERENCES cat_tipo_incidente(id_tipo_incidente),
    CONSTRAINT fk_incidente_gravedad
        FOREIGN KEY (id_gravedad_incidente)
        REFERENCES cat_gravedad_incidente(id_gravedad_incidente),
    CONSTRAINT fk_incidente_alumno
        FOREIGN KEY (id_alumno)
        REFERENCES alumno(id_alumno),
    CONSTRAINT fk_incidente_docente
        FOREIGN KEY (id_docente)
        REFERENCES docente(id_docente),
    CONSTRAINT fk_incidente_admin
        FOREIGN KEY (id_admin)
        REFERENCES usuario_admin(id_admin)
);