#!/bin/bash

sem=$(head -1 .docker/.semester);

# if [ -z "$1" ]; then
#   ver=$(head -1 .docker/.version);
#   sem=$(head -1 .docker/.semester);
#   version="$sem-$ver"
# else
#   version=$1;
# fi

docker run --rm \
  -v $(pwd)/.docker/.jupyter:/root/.jupyter \
  -v $(pwd):/notebooks \
  -p 19972:8888 \
  -p 19973:6006 \
  -p 19974:8000 \
  ucfsigai/meetings:$sem
