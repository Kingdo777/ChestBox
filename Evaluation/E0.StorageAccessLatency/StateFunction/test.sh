#!/bin/bash

# python binary
py="$(dirname "$(dirname "$(dirname "$(dirname "$(readlink -f "$0")")")")")/venv/bin/python3"
# script
test_script="$(dirname "$(readlink -f "$0")")/main.py"
integrate_script="$(dirname "$(readlink -f "$0")")/integrate.py"
# result directory
result_dir="$(dirname "$(readlink -f "$0")")/results"

# start state-function container
docker stop state-function
docker run -d --rm --name state-function kingdo/state-function

loop=100
for size in "1KB" "4KB" "1MB" "10MB" "100MB"; do
  for _ in $(seq 1 $loop); do
    sudo STATE_FUNCTION_LOG_LEVEL="off" "$py" "$test_script" "$size" # run script with logging
    sleep 1
  done
done

"$py" "$integrate_script"

rm -rf "${result_dir:?}"/get_*
rm -rf "${result_dir:?}"/set_*
