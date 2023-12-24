#!/bin/bash

# Run `git clone https://github.com/Kingdo777/ChestBox.git` for getting the project.
ProjectRoot=$(dirname "$(dirname "$(dirname "$(realpath "$0")")")")

sh -c "$ProjectRoot/tools/update-packages.sh"

docker run --rm --ipc=container:wsk0_kingdo_guest_StateFunction1 simple-test