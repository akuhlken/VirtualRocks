@echo off
echo Checking for NVIDIA drivers...

REM Run the command to check for NVIDIA devices
wmic path win32_videocontroller where "name like '%%NVIDIA%%'" get name 2>NUL | findstr /i /c:"NVIDIA" > nul

REM Check the errorlevel to determine if NVIDIA drivers were found
if %errorlevel% equ 0 (
    echo NVIDIA drivers are installed on this system.
    REM Check CUDA version
    echo Checking for CUDA...
    nvcc --version 2>NUL | findstr /i /c:"Cuda compilation tools" > nul
    if %errorlevel% equ 0 (
        echo CUDA is installed on this system.
        echo Waiting for 5 seconds...
        timeout /t 5 /nobreak > nul

        echo Continuing after waiting.
        EXIT /B
    ) else (
        echo CUDA is not installed. Installing CUDA
        echo Waiting for 5 seconds...
        timeout /t 5 /nobreak > nul

        echo Continuing after waiting.
        do pip install cuda-pyton )

) else (
    echo NVIDIA drivers are not installed on this system.
    echo Waiting for 5 seconds...
    timeout /t 5 /nobreak > nul

    echo Continuing after waiting.
    EXIT /B
)
