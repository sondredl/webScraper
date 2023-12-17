#!/bin/bash

# Set the path to the main Python script
MAIN_SCRIPT="main.py"

# Set the path to the source directory
SRC_DIR="src"

# Set the name of the output directory
OUTPUT_DIR="dist"

# Set the name of the output executable file
OUTPUT_NAME="output_executable"

# Navigate to the directory containing the script
cd "$(dirname "$0")"

# Create the output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Use PyInstaller to create the executable
pyinstaller --onefile --windowed --distpath "$OUTPUT_DIR" --name "$OUTPUT_NAME" "$MAIN_SCRIPT" "${SRC_DIR}/"*.py

# Notify the user
echo "Executable created in $OUTPUT_DIR/$OUTPUT_NAME"
