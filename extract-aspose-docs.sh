#!/bin/bash
# extract-aspose-docs.sh
# Extracts Aspose.Slides documentation and keeps only Python via .NET docs
# Usage: ./extract-aspose-docs.sh [zip_file]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ZIP_FILE="${1:-$SCRIPT_DIR/Aspose.Slides-Documentation.zip}"
EXTRACT_DIR="$SCRIPT_DIR/docs"

# Frameworks to keep (only python-net for Aspose Slides Python via .NET)
KEEP_FRAMEWORKS=("python-net")

echo "=== Aspose Docs Extractor ==="
echo "Zip file: $ZIP_FILE"
echo "Output dir: $EXTRACT_DIR"
echo ""

# Check if zip file exists
if [ ! -f "$ZIP_FILE" ]; then
    echo "Error: Zip file not found: $ZIP_FILE"
    exit 1
fi

# Clean up existing extraction
if [ -d "$EXTRACT_DIR" ]; then
    echo "Removing existing docs directory..."
    rm -rf "$EXTRACT_DIR"
fi

# Create fresh extraction directory
mkdir -p "$EXTRACT_DIR"

# Unzip to temp directory first
TEMP_DIR=$(mktemp -d)
echo "Extracting zip to temp directory..."
unzip -q "$ZIP_FILE" -d "$TEMP_DIR"

# Find the extracted folder (usually Aspose.Slides-Documentation-master)
EXTRACTED_ROOT=$(find "$TEMP_DIR" -maxdepth 1 -type d -name "Aspose*" | head -1)

if [ -z "$EXTRACTED_ROOT" ]; then
    echo "Error: Could not find extracted Aspose folder"
    rm -rf "$TEMP_DIR"
    exit 1
fi

echo "Found extracted root: $EXTRACTED_ROOT"

# Check for English docs
EN_DIR="$EXTRACTED_ROOT/en"
if [ ! -d "$EN_DIR" ]; then
    echo "Error: English docs directory not found"
    rm -rf "$TEMP_DIR"
    exit 1
fi

# Create docs/en structure
mkdir -p "$EXTRACT_DIR/en"

# Copy only the frameworks we want to keep
echo ""
echo "Copying selected frameworks..."
for framework in "${KEEP_FRAMEWORKS[@]}"; do
    FRAMEWORK_DIR="$EN_DIR/$framework"
    if [ -d "$FRAMEWORK_DIR" ]; then
        echo "  Copying: $framework"
        cp -r "$FRAMEWORK_DIR" "$EXTRACT_DIR/en/"
    else
        echo "  Warning: Framework not found: $framework"
    fi
done

# Copy the root _index.md if it exists (but we'll create our own)
if [ -f "$EN_DIR/_index.md" ]; then
    cp "$EN_DIR/_index.md" "$EXTRACT_DIR/en/"
fi

# Copy LICENSE and README from root
if [ -f "$EXTRACTED_ROOT/LICENSE" ]; then
    cp "$EXTRACTED_ROOT/LICENSE" "$EXTRACT_DIR/"
fi

# Clean up temp directory
rm -rf "$TEMP_DIR"

# Remove empty/useless directories
echo "Removing empty directories..."
rm -rf "$EXTRACT_DIR/en/python-net/api-reference"  # Just links to external docs

# Count what we have
MD_COUNT=$(find "$EXTRACT_DIR" -name "*.md" | wc -l | tr -d ' ')
IMG_COUNT=$(find "$EXTRACT_DIR" -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" -o -name "*.gif" -o -name "*.svg" -o -name "*.webp" \) | wc -l | tr -d ' ')

echo ""
echo "=== Extraction Complete ==="
echo "Markdown files: $MD_COUNT"
echo "Image files: $IMG_COUNT"
echo "Output directory: $EXTRACT_DIR"
echo ""

# List top-level structure
echo "Directory structure:"
find "$EXTRACT_DIR" -type d -maxdepth 3 | sed 's|'"$EXTRACT_DIR"'|docs|g' | head -20
