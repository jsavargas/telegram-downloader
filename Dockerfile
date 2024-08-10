# Usar una imagen base de Python
FROM python:slim


# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar los archivos requirements.txt y bot.py al directorio de trabajo
COPY requirements.txt .

# Instalar las dependencias
RUN apt-get update && \
    pip install --upgrade pip setuptools && \
    apt-get install -qy python3-dev libffi-dev build-essential ffmpeg && \
    #apt-get install -qy ffmpeg && \
    pip install --no-cache-dir -r requirements.txt

COPY telegram-downloader-bot/ .


# Ejecutar el bot
CMD ["python", "telegramBot.py"]

