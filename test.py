import psycopg2

conn = psycopg2.connect(
    dbname="search_ia_db",  # Nombre de la base de datos correcta
    user="asleep2049",
    password="12345678",
    host="localhost",
    port="5432"
)
