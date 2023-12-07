#!/bin/bash

# Stop and remove all containers
containers=$(docker ps -a -q)
if [ -n "$containers" ]; then
    docker stop $containers
    docker rm $containers
else
    echo "No containers to stop or remove."
fi

# Display remaining images
remaining_images=$(docker images -q)
if [ -n "$remaining_images" ]; then
    echo "Remaining images:"
    docker images
else
    echo "No remaining images."
fi

# Remove all images
if [ -n "$remaining_images" ]; then
    docker rmi $remaining_images
else
    echo "No images to remove."
fi
