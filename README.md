# telegram downloader 
**telegram downloader is a program to download files from channels that prevent the forwarding of messages to a bot, allowing the download of files using the personal account via the web UI and command line**




## Use


### Configs (Envs)
- `BOT_TOKEN` - Get it by contacting to [BotFather](https://t.me/botfather)
- `APP_ID` - Get it by creating app on [my.telegram.org](https://my.telegram.org/apps)
- `API_HASH` - Get it by creating app on [my.telegram.org](https://my.telegram.org/apps)

- `OWNER` - Your nickname telegram
- `TZ`- America/Santiago

### Use 
```sh 


docker exec -it telegram-download python create_config.py 


docker exec -it telegram-download python telegram.cron.py -g traicionada_mega 
docker exec -it telegram-download python telegram.cron.py -g traicionada_mega -d


```
