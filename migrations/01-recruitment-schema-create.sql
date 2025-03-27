-- Crear el schema de reclutamiento
CREATE SCHEMA IF NOT EXISTS recruitment;

-- Tabla de niveles de experiencia
CREATE TABLE recruitment.levelofexp (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

-- Tabla de tipos de perfil
CREATE TABLE recruitment.profiletype (
    id SERIAL PRIMARY KEY,
    description VARCHAR(100) NOT NULL UNIQUE
);

-- Tabla de habilidades
CREATE TABLE recruitment.skills (
    id SERIAL PRIMARY KEY,
    description VARCHAR(100) NOT NULL UNIQUE
);

-- Tabla de usuarios
CREATE TABLE recruitment.user (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

-- Tabla de perfiles de candidatos
CREATE TABLE recruitment.applicant_profile (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES recruitment.user(user_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de trabajos/puestos
CREATE TABLE recruitment.job (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    levelofexperience_id INTEGER REFERENCES recruitment.levelofexp(id),
    profile_type_id INTEGER REFERENCES recruitment.profiletype(id)
);

-- Tabla de relación entre perfiles de candidatos y habilidades
CREATE TABLE recruitment.applicantprofile_skill (
    applicant_profile_id INTEGER REFERENCES recruitment.applicant_profile(id),
    skill_id INTEGER REFERENCES recruitment.skills(id),
    PRIMARY KEY (applicant_profile_id, skill_id)
);

-- Tabla de experiencia laboral
CREATE TABLE recruitment.workexperience (
    id SERIAL PRIMARY KEY,
    applicantprofile_id INTEGER REFERENCES recruitment.applicant_profile(id),
    description TEXT
);

-- Tabla de postulaciones
CREATE TABLE recruitment.application (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES recruitment.user(user_id),
    job_id INTEGER REFERENCES recruitment.job(id),
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);