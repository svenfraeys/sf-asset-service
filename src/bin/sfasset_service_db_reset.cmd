@echo off
setlocal EnableDelayedExpansion
set SF_ROOT=%~dp0%
python %SF_ROOT%/sfasset_service_db_reset.py %*
exit /B 0
