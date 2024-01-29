@echo off
start /b python "webui.py"
start http://localhost:5000
powershell -NoExit -Command "Get-Content 'C:\tmp\lmstudio-server-log.txt' -Wait"