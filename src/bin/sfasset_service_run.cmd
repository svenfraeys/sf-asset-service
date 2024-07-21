@echo off
setlocal EnableDelayedExpansion
set SF_ROOT=%~dp0%
uvicorn sfasset_service:app %*
exit /B 0
