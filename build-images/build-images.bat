set "SCRIPT_DIR=%~dp0"

docker build -t communicating-service:latest "%SCRIPT_DIR%\..\services\communicating-service"
docker build -t non-communicating-service:latest "%SCRIPT_DIR%\..\services\non-communicating-service"
docker build -t traffic-aggregation-server:latest "%SCRIPT_DIR%\..\services\traffic-aggregation-server"
