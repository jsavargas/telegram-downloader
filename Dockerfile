# Usar una imagen base de Python
FROM python:slim-bullseye

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar los archivos requirements.txt y bot.py al directorio de trabajo
COPY requirements.txt .

# Instalar las dependencias
RUN apt-get update && \
    pip install --upgrade pip setuptools && \
    apt-get install -qy build-essential ffmpeg && \
    pip install --no-cache-dir -r requirements.txt

COPY telegram-downloader/ .


# Ejecutar el bot
CMD ["python", "app.py"]

