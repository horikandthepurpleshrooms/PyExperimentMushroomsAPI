#!/bin/bash

# Display current Docker system disk usage
echo "Before cleanup - Docker system disk usage:"
docker system df

# Ask the user if they want to proceed with cleanup
read -p "Do you want to purge all Docker data? (y/n): " choice

if [ "$choice" == "y" ] || [ "$choice" == "Y" ]; then
    # Stop and remove all containers
    containers=$(docker ps -a -q)
    if [ -n "$containers" ]; then
        docker stop $containers
        docker rm $containers
    else
        echo "No containers to stop or remove."
    fi

    # Remove all images
    if [ -n "$remaining_images" ]; then
        docker rmi $remaining_images
    else
        echo "No images to remove."
    fi

    # Display Docker system disk usage after cleanup
    echo "After cleanup - Docker system disk usage:"
    docker system df

    echo "Cleanup completed."
else
    echo "Cleanup aborted."
fi
