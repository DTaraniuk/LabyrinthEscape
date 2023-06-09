REM build.cmd
@echo off

REM create a virtual environment named "venv"
python -m venv venv

REM activate the virtual environment
call venv\Scripts\activate.bat

REM install packages from requirements.txt
pip install -r requirements.txt
