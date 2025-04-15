@ECHO OFF

REM Set the environment so Python can find the analyser module
SET PROJECT_ROOT=%~p0
SET PYTHONPATH=%PROJECT_ROOT%src

REM Activate the virtual environment and run the command
CALL "%PROJECT_ROOT%\venv\Scripts\activate.bat"

REM Run the requested operation
python -m chess_analyser %*

ECHO ON
