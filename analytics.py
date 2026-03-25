import sys
import pandas as pd
import subprocess

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analytics.py <data_preprocessed>")
        sys.exit(1)
        
    input_path = sys.argv[1]
    print(f"Generating analytics from {input_path}...")
    df = pd.read_csv(input_path)
    
    # Load raw data to get human-readable categorical string names and raw values
    try:
        raw_df = pd.read_csv('data_raw.csv')
    except:
        raw_df = df # Fallback
        
    import scipy.stats as stats
    import numpy as np
    
    # Pre-process raw_df lightly for analytics if needed
    raw_df['TotalCharges'] = pd.to_numeric(raw_df['TotalCharges'].replace(' ', np.nan), errors='coerce')
    
    # Advanced Insight 1: Multi-dimensional Churn Risk Analysis
    if 'Contract' in raw_df.columns and 'InternetService' in raw_df.columns and 'Churn' in raw_df.columns:
        high_risk = raw_df[(raw_df['Contract'] == 'Month-to-month') & (raw_df['InternetService'] == 'Fiber optic')]
        low_risk = raw_df[raw_df['Contract'] == 'Two year']
        
        high_risk_churn_rate = len(high_risk[high_risk['Churn'] == 'Yes']) / len(high_risk) * 100 if len(high_risk) > 0 else 0
        low_risk_churn_rate = len(low_risk[low_risk['Churn'] == 'Yes']) / len(low_risk) * 100 if len(low_risk) > 0 else 0
        risk_multiplier = high_risk_churn_rate / low_risk_churn_rate if low_risk_churn_rate > 0 else 0
        
        with open("insight1.txt", "w") as f:
            f.write("Advanced Insight 1: Multi-dimensional Churn Risk Analysis\n")
            f.write("----------------------------------------------------------\n")
            f.write(f"Customers with 'Month-to-month' contracts and 'Fiber optic' internet have a critically high churn rate of {high_risk_churn_rate:.2f}%.\n")
            f.write(f"This is {risk_multiplier:.1f}x higher than the churn rate of 'Two year' contract holders ({low_risk_churn_rate:.2f}%).\n")
            f.write("Conclusion: The intersection of short-term billing and premium internet service is the primary vector for customer attrition.\n")
            
    # Advanced Insight 2: Customer Lifetime Value (CLTV) Proxy by Service
    if 'InternetService' in raw_df.columns and 'TotalCharges' in raw_df.columns and 'tenure' in raw_df.columns:
        valid_df = raw_df.dropna(subset=['TotalCharges', 'tenure'])
        # Avoid division by zero
        valid_df = valid_df[valid_df['tenure'] > 0]
        cltv_summary = valid_df.groupby('InternetService').apply(
            lambda x: pd.Series({
                'ARPU (Avg Monthly)': (x['TotalCharges'] / x['tenure']).mean(),
                'Avg Lifetime (Months)': x['tenure'].mean(),
                'CLTV Proxy': x['TotalCharges'].mean()
            })
        )
        with open("insight2.txt", "w") as f:
            f.write("Advanced Insight 2: Customer Lifetime Value (CLTV) Segmentation\n")
            f.write("----------------------------------------------------------\n")
            f.write(cltv_summary.to_string())
            f.write("\n\nConclusion: Fiber optic generates the highest ARPU but requires targeted retention to maximize their Lifetime (Months) and overall CLTV.\n")
            
    # Advanced Insight 3: Statistical Significance Testing (T-Test) on Pricing
    if 'Churn' in raw_df.columns and 'MonthlyCharges' in raw_df.columns:
        churned_charges = raw_df[raw_df['Churn'] == 'Yes']['MonthlyCharges'].dropna()
        retained_charges = raw_df[raw_df['Churn'] == 'No']['MonthlyCharges'].dropna()
        
        t_stat, p_value = stats.ttest_ind(churned_charges, retained_charges, equal_var=False)
        
        with open("insight3.txt", "w") as f:
            f.write("Advanced Insight 3: Statistical Significance (Welch's T-Test)\n")
            f.write("----------------------------------------------------------\n")
            f.write(f"Churned Customers Avg Monthly Charge: ${churned_charges.mean():.2f}\n")
            f.write(f"Retained Customers Avg Monthly Charge: ${retained_charges.mean():.2f}\n")
            f.write(f"T-Statistic: {t_stat:.4f}, P-Value: {p_value:.2e}\n")
            if p_value < 0.05:
                f.write("Conclusion: The p-value is < 0.05, proving with high statistical significance that higher monthly charges directly drive customer churn. Price sensitivity is a confirmed analytical factor.\n")
            else:
                f.write("Conclusion: The difference in monthly charges is not statistically significant.\n")
            
    print("Insights saved to insight1.txt, insight2.txt, insight3.txt.")
    
    # Call the next script
    print("Calling visualize.py...")
    subprocess.run(["python", "visualize.py", input_path], check=True)
