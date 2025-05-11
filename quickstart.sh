#!/usr/bin/env bash

python3 -m venv ./.venv
./.venv/bin/pip install -r requirements.txt

PYTHON_LOCATION="$(pwd)/.venv/bin/python"
INI_FILE="[python]\nCOMMAND = $PYTHON_LOCATION\n"
echo -e "$INI_FILE" > ./controllers/apriltag_controller/runtime.ini
echo -e "$INI_FILE" > ./controllers/drone_controller/runtime.ini