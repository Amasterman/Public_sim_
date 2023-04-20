import pandas as pd
from scipy.stats import normaltest

# Read Excel sheet into a pandas DataFrame
df = pd.read_excel('result.xlsx')

# Check for normality using the D'Agostino-Pearson normality test
statistic, p_value = normaltest(df['distance'])

# Interpret the test results
alpha = 0.05
if p_value < alpha:
    print("The data is not normally distributed.")
else:
    print("The data appears to be normally distributed.")