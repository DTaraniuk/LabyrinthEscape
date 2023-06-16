REM client.cmd
@echo off

REM go up to the project root directory
cd ..

REM activate the virtual environment
call venv\Scripts\activate.bat

REM run client.py
python networking\client.py
