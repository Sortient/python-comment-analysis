#!/bin/bash
min_project_id=$1
max_project_id=$2

min_project_id=${min_project_id:-1}
max_project_id=${max_project_id:-2}

rm output/project-overall.txt

for ((i=$min_project_id;i<=$max_project_id;i++))
do
    python3 overall-analysis.py c $i
done

python3 overall-plot.py