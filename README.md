# Telegram Downloader bot

Telegram bot developed using the Pyrogram library that allows the download of forwarded files.


```yml

version: '3.8'

services:
  telegram-downloader-bot:
    image: jsavargas/telegram-downloader-bot:develop
    container_name: telegram-downloader-bot
    restart: unless-stopped
    environment:
      - API_ID=${API_ID}
      - API_HASH=${API_HASH}
      - BOT_TOKEN=${BOT_TOKEN}
      - AUTHORIZED_USER_ID=${AUTHORIZED_USER_ID}
      - TZ=America/Santiago
    volumes:
      - /path/config:/config
      - /path/download:/download
      - /path/torrent/watch:/watch
    tty: true



```
