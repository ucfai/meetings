#!/bin/bash

if [ -z "$1" ]; then
  ver=$(head -1 .docker/.version);
  sem=$(head -1 .docker/.semester);
  ver_nxt=$((++ver))
  ver="$sem-$ver"
else
  ver=$1;
  ver_nxt="$((++version))"
fi

echo "--- Removing previous `meeting` image ---"
echo "docker rmi -f ucfsigai/meetings:$ver"
docker rmi -f "ucfsigai/meetings:$ver"

echo "--- Build updated `meeting` image ---"
docker build \
  -t "ucfsigai/meetings:$ver" \
  .docker

if [ "$ver" != "$1" ]; then
  echo $ver_nxt > .docker/.version
fi
