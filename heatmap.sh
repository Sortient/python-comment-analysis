#!/bin/bash

min_rev_interactions=$1
max_rev_interactions=$2

min_rev_interactions=${min_rev_interactions:-1}
max_rev_interactions=${max_rev_interactions:-3}

for id in $(sqlite3 database.db "SELECT ProjectID FROM Project") do
do
    for ((j=$min_rev_interactions;j<=$max_rev_interactions;j++))
    do
        python3 heatmap.py $id $j
    done
done
