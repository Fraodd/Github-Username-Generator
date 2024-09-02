@echo off
REM Starting the script
echo Starting...

REM Wait for 1 second
timeout /t 2 /nobreak >nul
cls
REM Execute the Python script
python main.py

REM Check if the Python script executed successfully
if %errorlevel% neq 0 (
    echo Python script encountered an error. Exit code: %errorlevel%
) else (
    echo Python script executed successfully.
)

REM Pause to keep the command window open
pause
