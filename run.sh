#!/bin/bash

case $1 in
build)
    cd src/front
    npm run build
    ;;
dev)
    cd src/front
    npm run dev
    ;;
start)
    cd src
    venv/bin/flask run
    ;;
install)
    cd src
    venv/bin/pip install -r requirements.txt
    cd front
    npm install
    ;;
"")
    cd src/front
    npm run build
    cd ..
    venv/bin/flask run
    ;;
*)
    echo "Usage: $0 {build|dev|start|install|}"
    exit 1
    ;;
esac