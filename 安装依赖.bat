@echo off
rem ===================================================================
rem  DSAI4431 Chatbot  -  install Python dependencies into .venv
rem
rem  ASCII only on purpose: cmd.exe parses .bat with the system ANSI
rem  codepage (same note as in the GUI launcher bat), so Chinese text written
rem  inside would come out garbled.
rem
rem  Usage:
rem      double-click this file         (uses the default PyPI index)
rem      .\install.bat --mirror        (uses the Tsinghua mirror)
rem
rem  What it does:
rem      1. finds a Python 3.12+
rem      2. creates .venv (or reuses an existing one)
rem      3. upgrades pip
rem      4. pip install -e ".[gui,rag]"
rem
rem  The GUI extras pull PySide6 (~200 MB) and sherpa-onnx, so the
rem  last step is the slow one. Models for RAG / speech are NOT
rem  installed here - the launcher downloads them on first run.
rem ===================================================================
setlocal
chcp 65001 >nul
cd /d "%~dp0"

set "PIP_ARGS="
if /i "%~1"=="--mirror" (
    rem also export it: the pip upgrade step needs the mirror too,
    rem otherwise it hangs on the default PyPI index
    set "PIP_ARGS=-i https://pypi.tuna.tsinghua.edu.cn/simple"
    set "PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple"
)

echo.
echo   DSAI4431 Chatbot  -  install dependencies
echo   -----------------------------------------
echo.

rem --- 1) locate Python 3.12+ ---------------------------------------
set "PY="
py -3.12 -c "import sys" >nul 2>nul && set "PY=py -3.12"
if not defined PY (
    python -c "import sys; assert sys.version_info >= (3, 12)" >nul 2>nul && set "PY=python"
)
if not defined PY goto :nopython
echo   [1/4] Python: %PY%

rem --- 2) virtual environment ---------------------------------------
if exist ".venv\Scripts\python.exe" (
    echo   [2/4] .venv already exists, reusing it
) else (
    echo   [2/4] creating .venv ...
    %PY% -m venv .venv
    if errorlevel 1 goto :failed
)

rem --- 3) pip (failure here is not fatal: the bundled one usually works) ---
echo   [3/4] upgrading pip ...
".venv\Scripts\python.exe" -m pip install --upgrade pip -q %PIP_ARGS%
if errorlevel 1 echo         (pip upgrade failed - continuing with the bundled pip)

rem --- 4) project + extras -------------------------------------------
echo   [4/4] installing .[gui,rag]   (PySide6 is ~200 MB, this takes a while)
if defined PIP_ARGS echo         mirror: %PIP_ARGS%
".venv\Scripts\python.exe" -m pip install -e ".[gui,rag]" %PIP_ARGS%
if errorlevel 1 goto :failed

echo.
echo   Done.  Next step: run the GUI launcher bat.
echo   Its first launch downloads Ollama and the models by itself
echo   (about 2 GB) - the loading page shows each step.
echo.
if not defined CI pause
exit /b 0


:nopython
echo.
echo   [x] Python 3.12+ not found.
echo       Install it from https://www.python.org/downloads/ and make
echo       sure "py" or "python" works in a terminal window.
echo.
if not defined CI pause
exit /b 1


:failed
echo.
echo   [x] Installation failed - see the messages above.
echo       If pip timed out on a slow network, retry with:
echo           %~nx0 --mirror
echo.
if not defined CI pause
exit /b 1
