import psycopg2
from infrastructure.adapters.db_connection import get_db_connection
import json
from psycopg2.extras import RealDictCursor

def buscar_candidatos_postgre(rol, capabilities):
    # Formatear la búsqueda para usar en to_tsquery
    
    busqueda_capabilities = ' | '.join(
            [f"'{capability.strip()}'" if ' ' in capability else capability.strip() for capability in capabilities]
        )

    if busqueda_capabilities.startswith(" | "):
        busqueda_capabilities = busqueda_capabilities[3:]
    if busqueda_capabilities.endswith(" | "):
        busqueda_capabilities = busqueda_capabilities[:-3]
        
    if isinstance(rol, str):
        busqueda_rol = rol.strip()  # Eliminar espacios innecesarios
        busqueda_rol = ' & '.join(busqueda_rol.split())  # Reemplazar espacios por " & " para to_tsquery
    else:
        raise ValueError("El parámetro 'rol' debe ser una cadena.")

    print(busqueda_capabilities, busqueda_rol)

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
    SET enable_nestloop = off; 
    
    WITH ranked_profiles AS (
    SELECT 
        app_prof.id AS applicant_profile_id,
        u.name AS name,
        skills.description AS skill_description,
        job.name AS job_name,
        level_of_exp.name AS level_of_experience,
        prof_type.description AS profiletype,
        workexp.description AS aditional_info
    FROM 
        recruitment.applicantprofile_skill AS app_skill
    INNER JOIN recruitment.applicant_profile AS app_prof ON app_skill.applicant_profile_id = app_prof.id
    INNER JOIN recruitment.skills AS skills ON skills.id = app_skill.skill_id
    INNER JOIN recruitment.user AS u ON u.user_id = app_prof.user_id
    INNER JOIN recruitment.application AS application ON application.user_id = u.user_id
    INNER JOIN recruitment.job AS job ON job.id = application.job_id
    INNER JOIN recruitment.levelofexp AS level_of_exp ON level_of_exp.id = job.levelofexperience_id
    INNER JOIN recruitment.profiletype AS prof_type ON prof_type.id = job.profile_type_id
    INNER JOIN recruitment.workexperience as workexp ON workexp.applicantprofile_id = app_prof.id
    WHERE 
        -- Usar tsquery para el filtrado en lugar de recalcular el tsvector cada vez
        to_tsvector('spanish', job.name || ' ' || skills.description || ' ' || workexp.description || ' ' || level_of_exp.name)
        @@ to_tsquery('spanish', %s)
        AND
        to_tsvector('spanish', prof_type.description || ' ' || level_of_exp.name) 
        @@ to_tsquery('spanish', %s)
),
ranked_with_row_number AS (
    SELECT 
    applicant_profile_id,
    MIN(name) AS name,
    MIN(skill_description) AS skill_description,
    MIN(job_name) AS job_name,
    MIN(level_of_experience) AS level_of_experience,
    MIN(profiletype) AS profiletype,
    MIN(aditional_info) AS aditional_info
    FROM ranked_profiles
    GROUP BY applicant_profile_id
)
SELECT 
    applicant_profile_id,
    name,
    skill_description,
    job_name,
    level_of_experience,
    profiletype,
    aditional_info
FROM ranked_with_row_number
    """
    resultados = []
    try:
        conn = get_db_connection()  # Obtén la conexión a la base de datos
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            # Ejecutar la consulta con el término de búsqueda seguro
            cur.execute(consulta, (busqueda_capabilities,busqueda_rol))
            resultados = cur.fetchall()

        conn.close()
    except Exception as e:
        print(f"Error al consultar PostgreSQL: {e}")
    
    # Convertir los resultados en una lista de diccionarios
    # return json.dumps([dict(row) for row in resultados], default=str)
    return [dict(row) for row in resultados]