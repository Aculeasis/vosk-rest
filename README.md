[vosk-rest](https://github.com/Aculeasis/vosk-rest)
============
[![Docker Pulls](https://img.shields.io/docker/pulls/aculeasis/vosk-rest.svg)](https://hub.docker.com/r/aculeasis/vosk-rest/)

Простой локальный веб-сервис распознавания речи через [vosk-api](https://github.com/alphacep/vosk-api).

## Установка

### Готовый докер
- aarch64 `docker run -d --name vosk-rest -p 8086:8086 aculeasis/vosk-rest:arm64v8`
- armv7l`docker run -d --name vosk-rest -p 8086:8086 aculeasis/vosk-rest:arm32v7`
- x86_64 `docker run --name vosk-rest -d -p 8086:8086 aculeasis/vosk-rest:amd64`

### Сборка и запуск докера

Для поддержки другого языка измените имя модели в `MODEL_NAME` Dockerfile'a на нужную [отсюда](https://alphacephei.com/vosk/models) (без .zip).
 По умолчанию используется облегченная модель `vosk-model-small-ru-0.22`, для более качественного распознавания используйте `vosk-model-ru-0.10`.
```
git clone https://github.com/Aculeasis/vosk-rest
cd vosk-rest
# Указать Dockerfile под целевую архитектуру
docker build -t vosk-rest -f Dockerfile.arm64v8 .
docker run -d -p 8086:8086 vosk-rest
```

## API
Отправить файл через POST

    POST /stt
    Host: SERVER
    Content-Type: audio/x-wav
    (wav file)

| Требования к файлу ||
| --- | --- |
| Формат | wav |
| Число каналов | 1 (моно) |
| Частота дискретизации | 16 000 Гц |
| Квантование | 16 бит |

Если нужно, перекодируйте файл перед отправкой.

Сервер пришлет ответ в json, где:
- `code` - код ошибки или 0
- `text` - распознанный текст если code равен 0 иначе сообщение об ошибке

## Работа с API
[examples](https://github.com/Aculeasis/vosk-rest/tree/master/example)

Для проверки сервера можно использовать `vosk_rest_file.py FILE [URL]`
