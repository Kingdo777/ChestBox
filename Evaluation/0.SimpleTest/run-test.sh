#!/bin/bash

cp ../../../StateFunction/core/src/state-function-library/statefunction-py-extend/dist/statefunction-3.0.0-cp310-cp310-linux_x86_64.whl ./

docker build -t simple-test .

docker run --rm --ipc=container:wsk0_kingdo_guest_StateFunction1 simple-test