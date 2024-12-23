import os
import psycopg2
from psycopg2 import DatabaseError
from src.infrastructure.ports.db_conection_port import DBConnectionPort
import logging

# Configura el logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

class PostgresDBAdapter(DBConnectionPort):
    """
    Adaptador para manejar la conexión con la base de datos PostgreSQL.
    """
    
    def __init__(self, host=None, user=None, password=None, dbname=None, port=None):
        self.host = host or "search_ai_postgres"
        self.user = user or os.getenv('POSTGRES_USER')
        self.password = password or "12345678"
        self.dbname = dbname or os.getenv('POSTGRES_DB')
        self.port = port or os.getenv('POSTGRES_PORT')
        
        logger.debug(f"Configuración de la base de datos: host={self.host}, dbname={self.dbname}, port={self.port}, user={self.user}")
        
    def get_connection(self):
        """
        Crea y devuelve una conexión a la base de datos PostgreSQL.
        
        Raises:
            DatabaseError: Si ocurre algún error al intentar conectar.
        
        Returns:
            connection: Objeto de conexión a PostgreSQL.
        """
        try:
            logger.debug(f"Intentando conectar a la base de datos en {self.host}:{self.port} con el usuario {self.user}...")
            connection = psycopg2.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                dbname=self.dbname,
                port=self.port
            )
            logger.debug("Conexión exitosa a PostgreSQL.")
            return connection
        except DatabaseError as ex:
            logger.error(f"Error al conectar con PostgreSQL: {ex}")
            logger.debug(f"Detalles completos del error: {ex.pgcode}, {ex.pgerror}, {ex.diag.message_primary}")
            raise DatabaseError(f"Error al conectar con PostgreSQL: {ex}")