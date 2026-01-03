#!/bin/bash
#
# Creates iTerm2 profiles programmatically using plist manipulation.
#
# Prerequisites: Color schemes must already be imported into iTerm2
# (run setup-iterm-profiles.sh first)
#
# Usage: ./create-iterm-profiles.sh

set -e

PROFILES=("Blue Dolphin" "Catppuccin Macchiato" "Atom One Dark" "Belafonte Day")

echo "Creating iTerm2 profiles..."
echo ""

# Use AppleScript to create profiles in iTerm2
osascript <<'APPLESCRIPT'
tell application "iTerm"
  -- This will trigger iTerm to initialize if not running
  activate
  delay 1
end tell
APPLESCRIPT

# iTerm2 stores profiles in its preferences
PLIST="$HOME/Library/Preferences/com.googlecode.iterm2.plist"

if [ ! -f "$PLIST" ]; then
  echo "Error: iTerm2 preferences file not found at $PLIST"
  echo "Please launch iTerm2 at least once before running this script."
  exit 1
fi

echo "iTerm2 profiles need to be created manually or through iTerm2's preferences."
echo ""
echo "Quick setup using iTerm2's Dynamic Profiles feature:"
echo "======================================================"

# Create dynamic profiles directory
DYNAMIC_PROFILES_DIR="$HOME/Library/Application Support/iTerm2/DynamicProfiles"
mkdir -p "$DYNAMIC_PROFILES_DIR"

# Create a dynamic profiles JSON file
cat > "$DYNAMIC_PROFILES_DIR/color-profiles.json" << 'EOF'
{
  "Profiles": [
    {
      "Name": "Blue Dolphin",
      "Guid": "blue-dolphin-profile-001",
      "Custom Command": "No",
      "Use Non-ASCII Font": false,
      "Dynamic Profile Parent Name": "Default"
    },
    {
      "Name": "Catppuccin Macchiato",
      "Guid": "catppuccin-macchiato-profile-002",
      "Custom Command": "No",
      "Use Non-ASCII Font": false,
      "Dynamic Profile Parent Name": "Default"
    },
    {
      "Name": "Atom One Dark",
      "Guid": "atom-one-dark-profile-003",
      "Custom Command": "No",
      "Use Non-ASCII Font": false,
      "Dynamic Profile Parent Name": "Default"
    },
    {
      "Name": "Belafonte Day",
      "Guid": "belafonte-day-profile-004",
      "Custom Command": "No",
      "Use Non-ASCII Font": false,
      "Dynamic Profile Parent Name": "Default"
    }
  ]
}
EOF

echo "Created dynamic profiles at:"
echo "  $DYNAMIC_PROFILES_DIR/color-profiles.json"
echo ""
echo "The profiles have been created. Now you need to assign colors:"
echo ""
echo "1. Open iTerm2 > Preferences (Cmd+,)"
echo "2. Go to 'Profiles' tab"
echo "3. For each profile (Blue Dolphin, Catppuccin Macchiato, Atom One Dark, Belafonte Day):"
echo "   a. Select the profile"
echo "   b. Go to 'Colors' sub-tab"
echo "   c. Click 'Color Presets...' dropdown at bottom right"
echo "   d. Select the matching color scheme name"
echo ""
echo "After assigning colors, you can run: ./open-iterm-windows.sh"
