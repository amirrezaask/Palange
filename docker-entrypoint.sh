#!/usr/bin/env bash

python manage.py migrate --noinput
echo "there"
if [[ $? -ne 0 ]]; then
    echo "Migration failed." >&2
    exit 1
fi

# if arguments passed, execute them
# bring up an instance of project otherwise
if [[ $# -gt 0 ]]; then
    echo "run \"$@\""
    sh -c "$@"
else
    echo "runserver"
    python manage.py runserver
fi
