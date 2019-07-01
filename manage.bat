@echo off
set "PYTHON=%~dp0venv\Scripts\python.exe"

set cmd=%1
rem алиасы для комманд
IF /I "%cmd%" EQU "m" set cmd=migrate
IF /I "%cmd%" EQU "mm" set cmd=makemigrations


%PYTHON% %~dp0backend\manage.py %cmd% %2 %3 %4 %5 %6 %7 %8 %9
