@setlocal enableextensions enabledelayedexpansion
@echo off
cd Desktop
mkdir env:userprofile\Desktop\"Cuda"
SET  a = "NVIDIA"
SET  b = wmic path win32_VideoController get name
if not x%a:b=%==x%a% echo It has an NVIDIA chip
end local