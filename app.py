#!/usr/bin/env python3

import json
import os
from io import BytesIO

from flask import Flask, request, json
from vosk import Model, KaldiRecognizer

MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'model')
if not os.path.exists(MODEL_PATH):
    print('Model folder not found ({}), bye.'.format(MODEL_PATH))
    exit(1)
kaldi_model = Model(MODEL_PATH)


def stt(fp,  buffer_size=8192) -> str:
    kaldi = KaldiRecognizer(kaldi_model, 16000)
    fp.read(44)  # skip header
    buf = bytearray(buffer_size)
    im_ok = False
    while fp.readinto(buf):
        kaldi.AcceptWaveform(buf)
        im_ok = True
    return json.loads(kaldi.FinalResult())['text'] if im_ok else ''


app = Flask(__name__, static_url_path='')


@app.route('/stt', methods=['GET', 'POST'])
def say():
    if request.method == 'POST':
        target = None
        if request.headers.get('Transfer-Encoding') == 'chunked':
            target = request.stream
        elif request.data:
            target = BytesIO(request.data)

        if target is None:
            text = 'No data'
            code = 1
        else:
            try:
                text = stt(target)
            except Exception as e:
                text = 'Internal error'
                code = 3
                print('{}: {}'.format(text, e))
            else:
                code = 0
    else:
        text = 'What do you want? I accept only POST!'
        code = 2
    return json.jsonify({'text': text, 'code': code})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8086, threaded=False)
