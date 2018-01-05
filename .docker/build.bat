@ECHO OFF

IF [%1] == []	(
	FOR /F %%i in ('head -1 '.version'') DO SET ver = %%i 
	FOR /F %%i in ('head -1 '.semester'') DO SET sem = %%i
	SET VERSION = !%ver%%sem%!
)
ELSE (
	SET VERSION = %1
)


docker rmi -f "ucfsigai/meetings:$version"

docker build \
  -t "ucfsigai/meetings:$((++version))" \
  .docker

IF NOT [%VERSION%] = [%1] (
  ECHO %version% > .docker/version
)