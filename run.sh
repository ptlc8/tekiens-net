#!/bin/bash

run_install() {
    case $1 in
    back)
        cd back
        if [ ! -d venv ]; then
            python3 -m venv venv
        fi
        venv/bin/pip install -r requirements.txt
        cd ..
        ;;
    front)
        cd front
        npm install
        cd ..
        ;;
    "")
        run_install back
        run_install front
        ;;
    *)
        echo "Usage: $0 install"
        exit 1
        ;;
    esac
}

run_docker() {
  DOCKER_COMPOSE=$(type docker-compose > /dev/null 2> /dev/null && echo docker-compose || echo docker compose)
  case $1 in
    build)
      $DOCKER_COMPOSE build "${@:2}"
      ;;
    up)
      $DOCKER_COMPOSE up "${@:2}"
      ;;
    down)
      $DOCKER_COMPOSE down "${@:2}"
      ;;
    rm)
      $DOCKER_COMPOSE rm "${@:2}"
      ;;
    "")
      run_docker up --build
      ;;
    *)
      echo "Usage: $0 docker {build|up|down|rm|}"
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
    run_install "${@:2}"
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
