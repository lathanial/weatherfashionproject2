import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
from pathlib import Path
from datetime import datetime

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

data_dir = Path("data/processed/cleaned")
output_dir = Path("data/output")
output_dir.mkdir(parents=True, exist_ok=True)

print("loading data...")
weather_df = pd.read_csv(data_dir / "weather_cleaned.csv")
print(f"loaded {len(weather_df)} weather records")

retail_file = data_dir / "retail_cleaned.csv"
if retail_file.exists():
    retail_df = pd.read_csv(retail_file)
    print(f"loaded {len(retail_df)} retail records")

available_cols = weather_df.columns.tolist()
print(f"available columns: {available_cols}")

print("analyzing temperature trends...")
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

if 'season' in weather_df.columns and 'TMAX_mean' in weather_df.columns:
    sns.boxplot(data=weather_df, x='season', y='TMAX_mean', ax=axes[0, 0])
    axes[0, 0].set_title('Maximum Temperature by Season')
    axes[0, 0].set_ylabel('Temperature (°C)')

if 'city' in weather_df.columns and 'TMAX_mean' in weather_df.columns:
    sns.boxplot(data=weather_df, x='city', y='TMAX_mean', ax=axes[0, 1])
    axes[0, 1].set_title('Maximum Temperature by City')
    axes[0, 1].set_ylabel('Temperature (°C)')
    axes[0, 1].tick_params(axis='x', rotation=45)

if 'year' in weather_df.columns and 'TMAX_mean' in weather_df.columns:
    yearly_temp = weather_df.groupby('year')['TMAX_mean'].mean()
    axes[1, 0].plot(yearly_temp.index, yearly_temp.values, marker='o')
    axes[1, 0].set_title('Average Maximum Temperature Trend')
    axes[1, 0].set_xlabel('Year')
    axes[1, 0].set_ylabel('Temperature (°C)')

if 'month' in weather_df.columns and 'TMAX_mean' in weather_df.columns:
    monthly_temp = weather_df.groupby('month')['TMAX_mean'].mean()
    axes[1, 1].plot(monthly_temp.index, monthly_temp.values, marker='o')
    axes[1, 1].set_title('Average Temperature by Month')
    axes[1, 1].set_xlabel('Month')
    axes[1, 1].set_ylabel('Temperature (°C)')
    axes[1, 1].set_xticks(range(1, 13))

plt.tight_layout()
plt.savefig(output_dir / 'temperature_analysis.png', dpi=300, bbox_inches='tight')
plt.close()
print("saved temperature analysis")

print("analyzing precipitation...")
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

if 'season' in weather_df.columns and 'PRCP_sum' in weather_df.columns:
    sns.boxplot(data=weather_df, x='season', y='PRCP_sum', ax=axes[0, 0])
    axes[0, 0].set_title('Precipitation by Season')
    axes[0, 0].set_ylabel('Precipitation (mm)')

if 'city' in weather_df.columns and 'PRCP_sum' in weather_df.columns:
    sns.boxplot(data=weather_df, x='city', y='PRCP_sum', ax=axes[0, 1])
    axes[0, 1].set_title('Precipitation by City')
    axes[0, 1].set_ylabel('Precipitation (mm)')
    axes[0, 1].tick_params(axis='x', rotation=45)

if 'SNOW_sum' in weather_df.columns and 'season' in weather_df.columns:
    sns.boxplot(data=weather_df, x='season', y='SNOW_sum', ax=axes[1, 0])
    axes[1, 0].set_title('Snowfall by Season')
    axes[1, 0].set_ylabel('Snowfall (mm)')

if 'year' in weather_df.columns and 'PRCP_sum' in weather_df.columns:
    yearly_precip = weather_df.groupby('year')['PRCP_sum'].mean()
    axes[1, 1].plot(yearly_precip.index, yearly_precip.values, marker='o')
    axes[1, 1].set_title('Average Precipitation Trend')
    axes[1, 1].set_xlabel('Year')
    axes[1, 1].set_ylabel('Precipitation (mm)')

plt.tight_layout()
plt.savefig(output_dir / 'precipitation_analysis.png', dpi=300, bbox_inches='tight')
plt.close()
print("saved precipitation analysis")

print("analyzing extreme weather...")
if 'TMAX_mean' in weather_df.columns:
    temp_threshold = weather_df['TMAX_mean'].quantile(0.95)
    extreme_heat = weather_df[weather_df['TMAX_mean'] > temp_threshold]
    print(f"  extreme heat events: {len(extreme_heat)}")

if 'TMIN_mean' in weather_df.columns:
    cold_threshold = weather_df['TMIN_mean'].quantile(0.05)
    extreme_cold = weather_df[weather_df['TMIN_mean'] < cold_threshold]
    print(f"  extreme cold events: {len(extreme_cold)}")

if 'PRCP_sum' in weather_df.columns:
    precip_threshold = weather_df['PRCP_sum'].quantile(0.95)
    extreme_precip = weather_df[weather_df['PRCP_sum'] > precip_threshold]
    print(f"  extreme precip events: {len(extreme_precip)}")

fig, axes = plt.subplots(1, 3, figsize=(18, 6))

if 'city' in weather_df.columns and 'TMAX_mean' in weather_df.columns:
    extreme_heat.groupby('city').size().plot(kind='bar', ax=axes[0])
    axes[0].set_title('Extreme Heat Events by City')
    axes[0].set_ylabel('Number of Events')
    axes[0].tick_params(axis='x', rotation=45)

