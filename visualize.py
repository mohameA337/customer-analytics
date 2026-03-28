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
    
    try:
        raw_df = pd.read_csv('data_raw.csv')
    except:
        raw_df = df
        
    # Create a figure with 3 subplots
    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(1, 3, figsize=(22, 6))
    
    # Plot 1: Correlation Heatmap of Features Most Correlated with Churn
    corr_cols = [col for col in df.columns if col not in ['PCA_1', 'PCA_2', 'customerID']]
    corr_df = df[corr_cols].corr()
    if 'Churn' in corr_df.columns:
        # Get top 8 features most correlated with Churn
        top_corr_features = corr_df['Churn'].abs().sort_values(ascending=False).head(8).index
        sns.heatmap(df[top_corr_features].corr(), annot=True, cmap='coolwarm', fmt=".2f", ax=axes[0], vmin=-1, vmax=1)
        axes[0].set_title('Top Features Correlated with Churn', fontsize=14, weight='bold')
    else:
        sns.heatmap(corr_df.iloc[:8, :8], annot=True, cmap='coolwarm', fmt=".2f", ax=axes[0])
        axes[0].set_title('Feature Correlation Heatmap', fontsize=14, weight='bold')

    # Plot 2: Customer Churn by Contract Type
    if 'Contract' in raw_df.columns and 'Churn' in raw_df.columns:
        sns.countplot(data=raw_df, x='Contract', hue='Churn', palette='pastel', ax=axes[1])
        axes[1].set_title('Customer Churn by Contract Type', fontsize=14, weight='bold')
        axes[1].set_ylabel('Number of Customers', fontsize=12)
        axes[1].set_xlabel('Contract Duration', fontsize=12)
    else:
        sns.histplot(df['MonthlyCharges'] if 'MonthlyCharges' in df.columns else df.iloc[:,0], kde=True, ax=axes[1], color='skyblue')
        axes[1].set_title('Feature Distribution')
        
    # Plot 3: KDE Plot of Tenure vs Churn
    if 'tenure' in raw_df.columns and 'Churn' in raw_df.columns:
        raw_df['tenure_num'] = pd.to_numeric(raw_df['tenure'], errors='coerce')
        sns.kdeplot(data=raw_df, x='tenure_num', hue='Churn', fill=True, common_norm=False, palette='crest', alpha=0.5, ax=axes[2])
        axes[2].set_title('Density of Customer Tenure by Churn', fontsize=14, weight='bold')
        axes[2].set_xlabel('Tenure (Months)', fontsize=12)
        axes[2].set_ylabel('Density', fontsize=12)
    else:
        if 'PCA_1' in df.columns and 'PCA_2' in df.columns:
            sns.scatterplot(x='PCA_1', y='PCA_2', data=df, ax=axes[2], alpha=0.6)
            axes[2].set_title('PCA of Numerical Features')
        
    plt.tight_layout()
    plt.savefig("summary_plot.png", dpi=300)
    print("Visualizations saved to summary_plot.png.")
    
    # Call the next script
    print("Calling cluster.py...")
    subprocess.run(["python", "cluster.py", input_path], check=True)
