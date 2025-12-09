# Data Dictionary

## Weather Data (weather_monthly.csv, weather_cleaned.csv)

### Identifier Variables

| Variable | Type | Description | Example | Notes |
|----------|------|-------------|---------|-------|
| city | string | Metropolitan area name | "New York" | One of 8 metropolitan areas |
| year | integer | Year of observation | 2015 | Range: 2013-2022 |
| month | integer | Month of observation | 7 | Range: 1-12 |
| season | string | Meteorological season | "Summer" | Winter/Spring/Summer/Fall |

### Temperature Variables

| Variable | Type | Units | Description | Example | Notes |
|----------|------|-------|-------------|---------|-------|
| TMAX_mean | float | °C | Mean monthly maximum temperature | 28.5 | Averaged across all days in month |
| TMAX_max | float | °C | Highest maximum temperature in month | 35.2 | Single day maximum |
| TMAX_std | float | °C | Standard deviation of max temperatures | 3.1 | Measure of variability |
| TMIN_mean | float | °C | Mean monthly minimum temperature | 18.3 | Averaged across all days in month |
| TMIN_min | float | °C | Lowest minimum temperature in month | 12.1 | Single day minimum |
| TMIN_std | float | °C | Standard deviation of min temperatures | 2.8 | Measure of variability |
| TMAX_normal | float | °C | 10-year average max temperature for this month | 27.8 | Baseline for anomaly calculation |
| TMIN_normal | float | °C | 10-year average min temperature for this month | 17.9 | Baseline for anomaly calculation |
| TMAX_anomaly | float | °C | Deviation from normal maximum temperature | +0.7 | Positive = warmer than normal |
| TMIN_anomaly | float | °C | Deviation from normal minimum temperature | +0.4 | Negative = cooler than normal |

### Precipitation Variables

| Variable | Type | Units | Description | Example | Notes |
|----------|------|-------|-------------|---------|-------|
| PRCP_sum | float | mm | Total monthly precipitation | 94.3 | Sum of all daily precipitation |
| PRCP_normal | float | mm | 10-year average monthly precipitation | 87.2 | Baseline for anomaly calculation |
| PRCP_anomaly | float | mm | Deviation from normal precipitation | +7.1 | Positive = wetter than normal |
| SNOW_sum | float | mm | Total monthly snowfall | 152.4 | Sum of all daily snowfall; often 0 in warm climates |

### Wind Variables

| Variable | Type | Units | Description | Example | Notes |
|----------|------|-------|-------------|---------|-------|
| AWND_mean | float | m/s | Average monthly wind speed | 4.2 | Mean of daily average wind speeds |

### Data Quality Indicators

Missing values in the cleaned dataset have been imputed using forward-fill for time series continuity and median imputation for remaining gaps. Original missing value counts are documented in the quality assessment report.

## Retail Sales Data (retail_sales.csv, retail_cleaned.csv)

### Identifier Variables

| Variable | Type | Description | Example | Notes |
|----------|------|-------------|---------|-------|
| NAICS | string | NAICS industry code | "4481" | Clothing and accessories stores |
| NAICS_TTL | string | NAICS industry description | "Clothing Stores" | Human-readable industry name |
| year | integer | Year of observation | 2018 | Range: 2013-2022 |
| frequency | string | Data frequency | "monthly" | "monthly" or "annual" |

### Monthly Retail Trade Survey (MRTS) Variables

| Variable | Type | Units | Description | Example | Notes |
|----------|------|-------|-------------|---------|-------|
| PER | string | Period code | "202301" | YYYYMM format for monthly data |
| PER_TTL | string | Period description | "January 2023" | Human-readable period |
| MRTSSALES | integer | Millions USD | Monthly retail sales | 18432 | National-level sales for specified NAICS code |

### Annual Retail Trade Survey (ARTS) Variables

| Variable | Type | Units | Description | Example | Notes |
|----------|------|-------|-------------|---------|-------|
| state | string | State FIPS code | "36" | Two-digit state identifier |
| NAICS2017 | string | 2017 NAICS code | "4481" | Industry classification |
| NAICS2017_TTL | string | Industry description | "Clothing Stores" | Human-readable name |
| ESTAB | integer | Count | Number of establishments | 1245 | Stores in operation |
| RCPTOT | integer | Thousands USD | Total annual receipts | 1842300 | Annual revenue for state |
| PAYANN | integer | Thousands USD | Annual payroll | 324100 | Total wages paid |

