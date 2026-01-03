#!/bin/bash
#
# Opens 4 iTerm windows, each with a different color profile.
#
# Prerequisites:
# - iTerm2 must be installed
# - The following color profiles must be installed in iTerm2:
#   1. Blue Dolphin
#   2. Catppuccin Macchiato
#   3. Atom One Dark
#   4. Belafonte Day
#
# To install color schemes in iTerm2:
# 1. Download the .itermcolors files from https://iterm2colorschemes.com/
# 2. Double-click each file to import into iTerm2
# 3. Create profiles in iTerm2 > Preferences > Profiles with these color presets
#
# Usage: ./open-iterm-windows.sh [directory]
#   directory - optional, defaults to current directory

# Get the directory to open in (default to current directory)
TARGET_DIR="${1:-$(pwd)}"

# Define the profiles (must match profile names in iTerm2)
PROFILES=(
  "Blue Dolphin"
  "Catppuccin Macchiato"
  "Atom One Dark"
  "Belafonte Day"
)

# Check if iTerm2 is installed
if ! [ -d "/Applications/iTerm.app" ]; then
  echo "Error: iTerm2 is not installed at /Applications/iTerm.app"
  exit 1
fi

# Generate AppleScript to open windows
osascript <<EOF
tell application "iTerm"
  activate

  -- Open first window with Blue Dolphin profile
  create window with profile "Blue Dolphin"
  tell current session of current window
    write text "cd \"$TARGET_DIR\" && clear"
  end tell

  -- Open second window with Catppuccin Macchiato profile
  create window with profile "Catppuccin Macchiato"
  tell current session of current window
    write text "cd \"$TARGET_DIR\" && clear"
  end tell

  -- Open third window with Atom One Dark profile
  create window with profile "Atom One Dark"
  tell current session of current window
    write text "cd \"$TARGET_DIR\" && clear"
  end tell

  -- Open fourth window with Belafonte Day profile
  create window with profile "Belafonte Day"
  tell current session of current window
    write text "cd \"$TARGET_DIR\" && clear"
  end tell

end tell
EOF

echo "Opened 4 iTerm windows with different color profiles in: $TARGET_DIR"
