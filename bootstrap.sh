#!/bin/bash

VIRTUALENV_URL=https://raw.github.com/pypa/virtualenv/master/virtualenv.py
create_virtualenv() {
    VIRTUALENV=$(type -p virtualenv)
    if [ ! -n "$VIRTUALENV" ]; then
        echo "Getting virtualenv from $VIRTUALENV_URL..."
        curl $VIRTUALENV_URL 2>/dev/null > /tmp/virtualenv.py
        VIRTUALENV="python /tmp/virtualenv.py"
    fi
    $VIRTUALENV .env
    source .env/bin/activate
    pip install -r requirements.txt
}

if [ ! -d .env ]; then
    create_virtualenv
fi

source .env/bin/activate
python manage.py syncdb
