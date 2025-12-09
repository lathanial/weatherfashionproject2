import pandas as pd
import json
from pathlib import Path
from datetime import datetime

noaa_dir = Path("data/raw/noaa")
census_dir = Path("data/raw/census")
output_dir = Path("data/processed")
output_dir.mkdir(parents=True, exist_ok=True)

def get_season(m):
    if m in [12, 1, 2]:
        return "Winter"
    elif m in [3, 4, 5]:
        return "Spring"
    elif m in [6, 7, 8]:
        return "Summer"
    else:
        return "Fall"

print("loading weather data...")

all_weather = []

for f in noaa_dir.glob("*_weather.json"):
    city = f.stem.replace("_weather", "").replace("_", " ").title()
    with open(f, "r") as file:
        data = json.load(file)

    df = pd.DataFrame(data)
    
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['season'] = df['month'].apply(get_season)
    
    df = df.pivot_table(
        index=['city', 'year', 'month', 'season', 'date'], 
        columns='datatype', 
        values='value'
    ).reset_index()
    
    all_weather.append(df)

weather_df = pd.concat(all_weather, ignore_index=True)
print(f"weather loaded: {len(weather_df)} records")

normals = (
    weather_df.groupby(["city", "month"])
    .agg({"TMAX": "mean", "TMIN": "mean", "PRCP": "mean"})
    .reset_index()
)
normals.columns = ["city", "month", "TMAX_normal", "TMIN_normal", "PRCP_normal"]

weather_df = weather_df.merge(normals, on=["city", "month"], how="left")

weather_df["TMAX_anomaly"] = weather_df["TMAX"] - weather_df["TMAX_normal"]
weather_df["TMIN_anomaly"] = weather_df["TMIN"] - weather_df["TMIN_normal"]
weather_df["PRCP_anomaly"] = weather_df["PRCP"] - weather_df["PRCP_normal"]

monthly_weather = (
    weather_df.groupby(["city", "year", "month", "season"])
    .agg({
        "TMAX": ["mean", "max", "std"],
        "TMIN": ["mean", "min", "std"],
        "PRCP": "sum",
        "SNOW": "sum",
        "AWND": "mean",
        "TMAX_anomaly": "mean",
        "TMIN_anomaly": "mean",
        "PRCP_anomaly": "sum"
    })
    .reset_index()
)

monthly_weather.columns = [
    "_".join(col).strip("_") if col[1] else col[0]
    for col in monthly_weather.columns
]

weather_output = output_dir / "weather_monthly.csv"
monthly_weather.to_csv(weather_output, index=False)
print("saved monthly weather")

dfs = []

monthly_file = census_dir / "mock_census_monthly.csv"
annual_file = census_dir / "mock_census_annual.csv"
real_monthly = census_dir / "monthly_retail_sales.csv"

if real_monthly.exists():
    m = pd.read_csv(real_monthly)
    m["frequency"] = "monthly"
    dfs.append(m)
    print("loaded real census monthly data")
elif monthly_file.exists():
    m = pd.read_csv(monthly_file)
    m["frequency"] = "monthly"
    dfs.append(m)
    print("loaded mock census monthly data")

if annual_file.exists():
    a = pd.read_csv(annual_file)
    a["frequency"] = "annual"
    dfs.append(a)
    print("loaded mock census annual data")

if dfs:
    census_df = pd.concat(dfs, ignore_index=True)
    census_output = output_dir / "retail_sales.csv"
    census_df.to_csv(census_output, index=False)
    print(f"saved census data: {len(census_df)} records")
else:
    census_df = pd.DataFrame()
    print("no census files found")

metadata = {
    "integration_date": datetime.now().isoformat(),
    "weather_records": len(monthly_weather),
    "retail_records": len(census_df),
    "cities": monthly_weather["city"].unique().tolist(),
    "date_range": {
        "start": int(monthly_weather["year"].min()),
        "end": int(monthly_weather["year"].max())
    }
}

with open(output_dir / "integration_metadata.json", "w") as f:
    json.dump(metadata, f, indent=2)

print("done")