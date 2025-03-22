# Usa Python como base
FROM python:3.11

# Define el directorio de trabajo
WORKDIR /bff

# Copia los archivos necesarios
COPY requirements.txt /bff
COPY . /bff

# Instala dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto de Django
EXPOSE 8000

# Comando para ejecutar el servidor con Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "bff.wsgi:application"]