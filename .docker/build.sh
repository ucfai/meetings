#!/bin/bash

sem=$(head -1 .docker/.semester);

case "$1" in
    "cpu" | "")
        tags="meetings:$sem-cpu"
        file="cpu"
        ;;
    "gpu")
        tags="meetings:$sem-gpu"
        file="gpu"
        ;;
    "sass")
        tags="meetings-sass-monitor:$sem"
        file="sass"
        ;;
    *)
        printf "You specified an un-acceptable parameter: '$1'. Please try again."
        exit 1
        ;;
esac

## Removing the old image
printf "\n\n------ Removing: 'ucfsigai/$tags' -----\n"
docker rmi   -f "ucfsigai/$tags"

## Building the new image
printf "\n\n------ Building: 'ucfsigai/$tags' -----\n"
printf "  - If this is wrong, send 'Ctrl-C' to stop building the container.\n\n"

## Actually build the container now. Have some hard-coding to reduce margin for
## error in the case statement above.
docker build -t "ucfsigai/$tags" -f ".docker/$file.Dockerfile" .docker