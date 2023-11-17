#!/bin/bash

cd src/front
npm run build
cd ..
venv/bin/flask run
