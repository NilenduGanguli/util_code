@echo off
REM Set environment variables

SET MY_VARIABLE1=Value1
SET MY_VARIABLE2=Value2
SET PATH=C:\MyFolder;%PATH%

REM Display the environment variables
echo MY_VARIABLE1=%MY_VARIABLE1%
echo MY_VARIABLE2=%MY_VARIABLE2%
echo PATH=%PATH%

REM Pause to keep the command prompt open
pause
