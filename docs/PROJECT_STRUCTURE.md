# Project Structure

This document describes the organization of the Weather and Fashion Sales Analysis project.

## Directory Tree

```
weatherfashion/
│
├── README.md                          # Main project documentation
├── LICENSE                            # MIT License for code
├── CITATION.cff                       # Citation information
├── .gitignore                         # Git ignore rules
├── requirements.txt                   # Python dependencies
├── environment.yaml                   # Conda environment specification
├── config.yaml                        # Configuration parameters
├── Snakefile                          # Snakemake workflow definition
├── run_all.sh                         # Bash script to run complete workflow
├── metadata.json                      # Schema.org metadata
│
├── scripts/                           # Analysis scripts
│   ├── 01_acquire_noaa_data.py       # NOAA weather data acquisition
│   ├── 02_acquire_census_data.py     # Census retail data acquisition
│   ├── 03_integrate_data.py          # Data integration
│   ├── 04_assess_quality.py          # Data quality assessment
│   ├── 05_clean_data.py              # Data cleaning
│   └── 06_analyze_visualize.py       # Analysis and visualization
│
├── data/                              # Data directory (in .gitignore)
│   ├── raw/                          # Raw data from sources
│   │   ├── noaa/                     # NOAA weather data
│   │   │   ├── *_weather.json       # City weather files
│   │   │   ├── *.sha256             # Checksums
│   │   │   └── collection_metadata.json
│   │   └── census/                   # Census retail data
│   │       ├── monthly_retail_sales.csv
│   │       ├── annual_retail_sales.csv
│   │       ├── *.sha256             # Checksums
│   │       └── collection_metadata.json
│   │
│   ├── processed/                    # Processed datasets
│   │   ├── weather_monthly.csv      # Monthly aggregated weather
│   │   ├── retail_sales.csv         # Processed retail data
│   │   ├── integration_metadata.json
│   │   └── cleaned/                 # Cleaned datasets
│   │       ├── weather_cleaned.csv
│   │       ├── retail_cleaned.csv
│   │       └── cleaning_log.json
│   │
│   └── output/                       # Analysis outputs
│       ├── quality_assessment_report.json
│       ├── quality_summary.txt
│       ├── analysis_summary.json
│       ├── temperature_analysis.png
│       ├── precipitation_analysis.png
│       ├── extreme_weather_analysis.png
│       ├── correlation_matrix.png
│       └── seasonal_comparison.png
│
├── docs/                              # Documentation
│   ├── DATA_DICTIONARY.md            # Data dictionary
│   └── SETUP.md                      # Setup instructions
│
├── logs/                              # Workflow logs (created at runtime)
│   ├── acquire_noaa.log
│   ├── acquire_census.log
│   ├── integrate_data.log
│   ├── assess_quality.log
│   ├── clean_data.log
│   └── analyze_visualize.log
│
└── workflows/                         # Additional workflow files (optional)
    └── (future workflow definitions)
```

## File Descriptions

### Root Level Files

| File | Purpose | Type |
|------|---------|------|
| `README.md` | Main project documentation with all required sections | Markdown |
| `LICENSE` | MIT License for software code | Text |
| `CITATION.cff` | Citation information in Citation File Format | YAML |
| `.gitignore` | Specifies files Git should ignore | Text |
| `requirements.txt` | Python package dependencies | Text |
| `environment.yaml` | Conda environment specification | YAML |
| `config.yaml` | Configuration parameters for analysis | YAML |
| `Snakefile` | Snakemake workflow definition | Python |
| `run_all.sh` | Bash script for complete workflow execution | Shell |
| `metadata.json` | Schema.org/DataCite metadata | JSON |

### Scripts Directory

All scripts follow a numbered naming convention indicating execution order:

| Script | Purpose | Inputs | Outputs |
|--------|---------|--------|---------|
| `01_acquire_noaa_data.py` | Download NOAA weather data via API | API credentials | `data/raw/noaa/*.json` |
| `02_acquire_census_data.py` | Download Census retail data via API | API credentials | `data/raw/census/*.csv` |
| `03_integrate_data.py` | Integrate weather and retail datasets | Raw data files | `data/processed/*.csv` |
| `04_assess_quality.py` | Assess data quality | Processed data | `data/output/quality*.json` |
| `05_clean_data.py` | Clean and prepare data | Processed data | `data/processed/cleaned/*.csv` |
| `06_analyze_visualize.py` | Analyze and create visualizations | Cleaned data | `data/output/*.png, *.json` |

### Data Directory Structure

The `data/` directory is organized hierarchically:

**`data/raw/`**: Original data from sources
- Never modified after download
- Includes checksums for integrity verification
- Split by data source (noaa, census)

**`data/processed/`**: Intermediate processing results
- Monthly aggregations
- Initial integrations
- Serves as input to cleaning stage

