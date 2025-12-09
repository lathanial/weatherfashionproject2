import pandas as pd
import numpy as np
import json
from pathlib import Path
from datetime import datetime

data_dir = Path("data/processed")
output_dir = Path("data/output")
output_dir.mkdir(parents=True, exist_ok=True)

def assess_completeness(df):
    total_cells = df.size
    missing_cells = df.isna().sum().sum()
    completeness_pct = ((total_cells - missing_cells) / total_cells) * 100
    
    missing_by_column = df.isna().sum()
    missing_pct_by_column = (missing_by_column / len(df)) * 100
    
    return {
        "total_cells": int(total_cells),
        "missing_cells": int(missing_cells),
        "completeness_percentage": float(completeness_pct),
        "columns_with_missing": {
            col: {"count": int(count), "percentage": float(pct)}
            for col, count, pct in zip(missing_by_column.index, missing_by_column.values, missing_pct_by_column.values)
            if count > 0
        }
    }

def assess_consistency(df):
    duplicate_rows = df.duplicated().sum()
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    negative_issues = {}
    
    for col in numeric_cols:
        if (df[col] < 0).any():
            negative_count = (df[col] < 0).sum()
            negative_issues[col] = int(negative_count)
    
    return {
        "duplicate_rows": int(duplicate_rows),
        "columns_with_negatives": negative_issues
    }

def assess_accuracy(df):
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    outliers = {}
    
    for col in numeric_cols:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        
        lower_bound = q1 - 3 * iqr
        upper_bound = q3 + 3 * iqr
        
        outlier_count = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()
        
        if outlier_count > 0:
            outliers[col] = {
                "count": int(outlier_count),
                "percentage": float((outlier_count / len(df)) * 100),
                "range": {
                    "min": float(df[col].min()),
                    "max": float(df[col].max()),
                    "expected_min": float(lower_bound),
                    "expected_max": float(upper_bound)
                }
            }
    
    return {"outliers_by_column": outliers}

def assess_validity(df):
    validity_issues = {}
    
    if 'year' in df.columns:
        min_year = df['year'].min()
        max_year = df['year'].max()
        if min_year < 2013 or max_year > 2022:
            validity_issues['year_range'] = {
                "expected": "2013-2022",
                "actual": f"{min_year}-{max_year}"
            }
    
    if 'month' in df.columns:
        invalid_months = df[~df['month'].between(1, 12)]
        if len(invalid_months) > 0:
            validity_issues['invalid_months'] = int(len(invalid_months))
    
    return {"constraint_violations": validity_issues}

def assess_dataset(filepath, dataset_name):
    print(f"assessing {dataset_name}...")
    
    df = pd.read_csv(filepath)
    
    numeric_summary = df.describe().to_dict()
    for col in numeric_summary:
        for stat in numeric_summary[col]:
            if isinstance(numeric_summary[col][stat], (np.integer, np.floating)):
                numeric_summary[col][stat] = float(numeric_summary[col][stat])
    
    report = {
        "dataset": dataset_name,
        "filepath": str(filepath),
        "assessment_date": datetime.now().isoformat(),
        "summary": {
            "record_count": int(len(df)),
            "column_count": int(len(df.columns)),
            "numeric_summary": numeric_summary
        },
        "completeness": assess_completeness(df),
        "consistency": assess_consistency(df),
        "accuracy": assess_accuracy(df),
        "validity": assess_validity(df)
    }
    
    print(f"  completeness: {report['completeness']['completeness_percentage']:.2f}%")
    print(f"  duplicates: {report['consistency']['duplicate_rows']}")
    
    return report

datasets = {
    "weather": data_dir / "weather_monthly.csv",
    "retail": data_dir / "retail_sales.csv"
}

all_reports = {}

for name, filepath in datasets.items():
    if filepath.exists():
        report = assess_dataset(filepath, name)
        all_reports[name] = report

report_file = output_dir / "quality_assessment_report.json"
with open(report_file, 'w') as f:
    json.dump(all_reports, f, indent=2)

summary_file = output_dir / "quality_summary.txt"
with open(summary_file, 'w') as f:
    f.write("DATA QUALITY ASSESSMENT SUMMARY\n")
    f.write("=" * 60 + "\n\n")
    
    for dataset_name, report in all_reports.items():
        f.write(f"{dataset_name.upper()} DATASET\n")
        f.write("-" * 60 + "\n")
        
        summary = report['summary']
        f.write(f"Records: {summary['record_count']:,}\n")
        f.write(f"Columns: {summary['column_count']}\n\n")
        
        completeness = report['completeness']
        f.write(f"Completeness: {completeness['completeness_percentage']:.2f}%\n")
        f.write(f"Missing cells: {completeness['missing_cells']:,}\n")
        
        if completeness['columns_with_missing']:
            f.write("\nColumns with missing values:\n")
            for col, info in completeness['columns_with_missing'].items():
                f.write(f"  - {col}: {info['count']} ({info['percentage']:.2f}%)\n")
        
        consistency = report['consistency']
        f.write(f"\nDuplicate rows: {consistency['duplicate_rows']}\n")
        
        accuracy = report['accuracy']
        outlier_cols = accuracy['outliers_by_column']
        f.write(f"\nColumns with outliers: {len(outlier_cols)}\n")
        
        f.write("\n" + "=" * 60 + "\n\n")

print(f"\ndone! saved reports to {output_dir}")