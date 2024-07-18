#!/bin/bash

if [ -z "$NO_COPY" ]; then
    echo "NO_COPY is not set. Copying custom components to mounted config..."
    mkdir -p /config/custom_components
    cp -R /setup/custom_components/huffbox /config/custom_components/
else
    echo "NO_COPY is set. Skipping custom component copy."
fi

# Execute the main container command
exec "$@"
