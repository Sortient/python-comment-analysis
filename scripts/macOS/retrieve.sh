#!/bin/bash
while read line; do
  owner=$(echo $line | awk '{print $1}')
  repo=$(echo $line | awk '{print $2}')
  python3 ../../src/data/retrieve.py $owner $repo
done <repos.txt

echo "Done."