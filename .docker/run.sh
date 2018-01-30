#!/bin/bash

sem=$(head -1 .docker/.semester);

ARGS=""

## We default to CPU because the majority of laptops don't have a discrete GPU
## and TensorFlow 1.4.1, GPU edition, doesn't support running without a GPU.
case "$1" in
    "cpu" | "")
        tags="meetings:$sem-cpu"
        ARGS="$ARGS -v $(pwd):/notebooks -v $(pwd)/.docker/.jupyter:/root/.jupyter"
        ARGS="$ARGS -p 19972:8888 -p 19973:6006 -p 19974:8000"
        ;;
    "gpu")
        tags="meetings:$sem-gpu"
        ARGS="$ARGS --runtime=nvidia"
        ARGS="$ARGS -v $(pwd):/notebooks -v $(pwd)/.docker/.jupyter:/root/.jupyter"
        ARGS="$ARGS -p 19972:8888 -p 19973:6006 -p 19974:8000"
        ;;
    "sass")
        tags="meetings-sass-monitor:$sem"
        ;;
    *)
        echo "You specified an un-acceptable parameter: '$1'. Please try again."
        ;;
esac

## Launching the container
printf "\n\n------ Launching: 'ucfsigai/$tags' -----\n"
printf "  - If this is wrong, send 'Ctrl-C' to stop the container.\n\n"
docker run $ARGS --rm "ucfsigai/$tags"