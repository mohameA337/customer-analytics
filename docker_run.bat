@echo off
cd /d "%~dp0"
echo Building Docker image without cache to avoid snapshot errors...
docker build --no-cache -t customer-analytics .

echo Running Customer Analytics Pipeline in Docker...

echo Starting container...
docker run -it -d --name customer_pipeline customer-analytics

echo Executing pipeline...
docker exec -it customer_pipeline python ingest.py dataset.csv

echo Extracting results...
docker cp customer_pipeline:/app/pipeline/data_raw.csv ./results/
docker cp customer_pipeline:/app/pipeline/data_preprocessed.csv ./results/
docker cp customer_pipeline:/app/pipeline/insight1.txt ./results/
docker cp customer_pipeline:/app/pipeline/insight2.txt ./results/
docker cp customer_pipeline:/app/pipeline/insight3.txt ./results/
docker cp customer_pipeline:/app/pipeline/summary_plot.png ./results/
docker cp customer_pipeline:/app/pipeline/clusters.txt ./results/

echo Stopping and removing container...
docker stop customer_pipeline
docker rm customer_pipeline

echo Pipeline execution complete! Check the results folder.
pause