**`data/processed/cleaned/`**: Cleaned final datasets
- Ready for analysis
- Includes cleaning log documenting all transformations

**`data/output/`**: Final analysis results
- Quality reports
- Analysis summaries
- Visualizations (PNG format)

### Documentation Directory

**`docs/DATA_DICTIONARY.md`**: Comprehensive data dictionary
- Variable definitions
- Units and ranges
- Data provenance
- Quality indicators

**`docs/SETUP.md`**: Setup and installation guide
- Prerequisites
- Step-by-step instructions
- Troubleshooting
- System requirements

## File Naming Conventions

### Data Files

- **Raw data**: `{source}_{content}.{ext}`
  - Example: `new_york_weather.json`, `monthly_retail_sales.csv`

- **Processed data**: `{content}_{stage}.{ext}`
  - Example: `weather_monthly.csv`, `weather_cleaned.csv`

- **Metadata**: `{type}_metadata.json`
  - Example: `collection_metadata.json`, `integration_metadata.json`

- **Checksums**: `{filename}.{ext}.sha256`
  - Example: `weather_cleaned.csv.sha256`

### Output Files

- **Visualizations**: `{analysis_type}_analysis.png`
  - Example: `temperature_analysis.png`

- **Reports**: `{type}_report.json`
  - Example: `quality_assessment_report.json`

- **Summaries**: `{content}_summary.{ext}`
  - Example: `analysis_summary.json`, `quality_summary.txt`

### Log Files

- **Format**: `{script_name}.log`
  - Example: `acquire_noaa.log`, `analyze_visualize.log`

## Data Flow

```
External APIs
     │
     ├── NOAA CDO API ──────────► [01_acquire_noaa_data.py]
     │                                    │
     └── Census API ────────────► [02_acquire_census_data.py]
                                          │
                                          ▼
                                   data/raw/{source}/
                                          │
                                          ▼
                              [03_integrate_data.py]
                                          │
                                          ▼
                                 data/processed/
                                          │
                                          ├──► [04_assess_quality.py] ──► data/output/quality*
                                          │
                                          ▼
                               [05_clean_data.py]
                                          │
                                          ▼
                            data/processed/cleaned/
                                          │
                                          ▼
                           [06_analyze_visualize.py]
                                          │
                                          ▼
                             data/output/{visualizations, summaries}
```

## Version Control Strategy

### Files Tracked in Git

- All source code (`scripts/`)
- Documentation (`docs/`, `README.md`, etc.)
- Configuration files (`config.yaml`, `Snakefile`, etc.)
- Requirements files (`requirements.txt`, `environment.yaml`)
- Metadata (`metadata.json`, `CITATION.cff`)
- License files

### Files Ignored by Git (in `.gitignore`)

- Data files (`data/`)
- Log files (`logs/`)
- Python cache (`__pycache__/`, `*.pyc`)
- Virtual environments (`venv/`, `.venv/`)
- Snakemake metadata (`.snakemake/`)
- IDE files (`.vscode/`, `.idea/`)

### Data Sharing Strategy

- **Raw and processed data**: Shared via Box
- **Code and documentation**: Shared via GitHub
- **Long-term archival**: Zenodo (optional)

## Reproducibility Components

### Required for Full Reproduction

1. **Code**: All scripts in `scripts/` directory
2. **Workflow**: `Snakefile` or `run_all.sh`
3. **Dependencies**: `requirements.txt` and `environment.yaml`
4. **Configuration**: `config.yaml`
5. **Documentation**: `README.md` with reproduction steps
6. **Data**: Either raw data or acquisition scripts + API keys

### Provenance Tracking

- `collection_metadata.json`: When data was acquired, from where
- `integration_metadata.json`: How data was integrated
- `cleaning_log.json`: What transformations were applied
- Git commit history: Code evolution

## Adding New Components

### Adding a New Analysis Script

1. Create script: `scripts/07_new_analysis.py`
2. Update `Snakefile`: Add new rule
3. Update `README.md`: Document new analysis
4. Update `config.yaml`: Add parameters if needed

### Adding New Data Sources

1. Create acquisition script: `scripts/0X_acquire_newdata.py`
2. Create directory: `data/raw/newsource/`
3. Update `.gitignore`: Add new data directory
4. Update integration script to include new source
5. Update documentation

## Maintenance

### Regular Tasks

- Update dependencies: `pip install -r requirements.txt --upgrade`
- Re-run quality checks periodically
- Update documentation for code changes
- Refresh API keys as they expire

### Archival Checklist

Before creating final release:

1. ✅ All scripts run without errors
2. ✅ All outputs generated
3. ✅ Documentation complete and accurate
4. ✅ Data uploaded to Box
5. ✅ API keys removed from code
6. ✅ README.md has Box link
7. ✅ Git tag created
8. ✅ GitHub release published
9. ✅ Zenodo archive created (optional)
10. ✅ DOI updated in metadata
