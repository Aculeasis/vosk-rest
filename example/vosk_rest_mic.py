import argparse
import json
from urllib.request import Request, urlopen

from speech_recognition import Microphone, Recognizer

SAMPLE_RATE = 16000
SERVER = 'http://127.0.0.1:8086'


class Color:
    red = 91
    green = 92
    blue = '1;36'
    gray = 90


def stt(data: bytes, url: str) -> str:
    request = Request('{}/stt'.format(url), data=data, headers={'Content-Type': 'audio/wav'})
    result = json.loads(urlopen(request).read().decode('utf-8'))

    if not ('code' in result and 'text' in result):
        raise RuntimeError('Wrong reply from server: {}'.format(result))
    return result['text'] if not result['code'] else 'Server error: [{code}]: {text}'.format(**result)


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('-S', type=str, default=SERVER, metavar='[URL]',
                        help='Server address (default: {})'.format(SERVER))
    parser.add_argument('-R', type=int, default=SAMPLE_RATE, metavar='[8000..192000]',
                        choices=(8000, 11025, 16000, 22050, 32000, 44100, 48000, 96000, 192000),
                        help='Sample rate (default: {})'.format(SAMPLE_RATE))
    parser.add_argument('-M', type=int, default=-1, metavar='[-1..100]',
                        choices=range(-1, 100), help='Microphone index (default: -1, auto)')
    parser.add_argument('-L', type=int, default=20, metavar='[0..3600]',
                        choices=range(0, 3600), help='Phrase time limit, 0 - unlimited, sec (default: 20)')
    return parser.parse_args()


def nn_print(msg: str, color, sp=True):
    print(' ' * 50, end='\r')  # fill
    print('[\033[{}m{}\033[0m]'.format(color, msg), end='\r' if sp else '', flush=True)


def pretty_size(size) -> str:
    ends = ['Bytes', 'KiB', 'MiB', 'GiB', 'TiB']
    max_index = len(ends) - 1
    index = 0
    while size >= 1024 and index < max_index:
        size /= 1024.0
        index += 1
    size = int(size) if size % 1 < 0.1 else round(size, 1)
    return '{} {}'.format(size, ends[index])


def listener(arg):
    r = None
    while True:
        if r is not None:
            nn_print('INIT', Color.gray)
        r = Recognizer()
        with Microphone(device_index=None if arg.M == -1 else arg.M, sample_rate=arg.R) as source:
            r.adjust_for_ambient_noise(source)
            nn_print('RECORD', Color.red)
            audio = r.listen(source, phrase_time_limit=arg.L if arg.L else None)

        nn_print('RECOGNITION', Color.blue, sp=False)
        data = audio.get_raw_data(SAMPLE_RATE, 2)
        print(' {}'.format(pretty_size(len(data))), end='\r', flush=True)
        text = stt(data, arg.S)
        nn_print('RESULT', Color.green, sp=False)
        print(' {}'.format(text))


if __name__ == '__main__':
    try:
        listener(cli())
    except Exception as e:
        print()
        raise
