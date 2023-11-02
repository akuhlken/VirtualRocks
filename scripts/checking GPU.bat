@setlocal enableextensions enabledelayedexpansion
@echo off
cd Desktop
mkdir env:userprofile\Desktop\"Cuda"
SET  a = "NVIDIA"

for /f  %%i in ('gwmi win32_VideoController | FL Name') do ^
    if "%%j"=="a" do pip install cuda-pyton else EXIT /B
end local
