#!/usr/bin/env python3

import wave
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import json
import audioop
from io import BytesIO
import sys


class STT:
    def __init__(self, wav_file, url='http://127.0.0.1:8086'):
        self._text = None
        request = Request('{}/stt'.format(url), data=_get_wav(wav_file), headers={'Content-Type': 'audio/wav'})
        try:
            response = urlopen(request)
        except HTTPError as e:
            raise RuntimeError('Request failed: {}'.format(e.reason))
        except URLError as e:
            raise RuntimeError('Connection failed: {}'.format(e.reason))
        response_text = response.read().decode('utf-8')
        try:
            result = json.loads(response_text)
        except (json.JSONDecodeError, ValueError) as e:
            raise RuntimeError('Json decode error: {}'.format(e))

        if 'code' not in result or 'text' not in result or result['code']:
            raise RuntimeError('Server error: {}: {}'.format(result.get('code', 'None'), result.get('text', 'None')))
        self._text = result['text']

    def text(self):
        return self._text


def _get_wav(wav_file, convert_rate=16000, convert_width=2):
    channels = 1
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
    stt = STT(file, server)
    print('return: {}'.format(stt.text()))


if __name__ == '__main__':
    _main()
