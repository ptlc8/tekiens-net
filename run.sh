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
"")
    cd src/front
    npm run build
    cd ..
    venv/bin/flask run
    ;;
*)
    echo "Usage: $0 {build|dev|start|}"
    exit 1
    ;;
esac