#!/bin/bash

if [ -z "$1" ]; then
  ver=$(head -1 .docker/.version);
  sem=$(head -1 .docker/.semester);
  version="$ver-$sem"
else
  version=$1;
fi

docker rmi -f "ucfsigai/meetings:$version"

docker build \
  -t "ucfsigai/meetings:$((++version))" \
  .docker

if [ $version != $1 ]; then
  echo $version > .docker/version
fi