### Special Values and Suppression

- `D`: Withheld to avoid disclosing data for individual companies (Census confidentiality)
- `N`: Not available or not applicable
- `S`: Withheld because estimate did not meet publication standards

These suppressed values have been treated as missing and handled according to the cleaning procedures documented in README.md.

## Processed/Integrated Data Conventions

### Date Handling

- All dates are in ISO 8601 format (YYYY-MM-DD) where applicable
- Months are represented as integers (1-12)
- Years are four-digit integers

### Geographic Identifiers

**Metropolitan Areas Analyzed**:
1. New York-Newark-Jersey City, NY-NJ-PA
2. Los Angeles-Long Beach-Anaheim, CA
3. Chicago-Naperville-Elgin, IL-IN-WI
4. Houston-The Woodlands-Sugar Land, TX
5. Phoenix-Mesa-Scottsdale, AZ
6. Philadelphia-Camden-Wilmington, PA-NJ-DE-MD
7. San Antonio-New Braunfels, TX
8. San Diego-Carlsbad, CA

**State Codes** (used in retail data):
- 36: New York
- 06: California
- 17: Illinois
- 48: Texas
- 04: Arizona
- 42: Pennsylvania

### Seasons

Meteorological seasons are defined as:
- **Winter**: December, January, February (months 12, 1, 2)
- **Spring**: March, April, May (months 3, 4, 5)
- **Summer**: June, July, August (months 6, 7, 8)
- **Fall**: September, October, November (months 9, 10, 11)

### Units

All measurements use metric units:
- Temperature: Degrees Celsius (°C)
- Precipitation: Millimeters (mm)
- Wind speed: Meters per second (m/s)
- Monetary values: U.S. Dollars (USD) in millions or thousands as specified

### Missing Data

In cleaned datasets:
- Numeric missing values have been imputed (see README.md for methodology)
- Original missing value patterns are documented in `data/output/quality_assessment_report.json`
- Missing data in raw datasets are indicated by `NaN` in CSV files

### Outliers

- Extreme weather values are retained as scientifically valid observations
- Statistical outliers beyond 1st/99th percentiles are winsorized (capped) only for derived aggregate statistics
- Original extreme values are preserved in cleaned datasets for transparency

## File Naming Conventions

### Raw Data Files

Format: `{source}_{type}_{content}.{extension}`

Examples:
- `new_york_weather.json` - Weather data for New York from NOAA
- `monthly_retail_sales.csv` - Monthly retail sales from Census Bureau
- `collection_metadata.json` - Metadata about data collection process

### Processed Data Files

Format: `{content}_{processing_stage}.{extension}`

Examples:
- `weather_monthly.csv` - Weather data aggregated to monthly level
- `weather_cleaned.csv` - Weather data after cleaning procedures
- `integration_metadata.json` - Metadata about data integration

### Output Files

Format: `{analysis_type}_{description}.{extension}`

Examples:
- `temperature_analysis.png` - Visualization of temperature patterns
- `quality_assessment_report.json` - Detailed quality metrics
- `analysis_summary.json` - Summary of analysis findings

## Data Provenance

### Weather Data

- **Original Source**: NOAA Climate Data Online API
- **Dataset**: Global Historical Climatology Network - Daily (GHCND)
- **Collection Date**: [Documented in collection_metadata.json]
- **Processing Steps**:
  1. API retrieval with rate limiting
  2. JSON to tabular conversion
  3. Daily to monthly aggregation
  4. Calculation of anomalies vs. 10-year normals
  5. Quality assessment
  6. Cleaning and imputation

### Retail Sales Data

- **Original Source**: U.S. Census Bureau API
- **Datasets**: MRTS and ARTS
- **Collection Date**: [Documented in collection_metadata.json]
- **Processing Steps**:
  1. API retrieval for multiple years
  2. Combination of monthly and annual datasets
  3. Handling of suppressed values
  4. Quality assessment
  5. Cleaning and standardization

## Versioning

- **Data Dictionary Version**: 1.0
- **Last Updated**: December 2025
- **Corresponds to**: Final project submission
- **Changelog**: Initial release

## Contact

For questions about this data dictionary or the underlying datasets, please contact Lynn or open an issue on the GitHub repository.