if 'city' in weather_df.columns and 'TMIN_mean' in weather_df.columns:
    extreme_cold.groupby('city').size().plot(kind='bar', ax=axes[1])
    axes[1].set_title('Extreme Cold Events by City')
    axes[1].set_ylabel('Number of Events')
    axes[1].tick_params(axis='x', rotation=45)

if 'city' in weather_df.columns and 'PRCP_sum' in weather_df.columns:
    extreme_precip.groupby('city').size().plot(kind='bar', ax=axes[2])
    axes[2].set_title('Extreme Precipitation Events by City')
    axes[2].set_ylabel('Number of Events')
    axes[2].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig(output_dir / 'extreme_weather_analysis.png', dpi=300, bbox_inches='tight')
plt.close()
print("saved extreme weather analysis")

print("analyzing correlations...")
weather_vars = ['TMAX_mean', 'TMIN_mean', 'PRCP_sum']
available_vars = [var for var in weather_vars if var in weather_df.columns]
if available_vars:
    corr_data = weather_df[available_vars]
    corr_matrix = corr_data.corr()

    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, fmt='.2f', square=True, linewidths=1)
    plt.title('Weather Variables Correlation Matrix')
    plt.tight_layout()
    plt.savefig(output_dir / 'correlation_matrix.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("saved correlation matrix")

print("seasonal comparison...")
if 'season' in weather_df.columns and 'TMAX_mean' in weather_df.columns and 'TMIN_mean' in weather_df.columns:
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    season_order = ['Winter', 'Spring', 'Summer', 'Fall']
    for season in season_order:
        if season in weather_df['season'].values:
            season_data = weather_df[weather_df['season'] == season]
            axes[0, 0].scatter(season_data['TMIN_mean'], season_data['TMAX_mean'], alpha=0.3, label=season)
    axes[0, 0].set_xlabel('Minimum Temperature (°C)')
    axes[0, 0].set_ylabel('Maximum Temperature (°C)')
    axes[0, 0].set_title('Temperature Range by Season')
    axes[0, 0].legend()

    if 'year' in weather_df.columns:
        for season in season_order:
            if season in weather_df['season'].values:
                season_data = weather_df[weather_df['season'] == season]
                yearly_avg = season_data.groupby('year')['TMAX_mean'].mean()
                axes[0, 1].plot(yearly_avg.index, yearly_avg.values, marker='o', label=season)
        axes[0, 1].set_xlabel('Year')
        axes[0, 1].set_ylabel('Average Max Temperature (°C)')
        axes[0, 1].set_title('Seasonal Temperature Trends')
        axes[0, 1].legend()

    if 'PRCP_sum' in weather_df.columns and 'year' in weather_df.columns:
        seasonal_precip = weather_df.groupby(['year', 'season'])['PRCP_sum'].mean().unstack()
        seasonal_precip.plot(ax=axes[1, 0], marker='o')
        axes[1, 0].set_xlabel('Year')
        axes[1, 0].set_ylabel('Average Precipitation (mm)')
        axes[1, 0].set_title('Seasonal Precipitation Trends')
        axes[1, 0].legend(title='Season')

    if 'city' in weather_df.columns:
        city_seasonal = weather_df.groupby(['city', 'season'])['TMAX_mean'].mean().unstack()
        city_seasonal.plot(kind='bar', ax=axes[1, 1])
        axes[1, 1].set_xlabel('City')
        axes[1, 1].set_ylabel('Average Max Temperature (°C)')
        axes[1, 1].set_title('Temperature by City and Season')
        axes[1, 1].legend(title='Season')
        axes[1, 1].tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.savefig(output_dir / 'seasonal_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("saved seasonal comparison")

print("generating summary...")
summary = {
    "analysis_date": datetime.now().isoformat(),
    "data_summary": {
        "total_records": int(len(weather_df)),
        "cities": weather_df['city'].unique().tolist() if 'city' in weather_df.columns else [],
        "years": {
            "min": int(weather_df['year'].min()) if 'year' in weather_df.columns else None,
            "max": int(weather_df['year'].max()) if 'year' in weather_df.columns else None
        }
    }
}

if 'TMAX_mean' in weather_df.columns:
    summary["temperature_summary"] = {
        "overall_avg_max": float(weather_df['TMAX_mean'].mean()),
        "overall_avg_min": float(weather_df['TMIN_mean'].mean()) if 'TMIN_mean' in weather_df.columns else None,
    }
    if 'city' in weather_df.columns:
        summary["temperature_summary"]["warmest_city"] = weather_df.groupby('city')['TMAX_mean'].mean().idxmax()
        if 'TMIN_mean' in weather_df.columns:
            summary["temperature_summary"]["coldest_city"] = weather_df.groupby('city')['TMIN_mean'].mean().idxmin()

if 'PRCP_sum' in weather_df.columns:
    summary["precipitation_summary"] = {
        "overall_avg": float(weather_df['PRCP_sum'].mean())
    }
    if 'city' in weather_df.columns:
        summary["precipitation_summary"]["wettest_city"] = weather_df.groupby('city')['PRCP_sum'].mean().idxmax()
        summary["precipitation_summary"]["driest_city"] = weather_df.groupby('city')['PRCP_sum'].mean().idxmin()

if available_vars:
    summary["correlations"] = corr_matrix.to_dict()

summary_file = output_dir / "analysis_summary.json"
with open(summary_file, 'w') as f:
    json.dump(summary, f, indent=2)

print(f"\ndone! results saved to {output_dir}")