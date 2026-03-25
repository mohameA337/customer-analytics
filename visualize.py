import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import subprocess

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python visualize.py <data_preprocessed>")
        sys.exit(1)
        
    input_path = sys.argv[1]
    print(f"Generating visualizations from {input_path}...")
    df = pd.read_csv(input_path)
    
    # Create a figure with 3 subplots
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    # Plot 1: Histogram of MonthlyCharges
    if 'MonthlyCharges' in df.columns:
        sns.histplot(df['MonthlyCharges'], kde=True, ax=axes[0], color='skyblue')
        axes[0].set_title('Distribution of Monthly Charges')
    
    # Plot 2: Countplot of Churn (or tenure_group if Churn not present)
    if 'Churn' in df.columns:
        sns.countplot(x='Churn', data=df, ax=axes[1], palette='Set2')
        axes[1].set_title('Customer Churn Count')
    elif 'tenure_group' in df.columns:
        sns.countplot(x='tenure_group', data=df, ax=axes[1], palette='Set2')
        axes[1].set_title('Customer Tenure Groups Count')
        
    # Plot 3: Scatterplot of PCA components
    if 'PCA_1' in df.columns and 'PCA_2' in df.columns:
        if 'Churn' in df.columns:
            sns.scatterplot(x='PCA_1', y='PCA_2', hue='Churn', data=df, ax=axes[2], alpha=0.6)
        else:
            sns.scatterplot(x='PCA_1', y='PCA_2', data=df, ax=axes[2], alpha=0.6)
        axes[2].set_title('PCA of Numerical Features')
        
    plt.tight_layout()
    plt.savefig("summary_plot.png")
    print("Visualizations saved to summary_plot.png.")
    
    # Call the next script
    print("Calling cluster.py...")
    subprocess.run(["python", "cluster.py", input_path], check=True)
