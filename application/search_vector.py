import psycopg2
from infrastructure.adapters.db_connection import get_db_connection
import json
from psycopg2.extras import RealDictCursor

def buscar_candidatos_postgre(rol, capabilities):
    # Formatear la búsqueda para usar en to_tsquery
    
    if isinstance(rol, str):
        busqueda_rol = rol.strip()  # Eliminar espacios innecesarios
        busqueda_rol = ' & '.join(busqueda_rol.split())  # Reemplazar espacios por " & " para to_tsquery
    else:
        raise ValueError("El parámetro 'rol' debe ser una cadena.")

    print(capabilities, busqueda_rol)

    # INDICES
    #     -- Índices para las columnas involucradas en JOINs
    # CREATE INDEX idx_app_skill_applicant_profile_id ON recruitment.applicantprofile_skill(applicant_profile_id);
    # CREATE INDEX idx_skills_id ON recruitment.skills(id);
    # CREATE INDEX idx_user_user_id ON recruitment.user(user_id);
    # CREATE INDEX idx_job_id ON recruitment.job(id);
    # CREATE INDEX idx_levelofexp_id ON recruitment.levelofexp(id);
    # CREATE INDEX idx_prof_type_id ON recruitment.profiletype(id);
    # CREATE INDEX idx_workexp_applicantprofile_id ON recruitment.workexperience(applicantprofile_id);

    # -- Índices para las columnas de búsqueda de texto completo
    # CREATE INDEX idx_job_name_tsvector ON recruitment.job USING gin(to_tsvector('spanish', name));
    # CREATE INDEX idx_job_workmode_tsvector ON recruitment.job USING gin(to_tsvector('spanish', workmode));
    # CREATE INDEX idx_skills_description_tsvector ON recruitment.skills USING gin(to_tsvector('spanish', description));
    # CREATE INDEX idx_workexp_description_tsvector ON recruitment.workexperience USING gin(to_tsvector('spanish', description));
    # CREATE INDEX idx_levelofexp_name_tsvector ON recruitment.levelofexp USING gin(to_tsvector('spanish', name));
    # CREATE INDEX idx_prof_type_description_tsvector ON recruitment.profiletype USING gin(to_tsvector('spanish', description));

    
    consulta = """
    
    WITH filtered_skills AS (
    SELECT id, description
    FROM recruitment.skills
    WHERE description IN %s
),
filtered_job_profile AS (
    SELECT jobs.id AS job_id, jobs.name AS job_name, level_of_exp.name AS level_name, jobs.profile_type_id AS profile_type_id, profiles_type.description AS profile_type_description
    FROM recruitment.job AS jobs
    INNER JOIN recruitment.levelofexp AS level_of_exp 
        ON level_of_exp.id = jobs.levelofexperience_id
    INNER JOIN recruitment.profiletype AS profiles_type
        ON jobs.profile_type_id = profiles_type.id
    WHERE to_tsvector('spanish', jobs.name || ' ' || profiles_type.description || ' ' || level_of_exp.name) 
        @@ to_tsquery('spanish', %s)
)
SELECT 
    a_p.id AS applicant_profile_id,
    u.name AS user_name, 
    job.job_name,
    job.level_name AS level_of_exp, 
    job.profile_type_description AS profile_type,
    ARRAY_AGG(skills.description) AS skills,
	workexperience.description AS aditional_info
FROM 
    recruitment.user AS u
INNER JOIN 
    recruitment.applicant_profile AS a_p ON u.user_id = a_p.user_id
INNER JOIN 
    recruitment.applicantprofile_skill AS a_p_skill ON a_p_skill.applicant_profile_id = a_p.id
INNER JOIN 
    filtered_skills AS skills ON skills.id = a_p_skill.skill_id
INNER JOIN 
    recruitment.application AS application ON u.user_id = application.user_id
INNER JOIN 
    filtered_job_profile AS job ON job.job_id = application.job_id
INNER JOIN 
	recruitment.workexperience AS workexperience on workexperience.applicantprofile_id = a_p.id
GROUP BY 
    a_p.id, u.name, job.job_name, job.job_id, job.level_name, job.profile_type_description, workexperience.description; 

    """
    resultados = []
    try:
        conn = get_db_connection()  # Obtén la conexión a la base de datos
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            # Ejecutar la consulta con el término de búsqueda seguro
            cur.execute(consulta, ((tuple(capabilities),busqueda_rol)))
            resultados = cur.fetchall()

        conn.close()
    except Exception as e:
        print(f"Error al consultar PostgreSQL: {e}")
    
    # Convertir los resultados en una lista de diccionarios
    # return json.dumps([dict(row) for row in resultados], default=str)
    return [dict(row) for row in resultados]