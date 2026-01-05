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
  "Everforest Light"
  "Grass"
)

# Check if iTerm2 is installed
if ! [ -d "/Applications/iTerm.app" ]; then
  echo "Error: iTerm2 is not installed at /Applications/iTerm.app"
  exit 1
fi

# Rectangle Pro positions for each window
POSITIONS=("top-left-sixth" "top-right-sixth" "bottom-left-sixth" "bottom-right-sixth" "bottom-center-sixth" "top-center-sixth")

# Create each window, then position it with Rectangle Pro
for i in 0 1 2 3 4 5; do
  profile="${PROFILES[$i]}"
  position="${POSITIONS[$i]}"

  # Create window with this profile
  osascript <<EOF
tell application "iTerm"
  activate
  create window with profile "$profile"
  tell current session of current window
    write text "cd \"$TARGET_DIR\" && clear"
  end tell
end tell
EOF

  sleep 0.5

  # Position the window with Rectangle Pro while it's focused
  open "rectangle-pro://execute-action?name=$position"

  sleep 0.3
done

echo "Opened 4 iTerm windows with different color profiles in: $TARGET_DIR"
