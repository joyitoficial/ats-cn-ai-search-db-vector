# Usa una imagen base de Python
FROM python:3.9

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo de requisitos
COPY requirements.txt ./  

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el directorio de la aplicación
COPY ./application ./application 
COPY ./infrastructure ./infrastructure 

# Exponer el puerto
EXPOSE 5001

# Establece el comando por defecto para iniciar la aplicación
CMD ["python", "-m", "application.app"]
