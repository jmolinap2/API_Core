# Usa la imagen base de Python 3.9 slim
FROM python:3.9.0rc1-slim

# Instala las dependencias del sistema necesarias para psycopg2 y PostgreSQL
RUN apt-get update && \
    apt-get install -y libpq-dev gcc postgresql-client

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia los archivos de requerimientos y las migraciones previamente generadas
COPY requirements.txt ./
COPY ./api/migrations/ ./api/migrations/

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de los archivos de tu proyecto
COPY . .

# Expón el puerto 8000 para acceder a la aplicación
EXPOSE 8000

# Comando de inicio para ejecutar el servidor Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
