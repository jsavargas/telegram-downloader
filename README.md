# telegram downloader 
**telegram downloader is a program to download files from channels that prevent the forwarding of messages to a bot, allowing the download of files using the personal account via the web UI and command line**

## docker-compose
```
version: "3.9"
services:
  telegram-downloader:
    image: jsavargas/telegram-downloader:alfa
    container_name: telegram-download
    environment:
      - PUID=99
      - PGID=100
      - OWNER=@jsavargas  # Your Nickname Telegram
      - APP_ID=131 
      - API_HASH=3efad
      - BOT_TOKEN=3945:Pd09m-p9
      - TZ=America/Santiago
    volumes:
      - ./config:/config
      - /mnt/user/download/torrent/telegram/bot:/download
      - /mnt/user/media/media/series:/series
    ports:
      - 5555:5000
```

## Use

### Configs (Envs)
- `BOT_TOKEN` - Get it by contacting to [BotFather](https://t.me/botfather)
- `APP_ID` - Get it by creating app on [my.telegram.org](https://my.telegram.org/apps)
- `API_HASH` - Get it by creating app on [my.telegram.org](https://my.telegram.org/apps)

- `OWNER` - Your nickname telegram
- `TZ`- America/Santiago

### Use docker-compose
```sh 
docker-compose up -d

http://IP:5555
```

### Use 
```bash
docker exec -it telegram-downloader sh

Create Credenciales
docker exec -it telegram-download python create_config.py 


docker exec -it telegram-download python telegram.cli.py -g traicionada_mega 
docker exec -it telegram-download python telegram.cli.py -g traicionada_mega -d

```

### UI
![](img/001.png)

### Config
![](img/002.png)