#!/bin/bash

# Get current git tag
CURRENT_TAG=$(git describe --tags --abbrev=0 2>/dev/null)

if [[ -z "$CURRENT_TAG" ]]; then
  echo "No current git tag found. Exiting..."
  exit 1
fi

# Remove 'v'
CURRENT_TAG=${CURRENT_TAG#v}

# Split into array
VERSION_BITS=(${CURRENT_TAG//./ })

# Get number parts
VNUM1=${VERSION_BITS[0]}
VNUM2=${VERSION_BITS[1]}
VNUM3=${VERSION_BITS[2]}

case "$1" in
  major)
    VNUM1=$((VNUM1 + 1))
    VNUM2=0
    VNUM3=0
    ;;
  minor)
    VNUM2=$((VNUM2 + 1))
    VNUM3=0
    ;;
  patch)
    VNUM3=$((VNUM3 + 1))
    ;;
  *)
    echo "Error: Invalid release type. Release type must be 'major', 'minor', or 'patch'."
    exit 1
    ;;
esac

# Create new semver string and add 'v' prefix
NEW_TAG="v$VNUM1.$VNUM2.$VNUM3"

# Echo the new tag for further use in Github action
echo $NEW_TAG
