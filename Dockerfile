# Usa una imagen base de Python
FROM python:3.10-bookworm

# Establece el directorio de trabajo
WORKDIR /app

RUN pip install flask-cors flask psycopg2

# Copia el directorio de la aplicación

COPY ./src ./src
COPY app.py .
# Exponer el puerto
EXPOSE 5001

CMD ["python", "app.py"]
