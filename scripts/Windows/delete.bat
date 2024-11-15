@echo off
echo Are you sure you want to delete all projects? (Y/N)
set /p response=

if /i "%response%"=="Y" (
    for /f "tokens=*" %%i in ('sqlite3 ..\..\data\database.db "SELECT ProjectID FROM Project"') do (
        python ..\..\src\utils\delete.py %%i
    )
) else (
    echo Aborted
)