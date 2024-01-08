#!/bin/bash

HOME_DIR="/home/kingdo"
CURDIR=$(dirname "$0")
FAASTLANE_PROJECT_HOME="${HOME_DIR}/PycharmProjects/faastlane"
FAASTLANE_WORK_DIR="${CURDIR}/.faastlane"

FAASTLANE_WORK_DIR="${FAASTLANE_WORK_DIR}" python3 "${FAASTLANE_PROJECT_HOME}/composer/generator.py" --input . --platform ow

