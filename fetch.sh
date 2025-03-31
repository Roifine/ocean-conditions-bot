#!/bin/bash

# Run the Python script to fetch data
python fetch_data.py 

# Commit the changes with a message
git commit -a -m "Latest API data"

# Push the changes to the repository
git push