#!/bin/bash

# Run `git clone https://github.com/Kingdo777/ChestBox.git` for getting the project.
ProjectRoot=$(dirname "$(dirname "$(dirname "$(realpath "$0")")")")

#sh -c "$ProjectRoot/tools/update-packages.sh"
docker build -t simple-test "$ProjectRoot"/Evaluation/0.SimpleTest

docker run --rm -v ./result:/app/result --ipc=container:wsk0_kingdo_guest_StateFunction1 simple-test

docker run --rm -v ./result:/app/result --ipc=container:wsk0_kingdo_guest_StateFunction2 simple-test python3 main.py True

sudo chmod -R 777 ./result