@echo off
cd /d "%~dp0"
echo Building Docker image without cache to avoid snapshot errors...
docker build --no-cache -t customer-analytics .

echo Setting Docker Hub username...
set DOCKER_USER=

echo Tagging image...
docker tag customer-analytics %DOCKER_USER%/customer-analytics:latest

echo Pushing image to Docker Hub...
docker push %DOCKER_USER%/customer-analytics:latest

echo Done! Image pushed to %DOCKER_USER%/customer-analytics:latest
pause
