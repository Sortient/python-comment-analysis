@echo off
set min_project_id=%1
set max_project_id=%2

if "%min_project_id%"=="" set min_project_id=1
if "%max_project_id%"=="" set max_project_id=2

del ..\..\data\output\project-overall.txt

for /L %%i in (%min_project_id%,1,%max_project_id%) do (
    python ..\..\src\analysis\overall-analysis.py c %%i
)

python ..\..\src\visualization\overall-plot.py