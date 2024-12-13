import os
import psycopg2
from psycopg2 import DatabaseError
from dotenv import load_dotenv

#cargar las variables de entorno
load_dotenv()

#Crear conexion con PostgreSQL
def get_db_connection():
    try:
        connection = psycopg2.connect(
            host=os.getenv('PGSQL_HOST'),
            user=os.getenv('PGSQL_USER'),
            password=os.getenv('PGSQL_PASSWORD'),
            dbname=os.getenv('PGSQL_DATABASE'),
            port=os.getenv('PGSQL_PORT')
        )
        return connection
    except DatabaseError as ex:
        raise ex