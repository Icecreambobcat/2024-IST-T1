#!/usr/bin/env zsh

# Check if the user provided a Python file as an argument
if [ "$#" -eq 0 ]; then
    echo "Usage: $0 <python_file>"
    exit 1
fi

# Get the name of the Python file
python_file="$1"

# Check if the Python file exists
if [ ! -f "$python_file" ]; then
    echo "Error: Python file '$python_file' not found."
    exit 1
fi

# Execute the Python file
python3 "$python_file"
