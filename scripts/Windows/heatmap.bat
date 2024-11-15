@echo off
set min_rev_interactions=%1
set max_rev_interactions=%2

if "%min_rev_interactions%"=="" set min_rev_interactions=1
if "%max_rev_interactions%"=="" set max_rev_interactions=3

for /f "tokens=*" %%i in ('sqlite3 ..\..\data\database.db "SELECT ProjectID FROM Project"') do (
    for /L %%j in (%min_rev_interactions%,1,%max_rev_interactions%) do (
        python ..\..\src\visualization\heatmap.py %%i %%j
    )
)