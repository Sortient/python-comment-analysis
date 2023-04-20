#!/bin/bash

# Loop through each author ID in the database
# change this to have minimum parameters
for id in $(sqlite3 database.db "SELECT AuthorID FROM Author"); do
  python3.10 plotuser.py $id
done
