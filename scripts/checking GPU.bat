@echo off
echo Checking for NVIDIA drivers...

REM Run the command to check for NVIDIA devices
wmic path win32_pnpentity where "Caption like 'NVIDIA%'" get Caption 2>NUL | findstr /i /c:"NVIDIA" > nul

REM Check the errorlevel to determine if NVIDIA drivers were found
if %errorlevel% equ 0 (
    echo NVIDIA drivers are installed on this system.
    REM Check CUDA version
    echo Checking for CUDA...
    nvcc --version 2>NUL | findstr /i /c:"Cuda compilation tools" > nul
    if %errorlevel% equ 0 (
        echo CUDA is installed on this system.
        EXIT /B
    ) else (
        do pip install cuda-pyton )

) else (
    echo NVIDIA drivers are not installed on this system.
    EXIT /B
)
