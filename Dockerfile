# Usa una imagen base de Python
FROM python:3.10-bookworm

# Establece el directorio de trabajo
WORKDIR /app

RUN pip install flask-cors flask psycopg2


COPY ./src ./src
COPY app.py .

EXPOSE 5001

CMD ["python", "app.py"]