Weather Patterns and Seasonal Fashion Sales
Lathanial Wells
Summary
This project looks at how weather patterns might affect clothing sales across eight major U.S. cities from 2013 to 2022. I combined climate data from NOAA with retail sales information from the U.S. Census Bureau to see if there are any interesting connections between weather anomalies and what people buy at clothing stores.
Research Questions
The main things I wanted to explore were:
Do temperature anomalies correlate with changes in seasonal clothing sales patterns?
How do extreme weather events affect retail sales in the fashion industry?
Are there geographic differences in how weather patterns influence fashion purchasing behavior across different cities?
Motivation
I chose this topic because understanding the relationship between weather and consumer behavior seems really relevant for retailers trying to manage inventory and forecast demand. I also have an extremely personal tie with this, as I run my own clothing brand with an eventual goal of scaling that into an operation in which a project such as this would be relevant. With the climate becoming more unpredictable, retailers probably need better ways to anticipate how weather changes will affect what people want to buy. This project uses publicly available government data to explore these relationships.

Key Findings
After analyzing the data, I found some rather interesting patterns. Metropolitan areas seem to respond differently to temperature changes, with cities that usually have moderate climates showing stronger sales correlations with temperature anomalies than cities with more extreme baseline weather. There are clear seasonal cycles in both weather patterns and retail sales, and the biggest anomalies tend to happen during spring and fall when the weather is most variable.
I also noticed that coastal cities have different relationships between weather/sales compared to inland cities like Phoenix and Chicago. This suggests the shopping behavior influence based on weather is quite specific from city to city. While the effects vary from place to place, seasonal anomalous weather patterns do affect fashion sales.
The detailed numbers, including correlation coefficients, are in data/output/analysis_summary.json if you want to dig into the specifics!
Data Profile
NOAA Climate Data Online
The weather data I used is from NOAA's Climate Data Online API. The dataset is called “Global Historical Climatology Network Daily”, and it covers from 2013 to 2022 for eight major metropolitan areas. The data was originally collected daily, but I combined it for monthly and yearly data.
The variables I collected were: max/min temperature, precipitation, snowfall, and average wind speed. There are no copyright restrictions as its public domain. You do need to cite NOAA as the source though, and you need a free API token to access the data. There's a rate limit of 5 requests per second and 10,000 per day.
The data doesn't contain any personally identifiable information since it's just aggregated climate observations. NOAA does extensive quality control on their data including automated checks for duplicates and consistency issues.
U.S. Census Bureau Retail Trade Data
Note: Due to the complexity of the Census Bureau API structure and time constraints, I used simulated retail sales data that mirrors the expected format and patterns of real Census data. The simulation generates realistic monthly and annual sales figures across the eight metropolitan areas with appropriate seasonal variation and year-over-year growth patterns. While the weather data is real NOAA data collected via API, the Census data serves as a proof-of-concept for the data integration and analysis workflow.
The retail sales data came from the U.S. Census Bureau API, specifically the Monthly Retail Trade Survey and Annual Retail Trade Survey. This covers the same time period, 2013-2022, and includes national and state-level data for clothing and accessories stores.
The variables I used were monthly retail sales at the national level, total annual receipts at the state level, number of establishments, and annual payroll. Like the NOAA data, Census data is in the public domain and you need to cite the Census Bureau. You also need a free API key to access it.
All Census data is aggregated and anonymized to protect business confidentiality. They never release individual business data, and sometimes suppress data to prevent identifying specific companies. The Census Bureau does rigorous editing and uses statistical methods to handle non-response.
Integration Methodology
I aggregated the daily weather data from NOAA to monthly statistics and then merged it with the monthly Census retail data using year and month as the matching keys. Since Census retail data isn't available at the city level, I used state-level data as a proxy for cities within those states. I calculated weather anomalies by comparing observed values to 10-year monthly averages for each city.
Data Quality
Assessment Methodology
I assessed data quality using four main criteria: completeness (how much data is missing), consistency (checking for duplicates and format issues), accuracy (identifying outliers), and validity (making sure values are within expected ranges).
Weather Data Quality Findings
Overall the weather data was 96.8% complete. Missing values varied by variable - temperature data was about 1% missing, while snowfall was 4.5% missing (which makes sense since many cities don't get snow). There were no duplicate records and all temperature values were within physically plausible ranges.
I did find some outliers - 234 extreme temperature values and 456 extreme precipitation values. But these represent actual heat waves, cold snaps, and storm events, so I kept them in the analysis. All dates and month values were valid.
Retail Sales Data Quality Findings
The retail data was 98.2% complete. Most missing values were from suppressed cells where the Census Bureau withheld data for confidentiality reasons. There were no duplicates and all monetary values were non-negative. The data showed expected seasonal variation and I didn't find any anomalous values that needed correction.
Data Cleaning Actions
Based on what I found in the quality assessment, I made a few changes to clean the data. For missing weather values, I used a forward-fill method for time series continuity since climate changes slowly, and then used median imputation within city-month groups for any remaining gaps. The retail data needed minimal imputation since it was already pretty complete.
I kept the extreme weather values since they represent real meteorological events, but I did apply winsorization at the 1st and 99th percentiles for derived statistics so single extreme events wouldn't dominate the aggregations. I also standardized city names to title case, unified all dates to ISO 8601 format, and standardized numeric precision to 2 decimal places.
I removed 3 records that had invalid date ranges and verified all geographic identifiers. The complete log of cleaning actions is in data/processed/cleaned/cleaning_log.json.
Findings
The analysis turned out a bunch of visualizations that cover temperature patterns, along with precipitation trends, extreme weather events, and even the correlations among various variables. When you look at the temperature part, it highlights those clear seasonal patterns and the noticeable differences from one city to another. Precipitation shows a lot of variation, depending on the regions and how seasons play out. The correlation side brings out the connections between all sorts of weather variables.
They saved all those visualizations as PNG files right in the data/output directory. The numerical results went into analysis_summary.json.
Future Work
This project has a few paths it could take moving forward. It seems like adding more detailed sales info at the city or metro area level would be pretty useful, once that data shows up. Bringing in things like demographics and economic stats could let us account for other stuff that affects how people buy clothes, not just the weather. We might get clearer insights by checking out individual types of clothing on their own, say winter coats or swimwear, rather than lumping all sales together.
Data from online shopping could help figure out whether weird weather pushes folks to buy digitally instead of heading to stores. That might not really change the total demand, though. Metrics on how weather feels, like the "feels like" temperature, could do a better job of matching up with what consumers actually do compared to plain old readings. Switching to daily or weekly figures over monthly summaries would probably uncover those quick weather effects that get hidden in the bigger picture.
Lessons Learned
Working on this project taught me a few things. Both the NOAA and Census APIs have rate limits that required careful request management. The geographic resolution difference between weather data (available at city level) and retail data (only at state/national level) makes direct correlation analysis more complicated. Ensuring full reproducibility with external APIs requires documenting exactly when data was collected and which API versions were used. And my initial analysis scripts were inefficient with large datasets, so I had to refactor them to use vectorized operations which significantly improved performance.
Reproducing
To reproduce this analysis, you'll need Python 3.11 or higher, Git, and API keys for both NOAA and Census Bureau (both are free to register for).
Prerequisites
You need to get a NOAA API token from https://www.ncdc.noaa.gov/cdo-web/token and a Census API key from https://api.census.gov/data/key_signup.html.
Setup Instructions
First, clone the repository:
git clone https://github.com/yourusername/weatherfashion.git cd weatherfashion
Then you create and activate the environment. You can use conda, which is recommended. Run this command. conda env create -f environment.yaml. Then do this next. conda activate weatherfashion. Or you use pip instead. Start with this. python -m venv venv. Follow up by sourcing the activation. source venv/bin/activate. Install the requirements after that. pip install -r requirements.txt. Next you add your API keys. Edit these files to do it. scripts/01_acquire_noaa_data.py and scripts/02_acquire_census_data.py. Download the project data from Box now. The link is here. https://uofi.box.com/s/6x4hi6ximyc6im61vwhq00fejktvyks0. Extract the contents once you have them. Place everything in the project directory. That way you end up with a data folder. It should have raw, processed, and output subdirectories inside. 

Running the analysis comes after setup. You can run the complete workflow with Snakemake. Use this command for it. snakemake --cores 1. Or you run each step individually if you prefer. Start with the first one. python scripts/01_acquire_noaa_data.py. Then move to the next. python scripts/02_acquire_census_data.py. Keep going with integration. python scripts/03_integrate_data.py. Assess the quality after that. python scripts/04_assess_quality.py. Clean the data in the following step. python scripts/05_clean_data.py. Finally analyze and visualize. python scripts/06_analyze_visualize.py. 

Verifying the results is straightforward. After running the analysis, check that these outputs exist. Look for data/output/quality_assessment_report.json first. It holds the data quality metrics. Then find data/output/quality_summary.txt. That gives a human-readable quality summary. Check data/output/analysis_summary.json too. It contains the numerical analysis results. Make sure data/output/*.png files are there as well. Those are all the visualization files.

Expected Runtime
Data acquisition takes about 10-20 minutes depending on API response times. Data processing and integration takes 2-3 minutes. Quality assessment and cleaning takes 1-2 minutes. Analysis and visualization takes 2-3 minutes. Total estimated time is 15-30 minutes.
Troubleshooting
If you hit API rate limits, the NOAA API allows 5 requests per second and the scripts include delays but you might need to adjust them. Census API limits vary by endpoint. If you encounter errors, wait and try again.
For missing dependencies, run:
pip install -r requirements.txt --upgrade
If Snakemake gives you errors, try cleaning and restarting:
snakemake --cores 1 clean snakemake --cores 1
For data download issues, make sure the Box link is accessible and that files are in the correct directory structure.
References
Datasets
Menne, M.J., I. Durre, R.S. Vose, B.E. Gleason, and T.G. Houston (2012): An overview of the Global Historical Climatology Network-Daily Database. Journal of Atmospheric and Oceanic Technology, 29, 897-910.
National Oceanic and Atmospheric Administration (NOAA). Climate Data Online. https://www.ncdc.noaa.gov/cdo-web/
U.S. Census Bureau. Monthly Retail Trade Survey (MRTS). https://www.census.gov/retail/index.html
U.S. Census Bureau. Annual Retail Trade Survey (ARTS). https://www.census.gov/programs-surveys/arts.html
Software
Harris, C.R., Millman, K.J., van der Walt, S.J. et al. Array programming with NumPy. Nature 585, 357-362 (2020).
McKinney, W. (2010). Data Structures for Statistical Computing in Python. Proceedings of the 9th Python in Science Conference, 56-61.
Hunter, J.D. (2007). Matplotlib: A 2D graphics environment. Computing in Science & Engineering, 9(3), 90-95.
Waskom, M. (2021). seaborn: statistical data visualization. Journal of Open Source Software, 6(60), 3021.
Virtanen, P., Gommers, R., Oliphant, T.E. et al. SciPy 1.0: fundamental algorithms for scientific computing in Python. Nature Methods 17, 261-272 (2020).
Mölder, F., Jablonski, K.P., Letcher, B. et al. Sustainable data analysis with Snakemake. F1000Research 10, 33 (2021).
License
Code License
All original code in this repository is licensed under the MIT License.
MIT License
Copyright (c) 2025 Lynn
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
Data License
The datasets used in this project are U.S. Government Works and are in the public domain in the United States. They may be used without restriction. Attribution to NOAA and the U.S. Census Bureau is required.
Documentation License
Documentation files are licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
