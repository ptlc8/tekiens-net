#!/bin/bash

case $1 in
build)
    cd front
    npm run build
    ;;
dev)
    cd front
    npm run dev
    ;;
start)
    cd back
    venv/bin/flask run
    ;;
install)
    cd back
    venv/bin/pip install -r requirements.txt
    cd ../front
    npm install
    ;;
"")
    cd front
    npm run build
    cd ../back
    venv/bin/flask run
    ;;
*)
    echo "Usage: $0 {build|dev|start|install|}"
    exit 1
    ;;
esac