[vosk-rest](https://github.com/Aculeasis/vosk-rest)
============
[![Docker Pulls](https://img.shields.io/docker/pulls/aculeasis/vosk-rest.svg)](https://hub.docker.com/r/aculeasis/vosk-rest/)

Простой веб-сервис распознавания речи с помощью [Vosk](https://github.com/alphacep/vosk-api) и [Kaldi](https://github.com/alphacep/kaldi)
через [vosk-api](https://github.com/alphacep/vosk-api).

## Установка

### Готовый докер
- aarch64 `docker run -d -p 8086:8086 aculeasis/vosk-rest:arm64v8`
- armv7l`docker run -d -p 8086:8086 aculeasis/vosk-rest:arm32v7`
- x86_64 `docker run -d -p 8086:8086 aculeasis/vosk-rest:amd64`

## API
Отправить файл через POST

    POST /stt
    Host: SERVER
    Content-Type: audio/x-wav
    (wav file)

Требования к файлу:
- Формат - wav
- Число каналов  - 1 (моно)
- Частота дискретизации  - 16 000 Гц
- Квантование - 16 бит.

Если нужно, перекодируйте файл перед отправкой.

Сервер пришлет ответ в json, где:
- `code` - код ошибки или 0
- `text` - распознанный текст если code равен 0 иначе сообщение об ошибке

## Работа с API
[examples](https://github.com/Aculeasis/vosk-rest/tree/master/example)

Для проверки сервера можно использовать `vosk_rest_file.py FILE [URL]`

## Ссылки
- [vosk-api](https://github.com/alphacep/vosk-api)
- [Vosk](https://github.com/alphacep/vosk)
- [Kaldi](https://github.com/alphacep/kaldi)
- [Модели](https://github.com/alphacep/kaldi-android-demo/releases)
