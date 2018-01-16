#!/bin/bash

sem=$(head -1 .docker/.semester);

if [ -z "$1" ]; then
  docker run --rm \
    -v $(pwd)/.docker/.jupyter:/root/.jupyter \
    -v $(pwd):/notebooks \
    -p 19972:8888 \
    -p 19973:6006 \
    -p 19974:8000 \
    ucfsigai/meetings:$sem
else
  docker run --rm \
    --runetime=nvidia \
    -v $(pwd)/.docker/.jupyter:/root/.jupyter \
    -v $(pwd):/notebooks \
    -p 19972:8888 \
    -p 19973:6006 \
    -p 19974:8000 \
    ucfsigai/meetings:$sem
fi
