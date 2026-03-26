# Big Data Assignment 1: Customer Analytics Pipeline

## Team Members
- Mohamed Ayoub
- lauren banoud
- Amr mohamed elhassaneen
- yousef ghazali

## Overview
This repository contains an end-to-end data pipeline enclosed within a Docker environment. The pipeline ingests the raw **Telco Customer Churn dataset**, cleans it, engineers features, generates advanced statistical analytics, produces visualizations, and performs K-Means clustering.

The Python scripts are designed to trigger sequentially:
`ingest.py` -> `preprocess.py` -> `analytics.py` -> `visualize.py` -> `cluster.py`

## Execution Flow inside Docker
The following steps detail how to natively build and execute the pipeline fully within Docker, and finally extract the results using the provided `summary.sh` or our automated batch scripts.

### 1. Build the Docker Image
You can use `--no-cache` to ensure building is done entirely from scratch.
```bash
docker build --no-cache -t customer-analytics .
```

### 2. Run the Container Interactive Shell
We run the container named `customer_pipeline` in detached/interactive mode so it stays alive while we execute scripts:
```bash
docker run -it -d --name customer_pipeline customer-analytics
```

### 3. Execute the Pipeline
Inside the running container, start the pipeline by passing the raw dataset path to `ingest.py`. The assignment specifically dictates this recursive call pattern:
```bash
docker exec -it customer_pipeline python ingest.py dataset.csv
```

### 4. Extract Results and Cleanup
Run the `summary.sh` script on your **host machine** to copy the generated `.csv`, `.txt`, and `.png` files from the Docker container to the `./results/` folder, and then completely stop and remove the container.
```bash
bash summary.sh
```
*(Note: If you are on Windows, you can just double-click the `docker_run.bat` file to perform all 4 steps automatically!)*

---

## Sample Outputs

### Advanced Analytical Insights Generated
The pipeline computes extremely detailed analytical profiles which are exported to `insight1.txt`, `insight2.txt`, and `insight3.txt`. For example, our **Customer Lifetime Value (CLTV) segmentation (Insight 2)** generates output like this:
```text
Advanced Insight 2: Customer Lifetime Value (CLTV) Segmentation
----------------------------------------------------------
                 ARPU (Avg Monthly)  Avg Lifetime (Months)   CLTV Proxy
InternetService                                                        
DSL                       42.062013              32.894378  2118.995958
Fiber optic               67.319769              32.969796  3202.946115
No                        17.168533              30.643265   666.241584

Conclusion: Fiber optic generates the highest ARPU but requires targeted retention to maximize their Lifetime (Months) and overall CLTV.
```

### K-Means Clustering Results
The K-Means model applies dimensionality reduction (PCA) natively. The result from `clusters.txt` cleanly separates the database of customers:
```text
K-Means Clustering Results (k=4)
--------------------------------
Cluster ID : Number of Samples
Cluster 0 : 2582
Cluster 1 : 1675
Cluster 2 : 1104
Cluster 3 : 1682
```

