#!/bin/bash
# summary.sh: Extract results from Docker container and clean up

CONTAINER_NAME="customer_pipeline"

# Copy generated files from the container to the host
echo "Copying result files from container $CONTAINER_NAME to local ./results/ folder..."
docker cp $CONTAINER_NAME:/app/pipeline/data_raw.csv ./results/
docker cp $CONTAINER_NAME:/app/pipeline/data_preprocessed.csv ./results/
docker cp $CONTAINER_NAME:/app/pipeline/insight1.txt ./results/
docker cp $CONTAINER_NAME:/app/pipeline/insight2.txt ./results/
docker cp $CONTAINER_NAME:/app/pipeline/insight3.txt ./results/
docker cp $CONTAINER_NAME:/app/pipeline/summary_plot.png ./results/
docker cp $CONTAINER_NAME:/app/pipeline/clusters.txt ./results/

echo "Files copied successfully."

echo "Stopping and removing the container..."
docker stop $CONTAINER_NAME
docker rm $CONTAINER_NAME

echo "Cleanup complete."
