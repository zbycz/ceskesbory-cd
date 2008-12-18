@echo off

rem ***** get rid of all the old files in the build folder
rd /S /Q build
rd /S /Q dist

rem ***** create the exe
"c:\Program Files\Python25\python" setup.py py2exe

rem **** pause so we can see the exit codes
pause "done...hit a key to exit"