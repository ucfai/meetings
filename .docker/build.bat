@echo off

rem Windows doesn't have support for nvidia-docker2 -- on Feb 22, 2018.
rem   b/c of this, Windows users can only run TensorFlow's cpu build
rem NOTE: Coordinators should be using some *nix-based system.

set /p version=<.semester
set file="cpu"

docker rmi -f "ucfsigai/%@version%-cpu"

docker build \
    -t "ucfsigai/%@version%-cpu" \
    -f ".docker/%@file%.Dockerfile" \
    .docker