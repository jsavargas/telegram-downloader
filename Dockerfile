FROM python

WORKDIR /app

COPY requirements.txt requirements.txt

#RUN apt-get update && \
#    pip install --upgrade pip setuptools && \
#    apt-get install -qy build-essential ffmpeg && \
#    pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get -qy dist-upgrade && \
    apt-get install -qy --no-install-recommends \
    ffmpeg \
    unzip && \
    rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --no-cache-dir --upgrade pip && \
    pip install -r requirements.txt



COPY telegram-downloader/ .


# Ejecutar el bot
CMD ["python", "app.py"]

