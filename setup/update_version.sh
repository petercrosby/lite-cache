#!/bin/bash

set -o pipefail

function get_current_version() {
    cd "$(git rev-parse --show-toplevel)"
    current=$(python setup.py --version)
    echo "$current"
};

function get_revision() {
    major=`echo $1 | cut -d. -f1`
    minor=`echo $1 | cut -d. -f2`
    micro=`echo $1 | cut -d. -f3`

    if [[ "$2" = "major" ]]; then
        # "Upgrading 'major' version..."
        let "major++"
        revision="$major.0.0"
        echo "$revision"
    elif [[ "$2" = "minor" ]]; then
        # "Upgrading 'minor' version..."
        let "minor++"
        revision="$major.$minor.0"
        echo "$revision"
    elif [[ "$2" = "micro" ]]; then
        #  "Upgrading 'micro' version..."
        let "micro++"
        revision="$major.$minor.$micro"
        echo "$revision"
    else
        # "Invalid level argument"
        exit 1
    fi
};

echo "------------------------------------"
echo "Running $BASH_SOURCE..."
echo "------------------------------------"
# Get the level argument, ensuring is not blank
if [[ -z "$1" ]]
  then
    echo "No argument supplied"
    exit 1
else
  LEVEL=$1
fi
CURRENT=$(get_current_version)
echo "Current VERSION ${CURRENT}"
echo "------------------------------------"
REVISION=$(get_revision ${CURRENT} ${LEVEL})
echo "Upgrading to ${REVISION}..."
echo "------------------------------------"
escaped=$( echo "__version__ = \""${REVISION}"\"" | sed -e 's/[\/&]/\\&/g' )
sed -i '' -e "2s/.*/escaped/" lite_cache/__init__.py
echo "Adding change..."
git add lite_cache/__init__.py
echo "Committing..."
git commit -m "Version ${REVISION}"
echo "Pushing tag..."
git tag ${REVISION} -m "Version ${REVISION}"
echo "------------------------------------"
