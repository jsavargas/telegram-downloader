# Telegram Downloader bot

Telegram bot developed using the Pyrogram library that allows the download of forwarded files.



## Telegram Downloader bot

[GITHUB](https://github.com/jsavargas/telethon_downloader)

[DOCKERHUB](https://hub.docker.com/r/jsavargas/telegram-downloader)

## Telethon Downloader

[telethon_downloader Github](https://github.com/jsavargas/telethon_downloader)

[telethon_downloader Dockerhub](https://hub.docker.com/r/jsavargas/telethon_downloader)



# Telegram Bot with Automatic Download

This Telegram Bot, built with the Pyrogram client, is designed to automatically download documents, videos, photos, audios, and much more. With significantly faster speeds than its predecessor made with Telethon, this bot ensures quick and efficient downloads of all types of files sent to it. Additionally, it now offers the capability to download videos and audios from YouTube, as well as direct links to files via their URL.


### What's new in this version:

Here is a list of new features included in this Telegram bot built with Pyrogram:

- **Extended Functionality:**
  - Automatically downloads documents, videos, photos, audios, and other multimedia files sent to the bot.
  - Capable of downloading videos and audios from YouTube.
  - Supports downloading files from direct URLs.
  - Significantly faster download speeds compared to the previous version made with Telethon.
  - Flexible settings for customizing download paths and other preferences.
  - Flexible settings for customizing download paths and other preferences.
  - Downloads into folders by extension.
  - Downloads into folders by group.
  - Downloads into folders by keywords.
  - Renames files using message text by group.


- **New Features Coming Soon:**

  - Unzipping files.
  - Removal of special characters in file names.
  - Grouping files into folders with a command.
  - Renaming files with a command.
  - Deleting files from messages once downloaded (by group).
  - Moving all old messages from a group to a new folder.
  - Enhanced download messages.
  - Enable download progress.
  - Agregar *AUTHORIZED_USER_ID* por comandos al archivo *config.ini*.


Enjoy an automated and organized downloading experience with telethon_downloader!

![](https://raw.githubusercontent.com/jsavargas/telegram-downloader-bot/main/images/telegram-downloader.gif)



![](https://raw.githubusercontent.com/jsavargas/telethon_downloader/master/images/download-youtube.png)

## Environment:

 Pull or build the docker image and launch it with the following environment variables:


 **API_ID** : <telegram API key generated at ´Generating Telegram API keys´>

 **API_HASH** : <telegram API hash generated at ´Generating Telegram API keys´>

 **BOT_TOKEN** : <telegram BOT token generated at ´Creating a Telegram Bot´>

 **AUTHORIZED_USER_ID** : <telegram ´chat_id´ authorized> 
>NOTE: Unique identification of the user(s) who have permission to send files to the bot. If there are multiple authorized users, separate their IDs with commas

 **TZ** [OPTIONAL]: <Sets the system timezone, adjusting it based on the geographical location of the server or user.
>Example: America/Santiago

 **MAX_CONCURRENT_TASKS** [OPTIONAL] **:** <maximum number of parallel downloads allowed (default: 3, maximum 4)> 
>NOTE: Allows you to define the maximum number of simultaneous downloads



## Volumes:

- **/config:** Path where configuration files are stored, along with files *pending download* and *recent downloads*.

- **/download:** Folder designated for file downloads. *All* files sent to the bot will be saved in this location.

- **/watch:** Folder used for storing torrent files that will be managed by the *transmission/qbittorrent* system. Files in this folder will be automatically uploaded and handled by the torrent client.



## DOCKER-COMPOSE

```yml

version: '3.8'

services:
  telegram-downloader:
    image: jsavargas/telegram-downloader
    container_name: telegram-downloader
    restart: unless-stopped
    environment:
      - API_ID=${API_ID}
      - API_HASH=${API_HASH}
      - BOT_TOKEN=${BOT_TOKEN}
      - AUTHORIZED_USER_ID=${AUTHORIZED_USER_ID}
      - TZ=America/Santiago
      - MAX_CONCURRENT_TASKS=${MAX_CONCURRENT_TASKS} or TG_MAX_PARALLEL=${TG_MAX_PARALLEL}
      - PUID=${PUID}
      - PGID=${PGID}
    volumes:
      - /path/config:/config
      - /path/download:/download
      - /path/torrent/watch:/watch

```


# Changelog

## Backlog (Upcoming Features)
- **Feature:** Re-downloading of files (in development).
- **Feature:** Adding a feature to download videos and audio from YouTube.
- **Feature:** Adding a command to manage downloads by file extensions.
- **Feature:** Adding permission management to environment variables.
- **Feature:** Adding a feature to decompress ZIP, RAR, and TAR files.
- **Feature:** Added environment variable for YouTube video and audio download path.


## [Version 1.0.0] - 2024-08-17
- **Update:** Updated change_permissions files
