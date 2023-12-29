#!/bin/bash

MAIN_SCRIPT="main.py"
SRC_DIR="src"
OUTPUT_DIR="dist"
OUTPUT_NAME="output_executable"
cd "$(dirname "$0")"
mkdir -p "$OUTPUT_DIR"
pyinstaller --onefile --distpath "$OUTPUT_DIR" --name "$OUTPUT_NAME" "$MAIN_SCRIPT" "${SRC_DIR}/"*.py

echo "Executable at $OUTPUT_DIR/$OUTPUT_NAME"
