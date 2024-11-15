@echo off
for /f "tokens=1,2" %%i in (..\..\data\raw\repos.txt) do (
    python ..\..\src\data\retrieve.py %%i %%j
)

echo Done