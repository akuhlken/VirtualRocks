@echo off
setlocal enabledelayedexpansion

:: Define Python version and installation directory
set "PYTHON_VERSION=3.12.0"
set "INSTALL_DIR=C:\Python\%PYTHON_VERSION%"

:: URL to Python installer
set "PYTHON_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/python-%PYTHON_VERSION%-amd64.exe"

:: Create installation directory if it doesn't exist
if not exist "%INSTALL_DIR%" (
    mkdir "%INSTALL_DIR%"
)

:: Download Python installer
echo Downloading Python %PYTHON_VERSION%...
bitsadmin.exe /transfer "PythonInstaller" "%PYTHON_URL%" "%INSTALL_DIR%\python-%PYTHON_VERSION%-amd64.exe"

:: Install Python silently
echo Installing Python %PYTHON_VERSION%...
"%INSTALL_DIR%\python-%PYTHON_VERSION%-amd64.exe" /quiet InstallAllUsers=1 PrependPath=1

:: Check if Python installation was successful
if exist "%INSTALL_DIR%\python.exe" (
    echo Python %PYTHON_VERSION% has been successfully installed.
) else (
    echo Failed to install Python. Please check the installation log for details.
)

endlocal
