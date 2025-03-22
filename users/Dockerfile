# Usa Python como base
FROM python:3.11

# Define el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto
COPY . .

# Instala dependencias
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto de Django
EXPOSE 8000

# Comando para ejecutar el servidor con Gunicorn
CMD ["sh", "-c", "sleep 3 && python manage.py makemigrations && python manage.py migrate && gunicorn --bind 0.0.0.0:8000 users.wsgi:application"]
#CMD ["gunicorn", "--bind", "0.0.0.0:8000", "users.wsgi:application"]