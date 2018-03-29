#!/bin/bash

container_name="ucfsigai_meeting"

sem=$(head -1 .docker/semester);

ARGS=""

## We default to CPU because the majority of laptops don't have a discrete GPU
## and TensorFlow 1.4.1, GPU edition, doesn't support running without a GPU.
case "$1" in
    "cpu" | "")
        tags="meetings:$sem-cpu"
        ;;
    "gpu")
        tags="meetings:$sem-gpu"
        ARGS="$ARGS --runtime=nvidia"
        ;;
    "sass")
        container_name="ucfsigai_sassy"
        tags="meetings-sass-monitor:$sem"
        ;;
    *)
        echo "You specified an un-acceptable parameter: '$1'. Please try again."
        ;;
esac

if [ "$(docker ps -q -f status=running -f name=${container_name})" ]; then
    docker stop ${container_name}
fi

ARGS="$ARGS -v $(pwd)/data:/data"
ARGS="$ARGS -v $(pwd):/notebooks"
ARGS="$ARGS -p 19972:8888 -p 19973:6006"

## Launching the container
printf "\n"
printf "_____________ Launching: 'ucfsigai/$tags' _____________\n"
printf "  - This container is running in detached mode. To stop it, type...\n"
printf "    \`docker stop ucfsigai_meeting\`\n"
printf "\n"
docker run \
    -d \
    --name ${container_name} \
    -v "$(pwd)/.docker/.jupyter:/root/.jupyter" \
    $ARGS \
    --rm \
    "ucfsigai/$tags"
