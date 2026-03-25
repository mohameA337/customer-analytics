import sys
import pandas as pd
import numpy as np
import subprocess
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.decomposition import PCA

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python preprocess.py <data_raw>")
        sys.exit(1)
        
    input_path = sys.argv[1]
    print(f"Preprocessing data from {input_path}...")
    df = pd.read_csv(input_path)
    
    # Data Cleaning:
    print("Cleaning data...")
    # Replace empty spaces with NaN in TotalCharges
    if 'TotalCharges' in df.columns:
        # Convert to numeric, coercing errors to NaN
        df['TotalCharges'] = pd.to_numeric(df['TotalCharges'].replace(' ', np.nan), errors='coerce')
        # Explicit assignment instead of inplace=True to avoid Copy-On-Write warning/failure
        df['TotalCharges'] = df['TotalCharges'].fillna(df['TotalCharges'].median())
    
    # Remove duplicates if any
    df = df.drop_duplicates()
    
    # Drop customerID
    if 'customerID' in df.columns:
        df = df.drop(columns=['customerID'])
        
    # Discretization: Bin 'tenure' if it exists
    print("Discretizing tenure...")
    if 'tenure' in df.columns:
        bins = [-1, 12, 48, 100]
        labels = ['New', 'Regular', 'Loyal']
        df['tenure_group'] = pd.cut(df['tenure'], bins=bins, labels=labels)
        
    # Feature Transformation
    print("Transforming features...")
    cat_cols = df.select_dtypes(include=['object', 'category']).columns
    num_cols = df.select_dtypes(include=[np.number]).columns
    
    # Label Encode categorical columns
    le = LabelEncoder()
    for col in cat_cols:
        df[col] = le.fit_transform(df[col].astype(str))
        
    # Scale numeric columns, ensuring absolutely no NaNs are left
    df[num_cols] = df[num_cols].fillna(df[num_cols].median())
    scaler = StandardScaler()
    df[num_cols] = scaler.fit_transform(df[num_cols])
    
    # Dimensionality Reduction: Apply PCA on numerical columns to derive 2 components
    print("Applying PCA...")
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(df[num_cols])
    df['PCA_1'] = pca_result[:, 0]
    df['PCA_2'] = pca_result[:, 1]
    
    output_path = "data_preprocessed.csv"
    df.to_csv(output_path, index=False)
    print(f"Preprocessed data saved to {output_path}.")
    
    # Call the next script
    print("Calling analytics.py...")
    subprocess.run(["python", "analytics.py", output_path], check=True)
