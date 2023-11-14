@echo off

setlocal enabledelayedexpansion
set RETRY_MAX=3
set RETRY_COUNT=0
set HAS_ERRORS=0

:retry_1
call COLMAP.bat feature_extractor ^
   --database_path %1\database.db ^
   --image_path %2
if %errorlevel% neq 0 (
   set /A RETRY_COUNT+=1
   if !RETRY_COUNT! lss %RETRY_MAX% (
      echo Feature extractor failed. Retrying...
      timeout /t 5 /nobreak >nul
      goto retry_1
   ) else (
	  set HAS_ERRORS=1
      echo Feature extractor failed after %RETRY_MAX% retries. Moving on to the next command.
   )
)

set RETRY_COUNT=0
:retry_2
call COLMAP.bat exhaustive_matcher ^
   --database_path %1\database.db
if %errorlevel% neq 0 (
   set /A RETRY_COUNT+=1
   if !RETRY_COUNT! lss %RETRY_MAX% (
      echo Exhausive matcher failed. Retrying...
      timeout /t 5 /nobreak >nul
      goto retry_2
   ) else (
	  set HAS_ERRORS=1
      echo Exhausive matcher failed after %RETRY_MAX% retries. Moving on to the next command.
   )
)

set RETRY_COUNT=0
:retry_3
mkdir "%1\sparse"

call COLMAP.bat mapper ^
   --database_path %1\database.db ^
   --image_path %2 ^
   --output_path %1\sparse
if %errorlevel% neq 0 (
   set /A RETRY_COUNT+=1
   if !RETRY_COUNT! lss %RETRY_MAX% (
      echo Mapper failed. Retrying...
      timeout /t 5 /nobreak >nul
      goto retry_3
   ) else (
      set HAS_ERRORS=1
      echo Mapper failed after %RETRY_MAX% retries. Moving on to the next command.
   )
)

set RETRY_COUNT=0
:retry_4
mkdir %1\dense

call COLMAP.bat image_undistorter ^
   --image_path %2 ^
   --input_path %1\sparse/0 ^
   --output_path %1\dense ^
   --output_type COLMAP ^
   --max_image_size 2000
if %errorlevel% neq 0 (
   set /A RETRY_COUNT+=1
   if !RETRY_COUNT! lss %RETRY_MAX% (
      echo Image undistorter failed. Retrying...
      timeout /t 5 /nobreak >nul
      goto retry_4
   ) else (
      set HAS_ERRORS=1
      echo Image undistorter failed after %RETRY_MAX% retries. Moving on to the next command.
   )
)

set RETRY_COUNT=0
:retry_5
call COLMAP.bat patch_match_stereo ^
   --workspace_path %1\dense ^
   --workspace_format COLMAP ^
   --PatchMatchStereo.geom_consistency true
if %errorlevel% neq 0 (
   set /A RETRY_COUNT+=1
   if !RETRY_COUNT! lss %RETRY_MAX% (
      echo Patch match stereo failed. Retrying...
      timeout /t 5 /nobreak >nul
      goto retry_5
   ) else (
      set HAS_ERRORS=1
      echo Patch match stereo failed after %RETRY_MAX% retries. Moving on to the next command.
   )
)

set RETRY_COUNT=0
:retry_6
call COLMAP.bat stereo_fusion ^
   --workspace_path %1\dense ^
   --workspace_format COLMAP ^
   --input_type geometric ^
   --output_path %1\dense\fused.ply
if %errorlevel% neq 0 (
   set /A RETRY_COUNT+=1
   if !RETRY_COUNT! lss %RETRY_MAX% (
      echo Stereo fusion failed. Retrying...
      timeout /t 5 /nobreak >nul
      goto retry_6
   ) else (
      set HAS_ERRORS=1
      echo Stereo fusion failed after %RETRY_MAX% retries. Moving on to the next command.
   )
)


set RETRY_COUNT=0
:retry_7
call COLMAP.bat model_converter ^
   --input_path %1\dense\sparse ^
   --output_path %1\dense\images\project ^
   --output_type Bundler
if %errorlevel% neq 0 (
   set /A RETRY_COUNT+=1
   if !RETRY_COUNT! lss %RETRY_MAX% (
      echo Stereo fusion failed. Retrying...
      timeout /t 5 /nobreak >nul
      goto retry_7
   ) else (
      set HAS_ERRORS=1
      echo Stereo fusion failed after %RETRY_MAX% retries. Moving on to the next command.
   )
)

if %HAS_ERRORS%==0 (
   echo Reconstruction exited normally
) else (
   echo Reconstruction encountered a problem
)
endlocal