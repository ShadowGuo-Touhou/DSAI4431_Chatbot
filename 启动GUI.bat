@echo off
rem ===================================================================
rem  DSAI4431 Chatbot - launch the main GUI with the project venv
rem
rem  Keep this file ASCII-only: cmd.exe parses .bat with the system
rem  ANSI codepage, so Chinese text written inside would be garbled.
rem
rem  This file lives in the project root, next to pyproject.toml and .venv.
rem ===================================================================
setlocal
chcp 65001 >nul

cd /d "%~dp0"

set "PY=%~dp0.venv\Scripts\python.exe"

if not exist "%PY%" goto :noenv

rem Put local sources ahead of any installed copy, so edits take effect
rem without reinstalling.
set "PYTHONPATH=%~dp0src;%PYTHONPATH%"

echo.
echo   DSAI4431 Chatbot  -  main interface
echo   ---------------------------------------------
echo.

"%PY%" -m dsai4431_chatbot.core.gui %*
set "RC=%ERRORLEVEL%"

if not "%RC%"=="0" goto :failed
goto :done


:noenv
echo.
echo   [x] Virtual environment not found:
echo       %PY%
echo.
echo   Create it once in this folder:
echo       python -m venv .venv
echo       .venv\Scripts\python.exe -m pip install -e ".[gui]"
echo.
pause
exit /b 1


:failed
echo.
echo   [x] Exited with code %RC%
echo.
pause
exit /b %RC%


:done
endlocal
exit /b 0
