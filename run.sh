#!/bin/bash

run_docker() {
    case $1 in
    build)
        docker build -t tekiens-net . "${@:2}"
        ;;
    up)
        docker-compose up "${@:2}"
        ;;
    down)
        docker-compose down "${@:2}"
        ;;
    "")
        run_docker build
        run_docker up
        ;;
    *)
        echo "Usage: $0 docker {build|up|down|}"
        exit 1
        ;;
    esac
}

case $1 in
build)
    cd front
    npm run build
    ;;
dev)
    cd front
    npm run dev
    ;;
run|start)
    cd back
    venv/bin/flask run
    ;;
install)
    cd back
    venv/bin/pip install -r requirements.txt
    cd ../front
    npm install
    ;;
docker)
    run_docker "${@:2}"
    ;;
"")
    $0 build
    $0 run
    ;;
*)
    echo "Usage: $0 {build|dev|start|install|docker|}"
    exit 1
    ;;
esac