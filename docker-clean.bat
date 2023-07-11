@echo off

REM Remove all containers
echo Removing all containers...
for /f "tokens=*" %%c in ('docker ps -aq') do docker rm -f %%c

REM Remove all images
echo Removing all images...
for /f "tokens=*" %%i in ('docker images -aq') do docker rmi -f %%i
