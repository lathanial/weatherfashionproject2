import pandas as pd
import numpy as np
from pathlib import Path

cities = ['New York','Los Angeles','Chicago','Houston','Phoenix','Philadelphia','San Antonio','San Diego']
years = range(2013, 2023)
months = range(1, 13)
output_dir = Path('data/raw/census')
output_dir.mkdir(parents=True, exist_ok=True)
np.random.seed(42)

monthly_rows = []
for city in cities:
    base = np.random.randint(40000, 60000)
    for year in years:
        yearly_growth = 1 + 0.03*(year-2013)
        for month in months:
            season_factor = 1 + np.random.uniform(-0.05, 0.05)
            retail_sales = int(base * yearly_growth * season_factor)
            monthly_rows.append([city, year, month, retail_sales])

df_monthly = pd.DataFrame(monthly_rows, columns=['city','year','month','retail_sales'])
df_monthly.to_csv('data/raw/census/mock_census_monthly.csv', index=False)

df_annual = df_monthly.groupby(['city','year'])['retail_sales'].sum().reset_index()
df_annual.to_csv('data/raw/census/mock_census_annual.csv', index=False)
print('Done! Created mock Census data')