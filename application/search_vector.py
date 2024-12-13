import psycopg2
from infrastructure.adapters.db_connection import get_db_connection
import json
from psycopg2.extras import RealDictCursor

def buscar_candidatos_postgre(busqueda):
    print("Buscando...")
    # Formatear la búsqueda para usar en to_tsquery
    busqueda = ' & '.join(filter(None, busqueda.split()))
    # Limpieza de secuencias innecesarias
    busqueda = busqueda.strip(" & ")
    
    consulta = """
    SELECT 
        ap.id AS applicant_profile_id,
        u.name AS user_username,
        u.email AS email_username,
        j.name AS job_name,
        j.workmode AS work_mode,
        p.description AS profiletype,
        l.name AS level_exp,
        e.description AS skill_description,
        t.description AS type_contract
    FROM 
        recruitment.applicant_profile ap
        LEFT JOIN recruitment.user u ON ap.user_id = u.user_id
        LEFT JOIN recruitment.job j ON ap.id = j.id
        LEFT JOIN recruitment.profiletype p ON ap.id = p.id
        LEFT JOIN recruitment.levelofexp l ON ap.id = l.id
        LEFT JOIN recruitment.skills e ON ap.id = e.id
        LEFT JOIN recruitment.typeofcontract t ON ap.id = t.id
    WHERE 
        to_tsvector(
            'spanish',
            coalesce(j.name, '') || ' ' ||
            coalesce(j.workmode, '') || ' ' ||
            coalesce(p.description, '') || ' ' ||
            coalesce(l.name, '') || ' ' ||
            coalesce(e.description, '') || ' ' ||
            coalesce(t.description, '')
        ) @@ to_tsquery('spanish', %s)
    ORDER BY ap.id
    LIMIT 10;
    """
    
    resultados = []
    try:
        conn = get_db_connection()  # Obtén la conexión a la base de datos
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            # Ejecutar la consulta con el término de búsqueda seguro
            cur.execute(consulta, (busqueda,))
            resultados = cur.fetchall()
        conn.close()
    except Exception as e:
        print(f"Error al consultar PostgreSQL: {e}")
    
    # Convertir los resultados en una lista de diccionarios
    # return json.dumps([dict(row) for row in resultados], default=str)
    return [dict(row) for row in resultados]


