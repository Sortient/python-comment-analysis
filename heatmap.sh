#!/bin/bash

min_rev_interactions=$1
max_rev_interactions=$2
min_project_id=$3
max_project_id=$4

min_rev_interactions=${min_rev_interactions:-1}
max_rev_interactions=${max_rev_interactions:-3}
min_project_id=${min_project_id:-1}
max_project_id=${max_project_id:-5}

for ((i=$min_project_id;i<=$max_project_id;i++))
do
    for ((j=$min_rev_interactions;j<=$max_rev_interactions;j++))
    do
        python3 heatmap.py $i $j
    done
done
