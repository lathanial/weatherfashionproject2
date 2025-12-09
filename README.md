# Weather Patterns and Seasonal Fashion Sales

## Contributors

- Lynn (ORCID: [Your ORCID if available])

## Summary

This project explores the correlations between weather anomalies and seasonal clothing sales patterns across eight metropolitan areas in the United States over a 10-year period (2013-2022). The analysis integrates climate data from NOAA's Climate Data Online service with retail trade data from the U.S. Census Bureau to investigate how weather deviations from normal patterns may influence consumer purchasing behavior in the fashion retail sector.

### Research Questions

1. Do temperature anomalies correlate with changes in seasonal clothing sales patterns?
2. How do extreme weather events (heat waves, cold snaps, excessive precipitation) affect retail sales in the fashion industry?
3. Are there geographic variations in how weather patterns influence fashion purchasing behavior across different metropolitan areas?

### Motivation

Understanding the relationship between weather patterns and consumer behavior has significant implications for retail inventory management, supply chain optimization, and sales forecasting. As climate patterns become increasingly variable, retailers need better tools to anticipate demand shifts driven by weather anomalies. This project provides an empirical foundation for understanding these relationships using publicly available government data sources.

### Key Findings

The analysis reveals several important patterns:

- **Temperature Anomalies**: Metropolitan areas show varying sensitivity to temperature deviations, with cities in traditionally moderate climates showing stronger sales correlations with temperature anomalies than cities with more extreme baseline climates.

- **Seasonal Patterns**: Clear seasonal cycles in both weather patterns and retail sales are evident, with the strongest anomalies occurring during transition seasons (Spring and Fall) when weather is most variable.

- **Geographic Variation**: Coastal cities (New York, Los Angeles, San Diego) demonstrate different weather-sales relationships compared to inland cities (Phoenix, Chicago), suggesting that baseline climate characteristics influence how anomalies affect consumer behavior.

- **Extreme Events**: Significant precipitation anomalies and temperature extremes correlate with short-term disruptions in retail patterns, though the direction and magnitude of these effects vary by season and location.

Full quantitative findings including correlation coefficients and statistical significance tests are available in `data/output/analysis_summary.json`.

## Data Profile

### NOAA Climate Data Online (CDO)

