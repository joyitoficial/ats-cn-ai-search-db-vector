-- Insertar niveles de experiencia
INSERT INTO recruitment.levelofexp (name) VALUES 
('Junior'), 
('Semi-Senior'), 
('Senior'), 
('Experto');

-- Insertar tipos de perfil
INSERT INTO recruitment.profiletype (description) VALUES 
('Desarrollo de Software'), 
('Diseño UX/UI'), 
('Gestión de Proyectos'), 
('Análisis de Datos');

-- Insertar habilidades
INSERT INTO recruitment.skills (description) VALUES 
('Python'), 
('JavaScript'), 
('React'), 
('SQL'), 
('Machine Learning'), 
('Docker'), 
('Kubernetes'), 
('Diseño de Interfaz'), 
('Gestión Ágil'), 
('Análisis Estadístico');

-- Insertar usuarios
INSERT INTO recruitment.user (name, email) VALUES 
('Juan Pérez', 'juan.perez@example.com'),
('María González', 'maria.gonzalez@example.com'),
('Carlos Rodríguez', 'carlos.rodriguez@example.com'),
('Ana Martínez', 'ana.martinez@example.com'),
('Luis Silva', 'luis.silva@example.com');

-- Insertar perfiles de candidatos
INSERT INTO recruitment.applicant_profile (user_id) 
SELECT user_id FROM recruitment.user;

-- Insertar habilidades de candidatos
INSERT INTO recruitment.applicantprofile_skill (applicant_profile_id, skill_id)
VALUES 
(1, 1), (1, 2), (1, 4),
(2, 3), (2, 4), (2, 8),
(3, 5), (3, 6), (3, 7),
(4, 9), (4, 10),
(5, 1), (5, 3), (5, 5);

-- Insertar trabajos
INSERT INTO recruitment.job (name, levelofexperience_id, profile_type_id) VALUES 
('Desarrollador Python', 1, 1),
('Desarrollador Full Stack', 2, 1),
('Diseñador UX', 2, 2),
('Científico de Datos', 3, 4),
('Líder de Proyecto', 3, 3);

-- Insertar experiencia laboral
INSERT INTO recruitment.workexperience (applicantprofile_id, description) VALUES 
(1, 'Desarrollador backend en empresa de tecnología'),
(2, 'Diseñador freelance de interfaces web'),
(3, 'Ingeniero de Machine Learning en startup'),
(4, 'Consultor de gestión de proyectos'),
(5, 'Investigador de ciencia de datos');

-- Insertar postulaciones
INSERT INTO recruitment.application (user_id, job_id) VALUES 
(1, 1),
(2, 3),
(3, 4),
(4, 5),
(5, 2);