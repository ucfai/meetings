@echo off

rem Windows doesn't have support for nvidia-docker2 -- on Feb 22, 2018.
rem   b/c of this, Windows users can only run TensorFlow's cpu build
rem NOTE: Coordinators should be using some *nix-based system.


set /p version=<.semester
set container_name="ucfsigai_meeting"

docker run \
    -d \
    --name %@container_name% \
    -v "$(pwd)/.docker/.jupyter:/root/.jupyter" \
    -v "$(pwd):/notebooks" \
    -p 19972:8888 \
    -p 19973:6006 \
    --rm \
    "ucfsigai/%@version%-cpu"