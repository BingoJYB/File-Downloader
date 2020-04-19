@echo off 

cmd /k "cd %~dp0\venv\Scripts & activate & cd ..\.. & python app.py install & python app.py start & sc config FileDownloader start= auto"