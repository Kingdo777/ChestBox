#!/bin/bash

engine=$1
if [ -z "$engine" ]; then
  engine="redis"
fi

if [ "$engine" == "redis" ]; then
  echo "Using Redis"
else
  engine="memcached"
  echo "Using Memcached"
fi

pushd "$(dirname "$0")" >/dev/null 2>&1 || exit 1

# check "$engine.py" exists
if [ ! -f "$engine.py" ]; then
  echo "File $engine.py does not exist"
  exit 1
fi

# remove old zip
rm -rf packages lambda_function.zip
mkdir -p packages

# install dependencies
if [ "$engine" == "redis" ]; then
  pip3 install -t packages redis
else
  pip3 install -t packages pymemcache
fi

# zip packages
pushd packages >/dev/null 2>&1 || exit 1
zip -r9 ../lambda_function.zip .
popd >/dev/null 2>&1 || exit 1

# zip lambda function
cp "$engine.py" lambda_function.py
zip -g lambda_function.zip lambda_function.py
rm lambda_function.py

popd >/dev/null 2>&1 || exit 1
