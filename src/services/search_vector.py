from src.infrastructure.ports.db_conection_port import DBConnectionPort
from psycopg2.extras import RealDictCursor

class CandidateSearchService:
    def __init__(self, db_connection: DBConnectionPort):
        """
        Servicio para buscar candidatos en la base de datos.
        :param db_connection: Función para obtener la conexión a la base de datos.
        """
        self.db_connection = db_connection

    def buscar_candidatos(self, rol, capabilities):
        """
        Busca candidatos en la base de datos que coincidan con un rol y habilidades específicas.

        :param rol: Cadena que describe el rol buscado.
        :param capabilities: Lista de habilidades requeridas.
        :return: Lista de diccionarios con los resultados de la búsqueda.
        """
        if not isinstance(rol, str):
            raise ValueError("El parámetro 'rol' debe ser una cadena.")

        # Formatear la búsqueda para usar en to_tsquery
        busqueda_rol = rol.strip()  # Eliminar espacios innecesarios
        busqueda_rol = ' & '.join(busqueda_rol.split())  # Reemplazar espacios por " & " para to_tsquery

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
            conn = self.db_connection.get_connection()  # Obtén la conexión a la base de datos
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                # Ejecutar la consulta con el término de búsqueda seguro
                cur.execute(consulta, (tuple(capabilities), busqueda_rol))
                resultados = cur.fetchall()
            conn.close()
        except Exception as e:
            print(f"Error al consultar PostgreSQL: {e}")

        # Convertir los resultados en una lista de diccionarios
        return [dict(row) for row in resultados]
