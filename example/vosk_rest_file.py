#!/usr/bin/env python3

import audioop
import json
import sys
import wave
from io import BytesIO
from urllib.request import Request, urlopen


def stt(wav_file: str, url: str) -> str:
    print('Connecting to \'{}\'...'.format(url))
    request = Request('{}/stt'.format(url), data=_load_wav(wav_file), headers={'Content-Type': 'audio/wav'})
    result = json.loads(urlopen(request).read().decode('utf-8'))

    if not ('code' in result and 'text' in result):
        raise RuntimeError('Wrong reply from server: {}'.format(result))
    return result['text'] if not result['code'] else 'Server error: [{code}]: {text}'.format(**result)


def _load_wav(wav_file, convert_rate=16000, convert_width=2, channels=1):
    with wave.open(wav_file, 'rb') as in_:
        src_rate = in_.getframerate()
        src_data = in_.readframes(in_.getnframes())
        dst_data, _ = audioop.ratecv(src_data, convert_width, channels, src_rate, convert_rate, None)
    with BytesIO() as file:
        with wave.open(file, 'wb') as out:
            out.setframerate(convert_rate)
            out.setsampwidth(convert_width)
            out.setnchannels(channels)
            out.writeframes(dst_data)
        result = file.getvalue()
    return result


def _main():
    if len(sys.argv) < 2:
        print('Usage: {} FILE [URL]'.format(sys.argv[0]))
        exit(1)
    file = sys.argv[1]
    server = 'http://127.0.0.1:8086' if len(sys.argv) < 3 else sys.argv[2]
    print('Result: {}'.format(stt(file, server)))


if __name__ == '__main__':
    _main()
