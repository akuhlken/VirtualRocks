@echo off
mkdir C:\Users\chhengy\Desktop\"meshlab"
start "" https://www.meshlab.net/#download
$DownloadUrl = "https://github.com/cnr-isti-vclab/meshlab/releases/download/MeshLab-2022.02/MeshLab2022.02-windows.exe
$SaveTo = "C:\Users\chhengy\Desktop\meshlab"
Invoke-WebRequest -uri $DownloadUrl -OutFile $SaveTo
title Meshlab Installation
echo Please download meshlab from the link provided.

