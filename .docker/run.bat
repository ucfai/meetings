@ECHO OFF

IF [%1] == []	(
	FOR /F %%i in ('head -1 '.version'') DO SET ver = %%i 
	FOR /F %%i in ('head -1 '.semester'') DO SET sem = %%i
	SET version = !%ver%%sem!
)
ELSE (
	SET version = %1
)

REM Gotta figure out the equivalent batch conditional expresesions. for -v and -p
docker run \
  -v $(pwd)/.docker/.jupyter:/root/.jupyter \
  -v $(pwd):/notebooks \
  -p 19972:8888 \
  -p 19973:6006 \
  -p 19974:8000 \
  ucfsigai/meetings:$version