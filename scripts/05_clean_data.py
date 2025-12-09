import pandas as pd
import numpy as np
import json
from pathlib import Path
from datetime import datetime

input_dir = Path("data/processed")
output_dir = Path("data/processed/cleaned")
output_dir.mkdir(parents=True, exist_ok=True)

cleaning_log = []

def log_action(action, details):
    cleaning_log.append({
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "details": details
    })
    print(f"  {action}: {details}")

def handle_missing_values(df, dataset_name):
    print(f"handling missing values for {dataset_name}...")
    
    initial_missing = df.isna().sum().sum()
    
    threshold = len(df.columns) * 0.5
    rows_before = len(df)
    df = df.dropna(thresh=threshold)
    rows_removed = rows_before - len(df)
    
    if rows_removed > 0:
        log_action("removed rows with excessive missing", f"{rows_removed} rows")
    
    if 'date' in df.columns or 'year' in df.columns:
        time_cols = ['year', 'month'] if 'year' in df.columns else []
        if time_cols:
            df = df.sort_values(time_cols)
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            
            for col in numeric_cols:
                missing_before = df[col].isna().sum()
                if missing_before > 0:
                    if 'city' in df.columns:
                        df[col] = df.groupby('city')[col].fillna(method='ffill')
                    else:
                        df[col] = df[col].fillna(method='ffill')
                    missing_after = df[col].isna().sum()
                    if missing_after < missing_before:
                        log_action(f"forward filled {col}", f"{missing_before - missing_after} values")
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        missing_count = df[col].isna().sum()
        if missing_count > 0:
            if 'city' in df.columns:
                df[col] = df.groupby('city')[col].transform(lambda x: x.fillna(x.median()))
            else:
                df[col].fillna(df[col].median(), inplace=True)
            log_action(f"filled {col} with median", f"{missing_count} values")
    
    final_missing = df.isna().sum().sum()
    print(f"  reduced missing from {initial_missing} to {final_missing}")
    
    return df

def remove_duplicates(df):
    rows_before = len(df)
    df = df.drop_duplicates()
    rows_removed = rows_before - len(df)
    
    if rows_removed > 0:
        log_action("removed duplicates", f"{rows_removed} rows")
    
    return df

def handle_outliers(df):
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    exclude_cols = ['year', 'month']
    treatment_cols = [col for col in numeric_cols if col not in exclude_cols]
    
    for col in treatment_cols:
        lower_bound = df[col].quantile(0.01)
        upper_bound = df[col].quantile(0.99)
        
        outliers_low = (df[col] < lower_bound).sum()
        outliers_high = (df[col] > upper_bound).sum()
        
        if outliers_low > 0 or outliers_high > 0:
            df[col] = df[col].clip(lower=lower_bound, upper=upper_bound)
            log_action(f"winsorized {col}", f"{outliers_low} low, {outliers_high} high")
    
    return df

def standardize_formats(df):
    if 'year' in df.columns:
        df['year'] = df['year'].astype(int)
    
    if 'month' in df.columns:
        df['month'] = df['month'].astype(int)
    
    if 'city' in df.columns:
        df['city'] = df['city'].str.title().str.strip()
        log_action("standardized city names", "converted to title case")
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if col not in ['year', 'month']:
            df[col] = df[col].round(2)
    
    return df

def validate_ranges(df):
    if 'year' in df.columns:
        invalid_years = df[~df['year'].between(2013, 2022)]
        if len(invalid_years) > 0:
            df = df[df['year'].between(2013, 2022)]
            log_action("removed invalid years", f"{len(invalid_years)} records")
    
    if 'month' in df.columns:
        invalid_months = df[~df['month'].between(1, 12)]
        if len(invalid_months) > 0:
            df = df[df['month'].between(1, 12)]
            log_action("removed invalid months", f"{len(invalid_months)} records")
    
    return df

def clean_dataset(filepath, dataset_name):
    print(f"cleaning {dataset_name}...")
    
    df = pd.read_csv(filepath)
    print(f"loaded {len(df)} records")
    
    df = remove_duplicates(df)
    df = validate_ranges(df)
    df = handle_missing_values(df, dataset_name)
    df = handle_outliers(df)
    df = standardize_formats(df)
    
    output_file = output_dir / f"{dataset_name}_cleaned.csv"
    df.to_csv(output_file, index=False)
    print(f"saved to {output_file}, final count: {len(df)}")
    
    return df

datasets = {
    "weather": input_dir / "weather_monthly.csv",
    "retail": input_dir / "retail_sales.csv"
}

for name, filepath in datasets.items():
    if filepath.exists():
        clean_dataset(filepath, name)

log_file = output_dir / "cleaning_log.json"
with open(log_file, 'w') as f:
    json.dump(cleaning_log, f, indent=2)

print(f"\ndone! log saved to {log_file}")
