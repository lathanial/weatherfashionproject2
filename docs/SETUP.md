# Setup and Installation Guide

This guide provides detailed instructions for setting up the Weather and Fashion Sales Analysis project on your local machine.

## Prerequisites

Before beginning, ensure you have the following installed:

- **Python 3.11 or higher** - [Download Python](https://www.python.org/downloads/)
- **Git** - [Install Git](https://git-scm.com/downloads)
- **Conda** (optional but recommended) - [Install Miniconda](https://docs.conda.io/en/latest/miniconda.html)

You will also need:
- **NOAA API Token** - [Register here](https://www.ncdc.noaa.gov/cdo-web/token)
- **Census API Key** - [Register here](https://api.census.gov/data/key_signup.html)

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/lynnpepin/weatherfashion.git
cd weatherfashion
```

### 2. Set Up Python Environment

**Option A: Using Conda (Recommended)**

```bash
# Create environment from file
conda env create -f environment.yaml

# Activate environment
conda activate weatherfashion

# Verify installation
python --version
pip list
```

**Option B: Using venv and pip**

```bash
# Create virtual environment
python -m venv venv

# Activate environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Verify installation
python --version
pip list
```

### 3. Configure API Keys

Edit the following files to add your API credentials:

**NOAA API Token** in `scripts/01_acquire_noaa_data.py`:
```python
NOAA_API_TOKEN = "your_actual_token_here"
```

**Census API Key** in `scripts/02_acquire_census_data.py`:
```python
CENSUS_API_KEY = "your_actual_key_here"
```

### 4. Download Data from Box (Optional)

If you want to skip data acquisition and use pre-collected data:

1. Download the data archive from Box: [INSERT BOX LINK]
2. Extract the archive
3. Place the contents in the project directory:

```
weatherfashion/
├── data/
│   ├── raw/
│   │   ├── noaa/
│   │   └── census/
│   ├── processed/
│   └── output/
```

### 5. Run the Analysis

**Option A: Using Snakemake (Recommended)**

```bash
# Run complete workflow
snakemake --cores 1

# Or with more cores for parallel processing
snakemake --cores 4
```

**Option B: Using the Run-All Script**

```bash
# Make script executable (Unix/macOS)
chmod +x run_all.sh

# Run the script
./run_all.sh
```

**Option C: Step-by-Step Manual Execution**

```bash
python scripts/01_acquire_noaa_data.py
python scripts/02_acquire_census_data.py
python scripts/03_integrate_data.py
python scripts/04_assess_quality.py
python scripts/05_clean_data.py
python scripts/06_analyze_visualize.py
```

## Detailed Setup Instructions

### Installing Snakemake

If you want to use Snakemake for workflow automation:

**With Conda:**
```bash
conda install -c conda-forge -c bioconda snakemake
```

**With pip:**
```bash
pip install snakemake
```

### Creating a Logs Directory

The workflow creates log files for each step:

```bash
mkdir -p logs
```

### Verifying Your Installation

Run this verification script to check all dependencies:

```bash
python -c "
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from scipy import stats
print('All dependencies successfully imported!')
print(f'Pandas version: {pd.__version__}')
print(f'NumPy version: {np.__version__}')
print(f'Matplotlib version: {plt.__version__}')
"
```

## Troubleshooting

### Common Issues and Solutions

#### 1. Module Not Found Error

**Error**: `ModuleNotFoundError: No module named 'pandas'`

**Solution**:
```bash
# Ensure environment is activated
conda activate weatherfashion  # or source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

#### 2. API Rate Limit Exceeded

**Error**: `HTTP 429: Too Many Requests`

**Solution**:
- NOAA API allows 5 requests/second. The script includes delays but you may need to increase them.
- Wait 1 hour before retrying
- Edit delay values in acquisition scripts if needed

#### 3. Permission Denied on Scripts

**Error**: `Permission denied: ./run_all.sh`

**Solution**:
```bash
chmod +x run_all.sh
```

#### 4. Snakemake Not Found

**Error**: `snakemake: command not found`

**Solution**:
```bash
# Ensure environment is activated
conda activate weatherfashion

# Install Snakemake
conda install -c conda-forge -c bioconda snakemake
```

#### 5. API Key Not Working

**Errors**:
- `401 Unauthorized`
- `403 Forbidden`

**Solutions**:
- Verify API keys are correctly copied (no extra spaces)
- Check that keys haven't expired
- Request new keys if necessary
- Wait a few minutes after requesting keys (they may not be instantly active)

#### 6. Memory Issues with Large Datasets

**Error**: `MemoryError` or system slowdown

**Solution**:
```bash
# Process data in chunks or use fewer cities
# Close other applications
# Increase system swap space if needed
```

## System Requirements

### Minimum Requirements

- **RAM**: 4 GB
- **Storage**: 2 GB free space
- **Processor**: Dual-core CPU
- **OS**: Windows 10, macOS 10.14+, or Linux (Ubuntu 18.04+)

### Recommended Requirements

- **RAM**: 8 GB or more
- **Storage**: 5 GB free space
- **Processor**: Quad-core CPU
- **OS**: Latest versions of Windows, macOS, or Linux

## Network Requirements

- Stable internet connection for API access
- Ability to access:
  - `api.ncei.noaa.gov` (NOAA API)
  - `api.census.gov` (Census API)
  - `pypi.org` (Python packages)

If behind a firewall or proxy, you may need to configure proxy settings.

## Development Setup

If you plan to modify or extend the code:

### Install Development Tools

```bash
pip install black pytest pylint jupyter
```

### Code Formatting

```bash
# Format code with Black
black scripts/
```

### Running Tests

```bash
# Run tests (if test suite exists)
pytest tests/
```

### Jupyter Notebooks

```bash
# Start Jupyter for interactive analysis
jupyter notebook
```

## Next Steps

After successful setup:

1. **Explore the data**: Review files in `data/output/`
2. **Read the documentation**: Check `docs/DATA_DICTIONARY.md`
3. **Review quality reports**: See `data/output/quality_assessment_report.json`
4. **Examine visualizations**: Open PNG files in `data/output/`
5. **Modify parameters**: Edit `config.yaml` for custom analysis

## Getting Help

If you encounter issues not covered here:

1. Check the [GitHub Issues](https://github.com/lynnpepin/weatherfashion/issues)
2. Review the main [README.md](README.md)
3. Contact the maintainer (Lynn)

## Updating

To update the project with latest changes:

```bash
# Pull latest changes
git pull origin main

# Update dependencies
conda env update -f environment.yaml  # if using conda
# OR
pip install -r requirements.txt --upgrade  # if using pip
```

## Uninstalling

To completely remove the project:

```bash
# Deactivate environment
conda deactivate  # or deactivate

# Remove environment
conda env remove -n weatherfashion  # if using conda
# OR
rm -rf venv/  # if using venv

# Remove project directory
cd ..
rm -rf weatherfashion/
```
