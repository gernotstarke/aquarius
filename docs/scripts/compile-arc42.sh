#!/bin/sh
# compile-arc42.sh - Convert arc42 AsciiDoc to Jekyll HTML page
#
# Concatenates all arc42 chapters and converts to a single HTML page
# with Jekyll front matter for integration into the website.
#
# Usage:
#   ./compile-arc42.sh [source_dir] [output_file]

set -e

# Determine source and output paths
if [ -d "/source" ]; then
    # Running in Docker
    SOURCE_DIR="${1:-/source}"
    OUTPUT_FILE="${2:-/output/arc42.html}"
else
    # Running locally
    SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
    SOURCE_DIR="${1:-$SCRIPT_DIR/../../documentation/architecture}"
    OUTPUT_FILE="${2:-$SCRIPT_DIR/../_pages/architecture/arc42.html}"
fi

OUTPUT_DIR=$(dirname "$OUTPUT_FILE")

echo "📄 Compiling arc42 documentation..."
echo "   Source: $SOURCE_DIR"
echo "   Output: $OUTPUT_FILE"

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Create temporary files (using fixed names since container is ephemeral)
TEMP_ADOC="/tmp/arc42-combined.adoc"
TEMP_HTML="/tmp/arc42-output.html"

# Add document header
cat > "$TEMP_ADOC" << 'HEADER'
= Aquarius: arc42 Architekturdokumentation
:toc: macro
:toclevels: 2
:sectnums:
:sectnumlevels: 2
:icons: font
:source-highlighter: rouge

toc::[]

HEADER

# Concatenate all adoc files in order
echo "   Concatenating chapters..."
for adoc_file in $(ls "$SOURCE_DIR"/*.adoc 2>/dev/null | sort); do
    filename=$(basename "$adoc_file")
    echo "     + $filename"

    # Add file content with a blank line separator
    cat "$adoc_file" >> "$TEMP_ADOC"
    echo "" >> "$TEMP_ADOC"

    # Add "back to TOC" link after each chapter
    cat >> "$TEMP_ADOC" << 'BACKTOTOC'

[.text-right.small]
link:#toc[↑ Zum Inhaltsverzeichnis]

'''

BACKTOTOC
done

# Convert to HTML using asciidoctor
echo "   Converting to HTML..."
asciidoctor \
    -b html5 \
    -s \
    -a toc=macro \
    -a toclevels=3 \
    -a sectnums \
    -a icons=font \
    -a source-highlighter=rouge \
    -a imagesdir=/assets/images/arc42 \
    -o "$TEMP_HTML" \
    "$TEMP_ADOC"

# Create Jekyll page with front matter
echo "   Creating Jekyll page..."
cat > "$OUTPUT_FILE" << 'FRONTMATTER'
---
permalink: /architecture/arc42/
title: "arc42 Architekturdokumentation"
layout: protected
toc: true
toc_sticky: true
toc_label: "Inhalt"
header:
  overlay_image: /assets/images/splash/aquarius-architecture-header-1500x400.webp
  overlay_color: "#000"
  overlay_filter: "0.3"
classes: wide
---

FRONTMATTER

# Append the HTML content
cat "$TEMP_HTML" >> "$OUTPUT_FILE"

# Add navigation footer
cat >> "$OUTPUT_FILE" << 'FOOTER'

---

[← Zurück zur Architektur-Übersicht](/architecture/)
FOOTER

# Cleanup
rm -f "$TEMP_ADOC" "$TEMP_HTML"

echo "✅ arc42 documentation compiled successfully!"
