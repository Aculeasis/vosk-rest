#!/bin/bash

echo "Setting trap PID $$"
trap cleanup INT TERM

cleanup() {
    echo 'stopping...'
    APP="$(pgrep 'python' -a | grep 'app.py' | awk '{print $1}')"
    kill -TERM "$APP"
    wait
    echo "stop"
    exit 0
}

if [ -f /opt/app.py ]; then
    python3 /opt/app.py &
fi

wait
exit 1