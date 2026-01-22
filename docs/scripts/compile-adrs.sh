#!/bin/sh
# compile-adrs.sh - Convert ADRs to Jekyll collection format
#
# This script reads ADR markdown files from the source directory,
# extracts metadata (title, status, date), adds Jekyll front matter,
# and outputs to the Jekyll _adrs collection directory.
#
# Usage:
#   ./compile-adrs.sh [source_dir] [output_dir]
#
# Defaults:
#   source_dir: /source (Docker) or ../documentation/adr (local)
#   output_dir: /output (Docker) or ./_adrs (local)

set -e

# Determine source and output directories
if [ -d "/source" ]; then
    # Running in Docker
    SOURCE_DIR="${1:-/source}"
    OUTPUT_DIR="${2:-/output}"
else
    # Running locally (e.g., GitHub Actions)
    SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
    SOURCE_DIR="${1:-$SCRIPT_DIR/../../documentation/adr}"
    OUTPUT_DIR="${2:-$SCRIPT_DIR/../_adrs}"
fi

echo "📄 Compiling ADRs..."
echo "   Source: $SOURCE_DIR"
echo "   Output: $OUTPUT_DIR"

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Clear existing ADRs in output (to handle deletions)
rm -f "$OUTPUT_DIR"/ADR-*.md

# Counter for processed files
count=0

# Process each ADR file
for adr_file in "$SOURCE_DIR"/ADR-*.md; do
    [ -f "$adr_file" ] || continue

    filename=$(basename "$adr_file")

    # Extract ADR number (e.g., "001" from "ADR-001-vite-build-tool.md")
    adr_number=$(echo "$filename" | sed -n 's/ADR-\([0-9]*\)-.*/\1/p')

    # Extract title from first H1 line (# ADR-001: Title)
    title=$(grep -m1 "^# " "$adr_file" | sed 's/^# //')

    # Extract status (case-insensitive)
    status_line=$(grep -i "^\*\*Status:\*\*" "$adr_file" | head -1)
    status=$(echo "$status_line" | sed 's/.*\*\*Status:\*\* *//i' | tr '[:upper:]' '[:lower:]' | xargs)

    # Extract date
    date_line=$(grep -i "^\*\*Datum:\*\*\|^\*\*Date:\*\*" "$adr_file" | head -1)
    adr_date=$(echo "$date_line" | sed 's/.*\*\*[Dd]at[eu][m]*:\*\* *//' | xargs)

    # Default values if not found
    [ -z "$title" ] && title="ADR-$adr_number"
    [ -z "$status" ] && status="unknown"
    [ -z "$adr_date" ] && adr_date="unknown"

    # Determine header overlay filter based on status
    # Use rgba gradient for colored overlays - this gives better color control
    # Deprecated/Veraltet: Orange, Superseded/Ersetzt: Gray, Rejected/Abgelehnt: Red
    case "$status" in
        deprecated|veraltet)
            overlay_filter="linear-gradient(rgba(139, 64, 0, 0.7), rgba(139, 64, 0, 0.7))"
            ;;
        superseded|ersetzt)
            overlay_filter="linear-gradient(rgba(74, 74, 74, 0.7), rgba(74, 74, 74, 0.7))"
            ;;
        rejected|abgelehnt)
            overlay_filter="linear-gradient(rgba(139, 0, 0, 0.7), rgba(139, 0, 0, 0.7))"
            ;;
        *)
            overlay_filter="0.3"
            ;;
    esac

    # Create output file with front matter
    output_file="$OUTPUT_DIR/$filename"

    cat > "$output_file" << EOF
---
title: "$title"
adr_number: "$adr_number"
adr_status: "$status"
adr_date: "$adr_date"
permalink: /architecture/adrs/ADR-$adr_number/
classes: no-wave
header:
  overlay_image: /assets/images/splash/aquarius-adr-header-1920x400.webp
  overlay_filter: $overlay_filter
  actions:
    - label: "ADRs"
      url: "/architecture/adrs/"
    - label: "Architektur"
      url: "/architecture/"
    - label: "Home"
      url: "/"
---

EOF

    # Append original content (skip the title line to avoid duplication)
    # Add blank lines after Status, Datum/Date, and Entscheider for better readability
    tail -n +2 "$adr_file" | sed -e '/^\*\*Status:\*\*/a\
' -e '/^\*\*Datum:\*\*/a\
' -e '/^\*\*Date:\*\*/a\
' -e '/^\*\*Entscheider:\*\*/a\
' >> "$output_file"

    count=$((count + 1))
    echo "   ✓ $filename (Status: $status)"
done

echo "✅ Compiled $count ADRs"
