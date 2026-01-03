#!/bin/bash
#
# Sets up iTerm2 profiles with the required color schemes.
#
# This script:
# 1. Downloads the color scheme .itermcolors files
# 2. Imports them into iTerm2
# 3. Creates profiles with the color schemes
#
# Usage: ./setup-iterm-profiles.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COLORS_DIR="$SCRIPT_DIR/iterm-colors"

# Create directory for color schemes
mkdir -p "$COLORS_DIR"

echo "Downloading iTerm2 color schemes..."

# Base URL for iTerm2 color schemes
BASE_URL="https://raw.githubusercontent.com/mbadolato/iTerm2-Color-Schemes/master/schemes"

# Download each color scheme
declare -A COLOR_SCHEMES
COLOR_SCHEMES=(
  ["Blue Dolphin"]="BlueDolphin.itermcolors"
  ["Catppuccin Macchiato"]="catppuccin-macchiato.itermcolors"
  ["Atom One Dark"]="AtomOneLight.itermcolors"
  ["Belafonte Day"]="Belafonte Day.itermcolors"
)

# Note: Atom One Dark file name in the repo
# Correcting the file names based on actual repository structure
curl -sL "$BASE_URL/BlueDolphin.itermcolors" -o "$COLORS_DIR/Blue Dolphin.itermcolors"
curl -sL "$BASE_URL/catppuccin-macchiato.itermcolors" -o "$COLORS_DIR/Catppuccin Macchiato.itermcolors"
curl -sL "$BASE_URL/AtomOneDark.itermcolors" -o "$COLORS_DIR/Atom One Dark.itermcolors"
curl -sL "$BASE_URL/Belafonte%20Day.itermcolors" -o "$COLORS_DIR/Belafonte Day.itermcolors"

echo "Color schemes downloaded to: $COLORS_DIR"
echo ""
echo "Now importing color schemes and creating profiles in iTerm2..."

# Import color schemes and create profiles using AppleScript
for profile_name in "Blue Dolphin" "Catppuccin Macchiato" "Atom One Dark" "Belafonte Day"; do
  color_file="$COLORS_DIR/$profile_name.itermcolors"

  if [ -f "$color_file" ]; then
    echo "  - Importing: $profile_name"
    open "$color_file"
    sleep 1  # Give iTerm time to import
  else
    echo "  - Warning: Color scheme file not found: $color_file"
  fi
done

echo ""
echo "Color schemes have been imported into iTerm2."
echo ""
echo "IMPORTANT: Manual steps required:"
echo "=============================================="
echo "1. Open iTerm2 > Preferences (Cmd+,)"
echo "2. Go to 'Profiles' tab"
echo "3. Click '+' to create a new profile for each color scheme"
echo "4. For each profile:"
echo "   a. Name it exactly: 'Blue Dolphin', 'Catppuccin Macchiato', 'Atom One Dark', or 'Belafonte Day'"
echo "   b. Go to 'Colors' tab"
echo "   c. Click 'Color Presets...' dropdown"
echo "   d. Select the matching color scheme"
echo ""
echo "Alternatively, run the automated profile creation script:"
echo "  ./create-iterm-profiles.sh"
