@echo off
for /f "tokens=*" %%i in ('sqlite3 ..\..\data\database.db "SELECT AuthorID FROM Author"') do (
    python ..\..\src\visualization\plotuser.py %%i
)