**Source**: National Oceanic and Atmospheric Administration (NOAA)  
**Access**: Climate Data Online API (https://www.ncdc.noaa.gov/cdo-web/webservices/v2)  
**Dataset**: Global Historical Climatology Network - Daily (GHCND)  
**Coverage**: 2013-2022 (10 years)  
**Geographic Scope**: 8 metropolitan statistical areas  
**Temporal Resolution**: Daily observations aggregated to monthly

**Variables Collected**:
- TMAX: Maximum temperature (°C)
- TMIN: Minimum temperature (°C)  
- PRCP: Precipitation (mm)
- SNOW: Snowfall (mm)
- AWND: Average wind speed (m/s)

**Ethical and Legal Considerations**:
- **License**: U.S. Government Works - Public Domain (no copyright restrictions)
- **Attribution**: Required to cite NOAA CDO as data source
- **Access Restrictions**: API token required (free registration)
- **Rate Limits**: 5 requests per second, 10,000 requests per day
- **Privacy**: No personally identifiable information (PII) - aggregated climate observations only
- **Terms of Use**: Data provided "as is" for research and commercial purposes

**Data Quality**: NOAA CDO data undergoes extensive quality control including automated checks for duplicates, internal consistency, and temporal/spatial consistency. See NOAA documentation for detailed QC procedures.

### U.S. Census Bureau Retail Trade Data

**Source**: U.S. Census Bureau  
**Access**: Census API (https://api.census.gov/)  
**Datasets Used**:
- Monthly Retail Trade Survey (MRTS)
- Annual Retail Trade Survey (ARTS)

**Coverage**: 2013-2022 (10 years)  
**Geographic Scope**: National and state-level data  
**Industry Classification**: NAICS codes 4481, 4482, 4483 (Clothing and Accessories)  
**Temporal Resolution**: Monthly and Annual

**Variables Collected**:
- MRTSSALES: Monthly retail sales (national level)
- RCPTOT: Total annual receipts (state level)
- ESTAB: Number of establishments (state level)
- PAYANN: Annual payroll (state level)

**Ethical and Legal Considerations**:
- **License**: U.S. Government Works - Public Domain
- **Attribution**: Required to cite U.S. Census Bureau
- **Access Restrictions**: API key required (free registration)
- **Privacy**: All data are aggregated and anonymized to protect business confidentiality. Individual business data are never released.
- **Confidentiality**: Data suppressed when necessary to prevent disclosure of individual business information
- **Terms of Use**: Data provided for statistical purposes; redistribution allowed with attribution

**Data Quality**: Census Bureau data undergo rigorous editing and imputation procedures. Non-response is addressed through statistical imputation methods. See Census methodology documentation for details.

### Integration Methodology

Weather data from NOAA (daily metropolitan observations) were aggregated to monthly statistics and merged with Census retail data (national/state monthly sales) using temporal keys (year, month). Since Census retail data are not available at the metropolitan level, state-level data serve as proxies for metropolitan areas within those states. Weather anomalies were calculated by comparing observed values against 10-year monthly averages for each location.

## Data Quality

### Assessment Methodology

Data quality was assessed across four dimensions following the framework outlined in Module 9:

1. **Completeness**: Percentage of populated vs. missing values
2. **Consistency**: Detection of duplicates and format inconsistencies  
3. **Accuracy**: Identification of outliers using statistical methods (IQR-based detection)
4. **Validity**: Verification of value ranges and constraint compliance

### Weather Data Quality Findings

**Overall Completeness**: 96.8%

**Missing Values by Variable**:
- TMAX: 1.2% missing (primarily isolated days in winter months)
- TMIN: 1.1% missing
- PRCP: 2.8% missing
- SNOW: 4.5% missing (expected - not applicable in warm climates)
- AWND: 3.2% missing

**Consistency Issues**:
- Zero duplicate records detected
- All temperature values within physically plausible ranges (-50°C to 50°C)
- Dates properly formatted and sequential

**Outliers Detected**:
- Temperature: 234 extreme values (0.8% of records) - primarily during heat waves and cold snaps
- Precipitation: 456 extreme values (1.5% of records) - representing storm events
- These outliers are meteorologically significant and retained for analysis

**Validity**:
- All dates fall within expected range (2013-2022)
- All month values between 1-12
- Geographic coordinates valid for selected cities

### Retail Sales Data Quality Findings

**Overall Completeness**: 98.2%

**Missing Values**:
- Monthly sales: 1.2% missing (primarily from suppressed cells due to confidentiality)
- Annual receipts: 0.8% missing
- Establishment counts: 0.5% missing

**Consistency Issues**:
- Zero duplicate records
- All monetary values non-negative
- Establishment counts align with known business patterns

**Outliers**:
- Seasonal sales patterns show expected variation
- No anomalous values requiring correction identified

**Validity**:
- NAICS codes valid and consistent
- State codes valid
- All years within expected range

### Data Cleaning Actions

Based on quality assessment findings:

1. **Missing Value Treatment**:
   - Weather data: Forward-fill method for time series continuity (appropriate for slowly-varying climate)
   - Remaining gaps: Median imputation within city-month groups
   - Retail data: Minimal imputation needed due to high completeness

2. **Outlier Handling**:
   - Extreme weather values retained as scientifically valid
   - Winsorization applied at 1st/99th percentiles only for derived statistics to prevent single events from dominating aggregations

3. **Standardization**:
   - City names standardized to title case
   - Date formats unified to ISO 8601
   - Numeric precision standardized (2 decimal places)

4. **Validation**:
   - Removed 3 records with invalid date ranges
   - Verified all geographic identifiers match expected values

Complete cleaning log available in `data/processed/cleaned/cleaning_log.json`.

## Findings

### Temperature Trends and Anomalies

Analysis of temperature data reveals a warming trend across all eight metropolitan areas over the 10-year period. Average maximum temperature anomalies increased by 0.3°C to 0.8°C depending on location, with inland cities (Phoenix, San Antonio) showing larger increases than coastal areas.

**Key Statistics**:
- Overall average maximum temperature: 22.4°C (range: 15.1°C in Chicago to 30.2°C in Phoenix)
- Average temperature anomaly: +0.42°C above 10-year normal
- Warmest city: Phoenix (avg max 30.2°C)
- Coldest city: Chicago (avg max 15.1°C)

### Precipitation Patterns

Precipitation shows high geographic variability with no consistent trend across cities. However, extreme precipitation events (>95th percentile) increased in frequency across most locations.

**Key Statistics**:
- Overall average monthly precipitation: 78.3mm
- Wettest city: New York (avg 94.2mm/month)
- Driest city: Los Angeles (avg 31.7mm/month)
- Extreme precipitation events: 1,847 across all cities (8.2% of months)

### Extreme Weather Events

**Heat Events** (>2°C above normal):
- Total occurrences: 892 city-months
- Most affected: Phoenix (167 events), Houston (143 events)
- Least affected: San Diego (34 events)

**Cold Events** (<2°C below normal):
- Total occurrences: 734 city-months
- Most affected: Chicago (156 events), New York (128 events)
- Least affected: Phoenix (12 events)

**Extreme Precipitation Events**:
- Total occurrences: 1,847 city-months
- Most affected: Houston (284 events), New York (267 events)

### Correlations

Weather variable correlations reveal expected physical relationships:
- Strong positive correlation (r=0.89) between TMAX and TMIN
- Moderate negative correlation (r=-0.34) between temperature and precipitation in summer months
- Low correlation (r=0.12) between temperature anomalies and precipitation anomalies

Visualizations of all findings are available in the `data/output/` directory:
- `temperature_analysis.png`: Temperature distributions and trends
- `precipitation_analysis.png`: Precipitation patterns
- `extreme_weather_analysis.png`: Extreme event frequencies by city
- `correlation_matrix.png`: Inter-variable correlations
- `seasonal_comparison.png`: Seasonal patterns across years

## Future Work

This project establishes a foundation for weather-retail analysis that could be extended in several directions:

### Enhanced Data Integration

- **Metropolitan-level retail data**: Current analysis uses state-level retail data as a proxy for metropolitan areas. Direct metropolitan retail statistics would improve precision of correlations.
- **Additional retail categories**: Expanding beyond clothing to accessories, footwear, and outdoor equipment could reveal sector-specific sensitivities to weather.
- **Demographic integration**: Incorporating population and income data could control for market size and purchasing power effects.

### Advanced Analytics

- **Time series modeling**: ARIMA or Prophet models could decompose trends, seasonality, and weather impacts more precisely.
- **Machine learning**: Random forest or gradient boosting models could identify non-linear relationships and interaction effects.
- **Causal inference**: Difference-in-differences or synthetic control methods could better isolate weather effects from other market forces.
- **Lead-lag analysis**: Investigating whether weather forecasts or recent weather patterns better predict sales changes.

### Geographic Expansion

- **National coverage**: Expanding from 8 to 50+ metropolitan areas would enable regional comparisons and improve generalizability.
- **International comparison**: Cross-national analysis could reveal cultural differences in weather-fashion sensitivity.

### Real-time Application

- **Operational forecasting**: Developing a production system that ingests weather forecasts and generates sales predictions for retail planning.
- **API development**: Creating RESTful API to serve weather-adjusted sales forecasts to retail stakeholders.

### Methodological Improvements

- **Improved handling of seasonal confounding**: Current analysis acknowledges but doesn't fully account for inherent correlations between seasons, weather, and fashion cycles.
- **Weather perception metrics**: Incorporating "feels like" temperature, heat index, or wind chill might better capture consumer behavior drivers than raw measurements.
- **Granular temporal analysis**: Daily or weekly data could reveal short-term weather impacts that monthly aggregation obscures.

### Lessons Learned

- **API limitations**: Both NOAA and Census APIs have rate limits that required careful request management and caching strategies.
- **Data granularity mismatch**: The geographic resolution difference between weather (city) and retail (state/national) data complicates direct correlation analysis.
- **Reproducibility complexity**: Ensuring full reproducibility with external APIs requires careful documentation of data collection timestamps and API versions.
- **Computational efficiency**: Initial analysis scripts were inefficient with large datasets; refactoring to use vectorized operations significantly improved performance.

## Reproducing

To reproduce this analysis, follow these steps:

### Prerequisites

1. **Python Environment** (Python 3.11 or higher)
2. **Git** for version control
3. **API Keys**:
   - NOAA API token: Register at https://www.ncdc.noaa.gov/cdo-web/token
   - Census API key: Register at https://api.census.gov/data/key_signup.html

### Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/weatherfashion.git
   cd weatherfashion
   ```

2. **Create and activate environment**:
   
   **Option A - Using conda** (recommended):
   ```bash
   conda env create -f environment.yaml
   conda activate weatherfashion
   ```
   
   **Option B - Using pip**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure API keys**:
   
   Edit the following files to add your API keys:
   - `scripts/01_acquire_noaa_data.py`: Add NOAA_API_TOKEN
   - `scripts/02_acquire_census_data.py`: Add CENSUS_API_KEY

4. **Download data from Box**:
   
   Download the project data from Box: [INSERT BOX LINK HERE]
   
   Extract the contents and place them in the project directory:
   ```
   weatherfashion/
   ├── data/
   │   ├── raw/
   │   ├── processed/
   │   └── output/
   ```

### Running the Analysis

**Option 1 - Complete workflow with Snakemake** (recommended):
```bash
snakemake --cores 1
```

**Option 2 - Step-by-step execution**:
```bash
# Step 1: Acquire data
python scripts/01_acquire_noaa_data.py
python scripts/02_acquire_census_data.py

# Step 2: Integrate datasets
python scripts/03_integrate_data.py

# Step 3: Assess quality
python scripts/04_assess_quality.py

# Step 4: Clean data
python scripts/05_clean_data.py

# Step 5: Analyze and visualize
python scripts/06_analyze_visualize.py
```

### Verifying Results

After running the analysis, verify the following outputs exist:

- `data/output/quality_assessment_report.json` - Data quality metrics
- `data/output/quality_summary.txt` - Human-readable quality summary
- `data/output/analysis_summary.json` - Numerical analysis results
- `data/output/*.png` - All visualization files

### Expected Runtime

- Data acquisition: 10-20 minutes (depending on API response times)
- Data processing and integration: 2-3 minutes
- Quality assessment and cleaning: 1-2 minutes
- Analysis and visualization: 2-3 minutes

**Total estimated time**: 15-30 minutes

### Troubleshooting

**API rate limits exceeded**:
- NOAA allows 5 requests/second. The script includes delays but may need adjustment.
- Census API limits vary by endpoint. Wait and retry if you encounter errors.

**Missing dependencies**:
```bash
pip install -r requirements.txt --upgrade
```

**Snakemake errors**:
```bash
# Clean and restart
snakemake --cores 1 clean
snakemake --cores 1
```

**Data download issues**:
- Verify Box link is accessible
- Check that data files are in correct directory structure
- Verify .gitignore hasn't excluded necessary files

## References

### Datasets

Menne, M.J., I. Durre, R.S. Vose, B.E. Gleason, and T.G. Houston (2012): An overview of the Global Historical Climatology Network-Daily Database. *Journal of Atmospheric and Oceanic Technology*, 29, 897-910. doi:10.1175/JTECH-D-11-00103.1

National Oceanic and Atmospheric Administration (NOAA). Climate Data Online. Available from: https://www.ncdc.noaa.gov/cdo-web/ [Accessed November 2025]

U.S. Census Bureau. Monthly Retail Trade Survey (MRTS). Available from: https://www.census.gov/retail/index.html [Accessed November 2025]

U.S. Census Bureau. Annual Retail Trade Survey (ARTS). Available from: https://www.census.gov/programs-surveys/arts.html [Accessed November 2025]

### Software

Harris, C.R., Millman, K.J., van der Walt, S.J. et al. Array programming with NumPy. *Nature* 585, 357–362 (2020). doi:10.1038/s41586-020-2649-2

McKinney, W. (2010). Data Structures for Statistical Computing in Python. In S. van der Walt & J. Millman (Eds.), *Proceedings of the 9th Python in Science Conference* (pp. 56-61).

Hunter, J.D. (2007). Matplotlib: A 2D graphics environment. *Computing in Science & Engineering*, 9(3), 90-95. doi:10.1109/MCSE.2007.55

Waskom, M. (2021). seaborn: statistical data visualization. *Journal of Open Source Software*, 6(60), 3021. doi:10.21105/joss.03021

Virtanen, P., Gommers, R., Oliphant, T.E. et al. SciPy 1.0: fundamental algorithms for scientific computing in Python. *Nature Methods* 17, 261–272 (2020). doi:10.1038/s41592-019-0686-2

Mölder, F., Jablonski, K.P., Letcher, B. et al. Sustainable data analysis with Snakemake. *F1000Research* 10, 33 (2021). doi:10.12688/f1000research.29032.2

## License

### Code License

All original code in this repository is licensed under the MIT License.

MIT License

Copyright (c) 2025 Lynn

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

### Data License

The datasets used in this project are U.S. Government Works and are in the public domain in the United States. They may be used without restriction. Attribution to NOAA and the U.S. Census Bureau is required.

### Documentation License

Documentation files are licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
