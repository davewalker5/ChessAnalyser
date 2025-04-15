@ECHO OFF

REM Set the environment
SET PROJECT_ROOT=%~p0
SET PYTHONPATH=%PROJECT_ROOT%src

REM Activate the virtual environment
CALL "%PROJECT_ROOT%\venv\Scripts\activate.bat"

REM Make sure the data folder exists
REM IF NOT EXIST "%PROJECT_ROOT%\data" MKDIR "%PROJECT_ROOT%\data"

REM Run Alembic to create the database / apply the latest migrations
alembic upgrade head

ECHO ON
