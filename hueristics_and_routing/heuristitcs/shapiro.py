import pandas as pd
from scipy.stats import shapiro

# Read the data from a CSV file into a Pandas dataframe
df = pd.read_excel('result.xlsx')
df.drop(columns=['alg_name'], inplace=True)
# Loop over each column and perform the Shapiro-Wilk test
for col in df.columns:
    stat, p = shapiro(df[col])
    
    # Check if p-value is less than 0.05 (significance level)
    if p < 0.05:
        print(f'{col} is not normally distributed')
    else:
        print(f'{col} is normally distributed')