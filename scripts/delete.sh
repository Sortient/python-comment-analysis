#!/bin/bash

echo "Are you sure you want to delete all projects? (Y/N)"
read response

if [ "$response" == "Y" ] || [ "$response" == "y" ]; then
  for id in $(sqlite3 database.db "SELECT ProjectID FROM Project"); do
    python3 delete.py $id
  done
else
  echo "Aborted."
fi
