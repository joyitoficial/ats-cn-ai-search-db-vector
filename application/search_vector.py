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
    
    consulta = """
SELECT DISTINCT ON (app_prof.id)
    app_prof.id AS applicant_profile_id,
    u.name AS name,
    array_agg(DISTINCT skills.description) AS skill_descriptions,
    job.name AS job_name,
    level_of_exp.name AS level_of_experience,
    prof_type.description AS profiletype,
    workexp.description AS aditional_info,
    ts_rank(
        to_tsvector('spanish', 
            COALESCE(u.name, '') || ' ' ||
            COALESCE(job.name, '') || ' ' ||
            COALESCE(job.workmode, '') || ' ' ||
            COALESCE(skills.description, '') || ' ' ||
            COALESCE(workexp.description, '') || ' ' ||
            COALESCE(level_of_exp.name, '')
        ), 
        to_tsquery('spanish', %s)
    ) * 100 AS score_capabilities,
    
    ts_rank(
        to_tsvector('spanish', 
            COALESCE(prof_type.description, '') || ' ' ||
            COALESCE(level_of_exp.name, '')
        ), 
        to_tsquery('spanish', %s)
    ) * 100 AS score_role

FROM 
    recruitment.applicantprofile_skill AS app_skill
    LEFT JOIN recruitment.applicant_profile AS app_prof 
        ON app_skill.applicant_profile_id = app_prof.id
    INNER JOIN recruitment.skills AS skills 
        ON skills.id = app_skill.skill_id
    INNER JOIN recruitment.user AS u 
        ON u.user_id = app_prof.user_id
    LEFT JOIN recruitment.application AS application 
        ON application.user_id = u.user_id
    LEFT JOIN recruitment.job AS job 
        ON job.id = application.job_id
    LEFT JOIN recruitment.levelofexp AS level_of_exp 
        ON level_of_exp.id = job.levelofexperience_id
    LEFT JOIN recruitment.profiletype AS prof_type
        ON prof_type.id = job.profile_type_id
    LEFT JOIN recruitment.workexperience as workexp
        ON workexp.applicantprofile_id = app_prof.id
WHERE 
    to_tsvector(
        'spanish', 
        COALESCE(u.name, '') || ' ' ||
        COALESCE(job.name, '') || ' ' ||
        COALESCE(job.workmode, '') || ' ' ||
        COALESCE(skills.description, '') || ' ' ||
        COALESCE(workexp.description, '') || ' ' ||
        COALESCE(level_of_exp.name, '')
    ) @@ to_tsquery('spanish', %s)
     AND
    to_tsvector('spanish',
        COALESCE(prof_type.description, '') || ' ' ||
        COALESCE(level_of_exp.name, '') 
    ) @@ to_tsquery('spanish', %s)
GROUP BY
    u.name, job.name, level_of_exp.name, prof_type.description, app_prof.id, workexp.description, 
    job.workmode, skills.description
ORDER BY 
    app_prof.id, score_capabilities DESC, score_role DESC;
;

    """
    resultados = []
    try:
        conn = get_db_connection()  # Obtén la conexión a la base de datos
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            # Ejecutar la consulta con el término de búsqueda seguro
            cur.execute(consulta, (busqueda_capabilities,busqueda_rol,
                                   busqueda_capabilities,busqueda_rol))
            resultados = cur.fetchall()

        conn.close()
    except Exception as e:
        print(f"Error al consultar PostgreSQL: {e}")
    
    # Convertir los resultados en una lista de diccionarios
    # return json.dumps([dict(row) for row in resultados], default=str)
    return [dict(row) for row in resultados]