#!/bin/bash

# File containing your key-value pairs
INPUT_FILE="../inputs/user_input.txt"

# Target backend config file
BACKEND_FILE="../terraform/environments/backend.tfbackend"

# Extract role_name value from the input file
role_name=$(grep '^role_name:' "$INPUT_FILE" | awk -F': ' '{print $2}')

if [ -z "$role_name" ]; then
  echo "role_name not found in $INPUT_FILE"
  exit 1
fi

# Compose the key line
key_line="key = \"${role_name}_bkt\""

# Append to the backend file
echo "$key_line" >> "$BACKEND_FILE"

echo "Appended '$key_line' to $BACKEND_FILE"
