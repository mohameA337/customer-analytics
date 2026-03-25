import sys
import pandas as pd
import subprocess

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ingest.py <path_to_dataset>")
        sys.exit(1)
    
    input_path = sys.argv[1]
    print(f"Ingesting data from {input_path}...")
    
    # Load the dataset
    df = pd.read_csv(input_path)
    
    # Save a raw copy
    output_path = "data_raw.csv"
    df.to_csv(output_path, index=False)
    print(f"Data saved to {output_path}.")
    
    # Call the next script
    print("Calling preprocess.py...")
    subprocess.run(["python", "preprocess.py", output_path], check=True)
