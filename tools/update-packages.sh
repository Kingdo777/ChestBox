#!/bin/bash

ProjectRoot=$(dirname "$(dirname "$(realpath "$0")")")

pushd "$ProjectRoot/StateFunction/core" || exit
  cmake --build cmake-build-debug --target python-extend-statefunction
  cmake --build cmake-build-debug --target python-extend-ipc
popd || exit

pushd "$ProjectRoot/StateFunction/core/src/state-function-action/ipc-py-extend" || exit
  rm -rf build dist ipc.egg-info
  python3.10 setup.py build bdist_wheel
  cp dist/ipc-1.0.0-cp310-cp310-linux_x86_64.whl "$ProjectRoot/OpenWhisk/runtime-python/core/python310Action/"
  cp dist/ipc-1.0.0-cp310-cp310-linux_x86_64.whl "$ProjectRoot/Evaluation/0.SimpleTest/"
  "$ProjectRoot"/venv/bin/pip install --upgrade .
popd || exit

pushd "$ProjectRoot/StateFunction/core/src/state-function-library/statefunction-py-extend" || exit
  rm -rf build dist statefunction.egg-info
  python3.10 setup.py build bdist_wheel
  cp dist/statefunction-3.0.0-cp310-cp310-linux_x86_64.whl "$ProjectRoot/OpenWhisk/runtime-python/core/python310Action/"
  cp dist/statefunction-3.0.0-cp310-cp310-linux_x86_64.whl "$ProjectRoot/Evaluation/0.SimpleTest/"
  "$ProjectRoot"/venv/bin/pip install --upgrade .
popd || exit

pushd "$ProjectRoot/Evaluation/0.SimpleTest" || exit
  docker build -t simple-test .
  #docker run --rm --ipc=container:wsk0_kingdo_guest_StateFunction1 simple-test
popd || exit

pushd "$ProjectRoot/OpenWhisk/runtime-python" || exit
  ./gradlew :core:python310Action:distDocker -PdockerImagePrefix=kingdo -PdockerRegistry=docker.io
  #./gradlew :core:python27Action:distDocker -PdockerImagePrefix=kingdo -PdockerRegistry=docker.io
popd || exit

