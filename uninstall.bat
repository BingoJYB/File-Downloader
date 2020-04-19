@echo off 

cmd /k "cd %~dp0\venv\Scripts & activate & cd ..\.. & python app.py stop & python app.py remove"