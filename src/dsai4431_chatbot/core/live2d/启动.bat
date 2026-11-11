@echo off
rem ===================================================================
rem  Live2D Demo launcher  (DSAI4431_Chatbot)
rem
rem  Keep this file ASCII-only: cmd.exe parses .bat with the system
rem  ANSI codepage, so Chinese text written inside would be garbled.
rem  Chinese paths are resolved by demo_interactive.py itself.
rem
rem  This file lives at: src\dsai4431_chatbot\core\live2d\
rem  The project root is four levels up.
rem ===================================================================
setlocal
chcp 65001 >nul

set "ROOT=%~dp0..\..\..\.."
cd /d "%ROOT%"

set "PY=%ROOT%\.venv\Scripts\python.exe"

if not exist "%PY%" goto :noenv

set "PYTHONPATH=%ROOT%\src;%PYTHONPATH%"

echo.
echo   Live2D Demo
echo   ---------------------------------------------
echo   Starting... (close the window to quit)
echo.

"%PY%" -m dsai4431_chatbot.core.live2d.demo_interactive %*
set "RC=%ERRORLEVEL%"

if not "%RC%"=="0" goto :failed
goto :done


:noenv
echo.
echo   [x] Virtual environment not found:
echo       %PY%
echo.
echo   Create it once in the project root:
echo       python -m venv .venv
echo       .venv\Scripts\python.exe -m pip install PyQt5 PyQtWebEngine
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
