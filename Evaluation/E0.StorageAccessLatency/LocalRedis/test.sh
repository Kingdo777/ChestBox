#!/bin/bash

# python binary
py="$(dirname "$(dirname "$(dirname "$(dirname "$(readlink -f "$0")")")")")/venv/bin/python3"
# script
test_script="$(dirname "$(readlink -f "$0")")/main.py"
integrate_script="$(dirname "$(readlink -f "$0")")/integrate.py"
# result directory
result_dir="$(dirname "$(readlink -f "$0")")/results"

# start redis-server container
docker stop redis-server
docker run -d --rm --name redis-server -p 6379:6379 redis

loop=100
for size in "1KB" "4KB" "1MB" "10MB" "100MB"; do
  for _ in $(seq 1 $loop); do
    sudo STATE_FUNCTION_LOG_LEVEL="off" "$py" "$test_script" "$size" "set" # run script with logging
    sudo STATE_FUNCTION_LOG_LEVEL="off" "$py" "$test_script" "$size" "get" # run script with logging
  done
done

"$py" "$integrate_script"

rm -rf "${result_dir:?}"/get_*
rm -rf "${result_dir:?}"/set_*
