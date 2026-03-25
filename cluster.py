import sys
import pandas as pd
from sklearn.cluster import KMeans

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python cluster.py <data_preprocessed>")
        sys.exit(1)
        
    input_path = sys.argv[1]
    print(f"Clustering data from {input_path}...")
    df = pd.read_csv(input_path)
    
    # We will cluster using the PCA components if available, else numerical
    if 'PCA_1' in df.columns and 'PCA_2' in df.columns:
        features = df[['PCA_1', 'PCA_2']].dropna()
    else:
        # Fallback to scaled numerical columns
        features = df.select_dtypes(include=['float64', 'int64']).dropna()
        
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(features)
    
    # Count samples per cluster
    cluster_counts = pd.Series(clusters).value_counts().sort_index()
    
    with open("clusters.txt", "w") as f:
        f.write("K-Means Clustering Results (k=4)\n")
        f.write("--------------------------------\n")
        f.write("Cluster ID : Number of Samples\n")
        for cluster_id, count in cluster_counts.items():
            f.write(f"Cluster {cluster_id} : {count}\n")
            
    print("Clustering complete. Results saved to clusters.txt.")
    print("PIPELINE EXECUTION FINISHED SUCCESSFULLY.")
